from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.detectors.interfaces.detector import DetectCaptchaI
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.utils.container import Utils


class DetectUnknownImageCaptcha(DetectCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def detected(self) -> float:
        score = 0.0

        captcha_image_xpath = """
        //img[
            contains(translate(@*, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha') or
            contains(translate(../@*, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha') or
            contains(translate(../../@*, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha') or
            contains(translate(../../../@*, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha')
        ]
        """
        captcha_images = self.driver.find_elements(
            By.XPATH, captcha_image_xpath
        )
        displayed_captcha_images_cnt = 0
        for captcha_image in captcha_images:
            displayed_captcha_images_cnt += int(captcha_image.is_displayed())

        if displayed_captcha_images_cnt:
            score += 0.4

        captcha_input_xpath = """
        //input[
            contains(translate(@*, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha') or
            contains(translate(../@*, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha') or
            contains(translate(../../@*, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha') or
            contains(translate(../../../@*, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha')
        ]
        """
        captcha_inputs = self.driver.find_elements(
            By.XPATH, captcha_input_xpath
        )
        displayed_captcha_inputs_cnt = 0
        for captcha_input in captcha_inputs:
            displayed_captcha_inputs_cnt += int(captcha_input.is_displayed())

        if displayed_captcha_inputs_cnt:
            score += 0.4

        return score