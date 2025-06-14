from abc import ABC, abstractmethod

from selenium_captcha_processing.config import Config

class SpeechRecogniserI(ABC):
    @abstractmethod
    def __init__(self, config: Config):
        """
        Initialize the speech recognizer interface.
        :param config: Configuration for speech recognition.
        """
        pass

    @abstractmethod
    def recognise_from_file(self, speech_file: str) -> None | str:
        """
        Recognize speech from an audio file.
        :param speech_file: Path to the audio file to recognize.
        :return: The recognized text or None if recognition fails.
        """
        pass