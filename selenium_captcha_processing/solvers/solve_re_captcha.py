import os
import tempfile
import uuid

from pydub import AudioSegment
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selmate.composites import complex_click, selenium_human_type
from selmate.selenium_primitives import find_element_safely

from selenium_captcha_processing.config import Config
from selenium_captcha_processing.helpers import download_audio
from selenium_captcha_processing.solvers.interfaces.solver import SolveCaptchaI
from selenium_captcha_processing.utils.container import Utils


class SolveReCaptcha(SolveCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def solve(self) -> bool:
        recaptcha_iframe = find_element_safely(
            By.XPATH, '//iframe[@title="reCAPTCHA"]',
            self.driver,
            self.config.default_element_waiting
        )
        if recaptcha_iframe is None:
            return False

        self.driver.switch_to.frame(recaptcha_iframe)

        checkbox = find_element_safely(
            By.ID, 'recaptcha-anchor',
            self.driver,
            self.config.default_element_waiting
        )
        if checkbox is None:
            self.driver.switch_to.parent_frame()
            return False

        complex_click(checkbox, self.driver, prevent_unselect=True)
        if checkbox.get_attribute('aria-checked') == 'true':
            self.driver.switch_to.parent_frame()
            return True

        self.driver.switch_to.parent_frame()

        return self._solve_challenge()

    def _solve_challenge(self):
        captcha_challenge = find_element_safely(
            By.XPATH,
            '//iframe[contains(@src, "recaptcha") and contains(@src, "bframe")]',
            self.driver,
            timeout=5,
        )

        if not captcha_challenge:
            return False

        self.driver.switch_to.frame(captcha_challenge)

        audio_btn = find_element_safely(
            By.XPATH,
            '//*[@id="recaptcha-audio-button"]',
            self.driver,
            timeout=1.5,
        )
        if audio_btn is None:
            return False

        complex_click(audio_btn, self.driver)

        download_link = find_element_safely(
            By.CLASS_NAME,
            'rc-audiochallenge-tdownload-link',
            self.driver,
            timeout=7,
        )
        if download_link is None:
            return False

        tmp_dir = tempfile.gettempdir()
        audio_file_id = uuid.uuid4().hex
        tmp_files = (
            os.path.join(tmp_dir, f'{audio_file_id}_tmp.mp3'),
            os.path.join(tmp_dir, f'{audio_file_id}_tmp.wav')
        )
        mp3_file, wav_file = tmp_files

        link = download_link.get_attribute('href')
        try:
            download_audio(link, mp3_file)
            AudioSegment.from_mp3(mp3_file).export(wav_file, format='wav')
            recognized_text = self.utils.speech_recogniser.recognise_from_file(wav_file)
        finally:
            for path in tmp_files:
                if os.path.exists(path):
                    os.remove(path)

        response_textbox = find_element_safely(
            By.ID, 'audio-response', self.driver, self.config.default_element_waiting
        )
        if response_textbox is None:
            return False

        selenium_human_type(recognized_text, response_textbox)

        second_verify_button = find_element_safely(
            By.ID,
            'recaptcha-verify-button',
            self.driver,
            timeout=5,
        )
        if second_verify_button is None:
            return False

        return complex_click(second_verify_button, self.driver)
