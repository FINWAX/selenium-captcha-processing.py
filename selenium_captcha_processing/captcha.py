from enum import Enum


class Captcha(Enum):
    """
    Enumeration of supported captcha types.
    """
    reCaptcha = 'reCaptcha'
    GeeTest = 'GeeTest'
    CloudflareTurnstile = 'CloudflareTurnstile'
    CloudflareTurnstilePage = 'CloudflareTurnstilePage'
    KeyCaptcha = 'KeyCaptcha'
    LeminCaptcha = 'LeminCaptcha'
    MTCaptcha = 'MTCaptcha'

    unknown_image_captcha = 'unknown_image_captcha'
