import logging
from operator import attrgetter
from time import sleep
from typing import Optional, List

from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.config import Config
from selenium_captcha_processing.data import CaptchaNote
from selenium_captcha_processing.factory import make_default_config, make_default_utils, make_solver_type
from selenium_captcha_processing.utils.container import Utils

logger = logging.getLogger(__name__)

class Solve:
    def __init__(self, driver: WebDriver, utils: Optional[Utils] = None, config: Optional[Config] = None):
        """
        Initialize the Solve instance for captcha solving.
        :param driver: The Selenium WebDriver instance used for browser automation.
        :param utils: Optional utilities container for captcha processing, defaults to None.
        :param config: Optional configuration for captcha processing, defaults to None.
        """
        self.config = config or make_default_config()
        self.utils = utils or make_default_utils(self.config)
        self.driver = driver

    def solve(self, captcha_notes: List[CaptchaNote]) -> bool:
        """
        Attempt to solve the provided captchas.
        :param captcha_notes: A list of CaptchaNote objects representing captchas to solve.
        :return: True if a captcha was successfully solved, False otherwise.
        """
        captcha_notes.sort(key=attrgetter('prob'), reverse=True)

        solutions_without_effect = 0
        for note in captcha_notes:
            solver_type = make_solver_type(note.captcha)
            if solver_type is None:
                logger.debug(f'There is no solver for {note.captcha} yet.')
                continue

            note.solver = solver_type(self.driver, self.utils, self.config)
            solved = False
            try:
                solved = note.solver.solve()
            except Exception as e:
                logger.error(f'Error occurred while solving: {str(e)}')
                if self.config.raise_exceptions_in_solving:
                    raise e
            if not solved:
                logger.info(f'Failed to solve {note.captcha}.')
                continue

            if self.config.wait_after_solving >= 1:
                logger.debug(f'Waiting {self.config.wait_after_solving}s after successful {note.captcha} solving.')
                sleep(self.config.wait_after_solving)

            new_prob = 1.0
            try:
                new_prob = note.detector.detected()
            except Exception as e:
                logger.error(f'Error occurred while detecting: {str(e)}')
                if self.config.raise_exceptions_in_detection:
                    raise e
            if new_prob < note.prob:
                logger.info(
                    f'Successful decreasing of {note.captcha} probability after solving: {note.prob} vs {new_prob}.'
                )
                return True

            solutions_without_effect += 1
            if solutions_without_effect >= self.config.max_solutions_without_effect:
                logger.debug(
                    f'The limit<{self.config.max_solutions_without_effect}> of ineffective solutions has been reached.'
                )
                break

        return False