from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.config import Config
from selenium_captcha_processing.helpers import find_element_safely
from selenium_captcha_processing.solvers.interfaces.solver import SolveCaptchaI
from selenium_captcha_processing.utils.container import Utils


class SolveCloudflareTurnstile(SolveCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def solve(self) -> bool:
        main_host = find_element_safely(
            self.driver, By.XPATH, "//*[@name='cf-turnstile-response']/..",
            self.config.default_element_waiting
        )
        if main_host is None or not main_host.is_displayed():
            main_host = find_element_safely(
                self.driver, By.XPATH, "//*[@data-sitekey]",
                self.config.default_element_waiting
            )

        if main_host is None or not main_host.is_displayed():
            return False

        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(
            main_host, round(-main_host.size['width'] / 2 + 30), round(-main_host.size['height'] / 2 + 30)
        ).click().perform()

        return True
