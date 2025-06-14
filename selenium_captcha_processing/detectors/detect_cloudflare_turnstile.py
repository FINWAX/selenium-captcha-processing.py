from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.helpers import find_element_safely
from selenium_captcha_processing.utils.container import Utils


class DetectCloudflareTurnstile(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        score = 0.0

        host_el = find_element_safely(
            self.driver, By.XPATH, "//*[@data-sitekey]",
            self.config.default_element_waiting
        )
        if host_el and host_el.is_displayed():
            score += 0.25

        response_el = find_element_safely(
            self.driver, By.XPATH, '//*[@name="cf-turnstile-response"]',
            self.config.default_element_waiting
        )
        if response_el is not None:
            score += 0.3

            if not response_el.get_attribute('value'):
                score += 0.1

        js_obj = self.driver.execute_script("return typeof window.turnstile !== 'undefined';")
        if js_obj:
            score += 0.35

        return score
