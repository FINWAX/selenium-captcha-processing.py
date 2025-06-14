from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """
    Configuration settings for captcha processing.
    :param detection_threshold: Probability threshold for captcha detection.
    :param max_detections_in_classification: Maximum number of captchas to successfully detect.
    :param wait_after_solving: Time to wait after solving a captcha, in seconds.
    :param max_solutions_without_effect: Maximum number of ineffective solutions before stopping.
    :param default_element_waiting: Default wait time for elements, in seconds.
    :param speech_language: Language for speech recognition.
    :param google_api_speech_recognition_api_key: API key for Google Speech Recognition.
    :param google_api_timeout: Timeout for Google API requests.
    :param raise_exceptions_in_detection: Flag for enabling errors that occur when captchas are detected (not applied directly in detectors).
    :param raise_exceptions_in_solving: Flag for enabling errors that occur when captchas are solving (not applied directly in solvers).
    """
    detection_threshold: float = 0.5
    max_detections_in_classification: int = 3
    wait_after_solving: int = 5
    max_solutions_without_effect: int = 3
    default_element_waiting: float = 0.5

    speech_language: str = 'en-US'
    # This is key from: https://github.com/thicccat688/selenium-recaptcha-solver
    google_api_speech_recognition_api_key: str = 'AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw'
    google_api_timeout: Optional[float] = None

    raise_exceptions_in_detection: bool = False
    raise_exceptions_in_solving: bool = False
