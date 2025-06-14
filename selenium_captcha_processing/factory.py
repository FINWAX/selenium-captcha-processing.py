from typing import Optional, Type

from selenium_captcha_processing.captcha import Captcha
from selenium_captcha_processing.detectors.detect_cloudflare_turnstile import DetectCloudflareTurnstile
from selenium_captcha_processing.detectors.detect_cloudflare_turnstile_page import DetectCloudflareTurnstilePage
from selenium_captcha_processing.detectors.detect_geetest_captcha import DetectGeetest
from selenium_captcha_processing.detectors.detect_key_captcha import DetectKeyCaptcha
from selenium_captcha_processing.detectors.detect_lemin_captcha import DetectLeminCaptcha
from selenium_captcha_processing.detectors.detect_mt_captcha import DetectMTCaptcha
from selenium_captcha_processing.detectors.detect_re_captcha import DetectReCaptcha
from selenium_captcha_processing.detectors.detect_unknown_image_captcha import DetectUnknownImageCaptcha
from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.solvers.interfaces.solver import SolveCaptchaI
from selenium_captcha_processing.solvers.solve_cloudflare_turnstile import SolveCloudflareTurnstile
from selenium_captcha_processing.solvers.solve_re_captcha import SolveReCaptcha
from selenium_captcha_processing.utils.container import Utils
from selenium_captcha_processing.utils.recognize_speech_by_google_api import RecognizeSpeechByGoogleApi

def make_detector_type(captcha: Captcha) -> Optional[Type[DetectCaptchaI]]:
    """
    Create a detector type based on the captcha type.
    :param captcha: The type of captcha to detect.
    :return: The detector type or None if no detector exists.
    """
    match captcha:
        case captcha.reCaptcha:
            return DetectReCaptcha
        case captcha.CloudflareTurnstile:
            return DetectCloudflareTurnstile
        case captcha.CloudflareTurnstilePage:
            return DetectCloudflareTurnstilePage
        case captcha.GeeTest:
            return DetectGeetest
        case captcha.KeyCaptcha:
            return DetectKeyCaptcha
        case captcha.MTCaptcha:
            return DetectMTCaptcha
        case captcha.LeminCaptcha:
            return DetectLeminCaptcha
        case captcha.unknown_image_captcha:
            return DetectUnknownImageCaptcha
        case _:
            return None

def make_solver_type(captcha: Captcha) -> Optional[Type[SolveCaptchaI]]:
    """
    Create a solver type based on the captcha type.
    :param captcha: The type of captcha to solve.
    :return: The solver type or None if no solver exists.
    """
    match captcha:
        case captcha.reCaptcha:
            return SolveReCaptcha
        case captcha.CloudflareTurnstile | captcha.CloudflareTurnstilePage:
            return SolveCloudflareTurnstile
        case _:
            return None

def make_default_utils(config: Optional[Config]):
    """
    Create a default utilities container.
    :param config: Optional configuration for utilities, defaults to None.
    :return: A configured utilities container.
    """
    if config is None:
        config = make_default_config()

    utils = Utils()
    utils.speech_recogniser = RecognizeSpeechByGoogleApi(config)

    return utils

def make_default_config():
    """
    Create a default configuration for captcha processing.
    :return: A default configuration instance.
    """
    return Config()