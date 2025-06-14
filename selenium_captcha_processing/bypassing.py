import logging
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.classification import Classify
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.factory import make_default_utils, make_default_config
from selenium_captcha_processing.solving import Solve
from selenium_captcha_processing.utils.container import Utils

logger = logging.getLogger(__name__)

class BypassCaptcha:
    def __init__(self, driver: WebDriver, utils: Optional[Utils] = None, config: Optional[Config] = None):
        """
        Initialize the BypassCaptcha instance.
        :param driver: The Selenium WebDriver instance used for browser automation.
        :param utils: Optional utilities container for captcha processing, defaults to None.
        :param config: Optional configuration for captcha processing, defaults to None.
        """
        self.config = config or make_default_config()
        self.utils = utils or make_default_utils(self.config)
        self.driver = driver

        self.classification = Classify(self.driver, self.utils, self.config)
        self.solving = Solve(self.driver, self.utils, self.config)

    def bypass(self):
        """
        Attempt to bypass detected captchas.
        :return: True if captcha is bypassed or no captcha is detected, False otherwise.
        """
        notes = self.classification.classify()
        if not notes:
            logger.info('No detected captcha.')
            return True

        return self.solving.solve(notes)