from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.utils.container import Utils


class DetectKeyCaptcha(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        page_source = self.driver.page_source
        key_captcha_substrings = [
            's_s_c_user_id',
            's_s_c_session_id',
            's_s_c_web_server_sign',
            's_s_c_web_server_sign2'
        ]
        key_captcha_occurrences = sum([1 for s in key_captcha_substrings if s in page_source])

        return key_captcha_occurrences / len(key_captcha_substrings)
