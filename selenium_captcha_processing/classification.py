import logging
from typing import Optional, List

from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.captcha import Captcha
from selenium_captcha_processing.config import Config
from selenium_captcha_processing.data import CaptchaNote
from selenium_captcha_processing.factory import make_default_config, make_default_utils, make_detector_type
from selenium_captcha_processing.utils.container import Utils

logger = logging.getLogger(__name__)

class Classify:
    def __init__(self, driver: WebDriver, utils: Optional[Utils] = None, config: Optional[Config] = None):
        """
        Initialize the Classify instance for captcha classification.
        :param driver: The Selenium WebDriver instance used for browser automation.
        :param utils: Optional utilities container for captcha processing, defaults to None.
        :param config: Optional configuration for captcha processing, defaults to None.
        """
        self.config = config or make_default_config()
        self.utils = utils or make_default_utils(self.config)
        self.driver = driver

    def classify(self) -> List[CaptchaNote]:
        """
        Classify potential captchas on the page via detectors.
        :return: A list of CaptchaNote objects representing detected captchas.
        """
        notes: List[CaptchaNote] = []
        for captcha in Captcha:
            detector_type = make_detector_type(captcha)
            if detector_type is None:
                logger.warning(f'There is no detector for {captcha} yet.')
                continue

            detector = detector_type(self.driver, self.utils, self.config)
            detected_prob = 0.0
            try:
                detected_prob = detector.detected()
            except Exception as e:
                logger.error(f'Error occurred while detecting: {str(e)}')
                if self.config.raise_exceptions_in_detection:
                    raise e

            logger.debug(f'The probability of {captcha} detected as {detected_prob}.')
            if detected_prob < self.config.detection_threshold:
                logger.debug(
                    f'Too little probability of {captcha}: {detected_prob} < {self.config.detection_threshold}.'
                )
                continue

            note = CaptchaNote(
                captcha=captcha, prob=detected_prob,
                detector=detector, solver=None
            )

            notes.append(note)
            if len(notes) >= self.config.max_detections_in_classification:
                logger.debug('The maximum number of detections has been reached.')
                break

        return notes