import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from speech_recognition import Recognizer, AudioFile, UnknownValueError, AudioData

from selenium_captcha_processing.config import Config
from selenium_captcha_processing.utils.interfaces.speech_recogniser import SpeechRecogniserI

class RecognizeSpeechByGoogleApi(SpeechRecogniserI):
    def __init__(self, config: Config):
        """
        Initialize the Google API speech recognizer.
        :param config: Configuration for speech recognition.
        """
        self.config = config
        self.recognizer = Recognizer()
        self.recognizer.dynamic_energy_threshold = False

    def recognise_from_file(self, speech_file: str) -> None | str:
        """
        Recognize speech from an audio file using Google Speech API.
        :param speech_file: Path to the audio file to recognize.
        :return: The recognized text or None if recognition fails.
        """
        with AudioFile(speech_file) as source:
            audio_data = self.recognizer.listen(source)
            return self._recognize_via_api(audio_data)

    def _recognize_via_api(self, audio_data: AudioData):
        flac_data = audio_data.get_flac_data(
            convert_rate=None if audio_data.sample_rate >= 8000 else 8000,
            convert_width=2
        )
        url = "http://www.google.com/speech-api/v2/recognize?{}".format(urlencode({
            "client": "chromium",
            "lang": self.config.speech_language,
            "key": self.config.google_api_speech_recognition_api_key,
        }))
        request = Request(
            url, data=flac_data,
            headers={"Content-Type": "audio/x-flac; rate={}".format(audio_data.sample_rate)}
        )

        response = urlopen(request, timeout=self.config.google_api_timeout)
        response_text = response.read().decode("utf-8")

        actual_result = []
        for line in response_text.split("\n"):
            if not line: continue
            result = json.loads(line)["result"]
            if len(result) != 0:
                actual_result = result[0]
                break

        if not isinstance(actual_result, dict) or len(actual_result.get("alternative", [])) == 0:
            raise UnknownValueError()

        if "confidence" in actual_result["alternative"]:
            best_hypothesis = max(actual_result["alternative"], key=lambda alternative: alternative["confidence"])
        else:
            best_hypothesis = actual_result["alternative"][0]

        if "transcript" not in best_hypothesis: raise UnknownValueError()
        return best_hypothesis["transcript"]