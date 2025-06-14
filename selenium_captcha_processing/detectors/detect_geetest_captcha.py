from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.helpers import find_element_safely
from selenium_captcha_processing.utils.container import Utils


class DetectGeetest(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        score = 0.0

        script = find_element_safely(
            self.driver, By.XPATH,
            "//script[starts-with(@src, 'https://api.geetest.com/get')]",
            self.config.default_element_waiting
        )
        if script:
            score += 0.5

        btn = find_element_safely(
            self.driver, By.CLASS_NAME, 'geetest_btn',
            self.config.default_element_waiting
        )
        if btn and btn.is_displayed():
            score += 0.5

        return score
