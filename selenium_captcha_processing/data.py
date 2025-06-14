from dataclasses import dataclass

from selenium_captcha_processing.captcha import Captcha
from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.solvers.interfaces.solver import SolveCaptchaI

@dataclass
class CaptchaNote:
    """
    Data class to store information about a detected captcha.
    :param captcha: The type of captcha detected.
    :param prob: The probability that the captcha is present.
    :param detector: The detector used to detect the captcha, defaults to None.
    :param solver: The solver used to solve the captcha, defaults to None.
    """
    captcha: Captcha
    prob: float
    detector: None | DetectCaptchaI = None
    solver: None | SolveCaptchaI = None