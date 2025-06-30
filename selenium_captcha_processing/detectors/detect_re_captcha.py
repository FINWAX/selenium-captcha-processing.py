from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selmate.composites import element_displayed_enabled
from selmate.selenium_primitives import find_element_safely

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.utils.container import Utils


class DetectReCaptcha(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        score = 0.0

        recaptcha_iframe = find_element_safely(
            By.XPATH, '//iframe[@title="reCAPTCHA"]',
            self.driver,
            self.config.default_element_waiting
        )
        if recaptcha_iframe and element_displayed_enabled(recaptcha_iframe):
            score += 0.25

        site_key = find_element_safely(
            By.XPATH, '//*[@data-sitekey]',
            self.driver,
            self.config.default_element_waiting
        )
        if site_key and element_displayed_enabled(site_key):
            score += 0.5

        js_obj = self.driver.execute_script("return typeof window.grecaptcha !== 'undefined';")
        if js_obj:
            score += 0.25

        return score