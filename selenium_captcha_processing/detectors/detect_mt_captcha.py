from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.helpers import find_element_safely
from selenium_captcha_processing.utils.container import Utils


class DetectMTCaptcha(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        score = 0.0

        iframe = find_element_safely(
            self.driver, By.XPATH, "//iframe[contains(@src, 'mtcap') or contains(@id, 'mtcap')]",
            self.config.default_element_waiting
        )
        if iframe is not None and iframe.is_displayed():
            score += 0.5

        js_obj = self.driver.execute_script("return typeof window.mtcaptcha !== 'undefined';")
        if js_obj:
            score += 0.25

        js_config_obj = self.driver.execute_script("return typeof window.mtcaptchaConfig !== 'undefined';")
        if js_config_obj:
            score += 0.25

        return score
