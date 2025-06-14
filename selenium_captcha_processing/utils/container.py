from dataclasses import dataclass

from selenium_captcha_processing.utils.interfaces.speech_recogniser import SpeechRecogniserI

@dataclass
class Utils:
    """
    Container for utility instances used in captcha processing.
    :param speech_recogniser: Optional speech recognizer instance, defaults to None.
    """
    speech_recogniser: None | SpeechRecogniserI = None