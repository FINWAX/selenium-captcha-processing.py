from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selmate.composites import element_displayed_enabled
from selmate.selenium_primitives import find_element_safely

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.utils.container import Utils


class DetectLeminCaptcha(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        score = 0.0

        scripts = self.driver.find_elements(
            By.XPATH,
            "//script[starts-with(@src, 'https://api.leminnow.com/captcha')]"
        )
        if scripts:
            score += 0.25

        js_obj = self.driver.execute_script("return typeof window.leminCroppedCaptcha !== 'undefined';")
        if js_obj:
            score += 0.2

        div = find_element_safely(
            By.ID, 'lemin-cropped-captcha',
            self.driver,
            self.config.default_element_waiting
        )
        if div is not None and element_displayed_enabled(div):
            score += 0.55

        return score
