from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.helpers import find_element_safely
from selenium_captcha_processing.utils.container import Utils


class DetectCloudflareTurnstilePage(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        score = 0.0

        response_el = find_element_safely(
            self.driver, By.XPATH, '//*[@name="cf-turnstile-response"]',
            self.config.default_element_waiting
        )
        if response_el is not None:
            score += 0.3

        js_obj = self.driver.execute_script("return typeof window.turnstile !== 'undefined';")
        if js_obj:
            score += 0.45

        return score
