from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selmate.composites import element_displayed_enabled
from selmate.selenium_primitives import find_element_safely

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.utils.container import Utils


class DetectCloudflareTurnstile(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        score = 0.0

        host_el = find_element_safely(
            By.XPATH, "//*[@data-sitekey]",
            self.driver,
            self.config.default_element_waiting
        )
        if host_el and element_displayed_enabled(host_el):
            score += 0.25

        response_el = find_element_safely(
            By.XPATH, '//*[@name="cf-turnstile-response"]',
            self.driver,
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
