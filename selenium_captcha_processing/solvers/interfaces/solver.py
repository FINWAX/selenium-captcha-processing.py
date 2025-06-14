from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.config import Config
from selenium_captcha_processing.utils.container import Utils

class SolveCaptchaI(ABC):
    @abstractmethod
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        """
        Initialize the captcha solver interface.
        :param driver: The Selenium WebDriver instance used for browser automation.
        :param utils: Utilities container for captcha processing.
        :param config: Configuration for captcha processing.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        pass

    @abstractmethod
    def solve(self) -> bool:
        """
        Attempt to solve the captcha.
        :return: True if the captcha was solved successfully, False otherwise.
        """
        pass
