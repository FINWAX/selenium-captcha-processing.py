import os
import tempfile
import uuid
from time import sleep

from pydub import AudioSegment
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_captcha_processing.config import Config
from selenium_captcha_processing.helpers import find_element_safely, js_click, human_type, download_audio
from selenium_captcha_processing.solvers.interfaces.solver import SolveCaptchaI
from selenium_captcha_processing.utils.container import Utils


class SolveReCaptcha(SolveCaptchaI):
    def __init__(self, driver: WebDriver, utils: Utils, config: Config, *args, **kwargs):
        self.config = config
        self.utils = utils
        self.driver = driver

    def solve(self) -> bool:
        recaptcha_iframe = find_element_safely(
            self.driver, By.XPATH, '//iframe[@title="reCAPTCHA"]',
            self.config.default_element_waiting
        )
        if recaptcha_iframe is None:
            return False

        self.driver.switch_to.frame(recaptcha_iframe)

        checkbox = find_element_safely(
            self.driver, By.ID, 'recaptcha-anchor',
            self.config.default_element_waiting
        )
        if checkbox is None:
            self.driver.switch_to.parent_frame()
            return False

        js_click(self.driver, checkbox)
        sleep(0.5)
        if checkbox.get_attribute('aria-checked') == 'true':
            self.driver.switch_to.parent_frame()
            return True

        self.driver.switch_to.parent_frame()

        return self._solve_challenge()

    def _solve_challenge(self):
        captcha_challenge = find_element_safely(
            self.driver,
            By.XPATH,
            '//iframe[contains(@src, "recaptcha") and contains(@src, "bframe")]',
            timeout=5,
        )

        if not captcha_challenge:
            return False

        self.driver.switch_to.frame(captcha_challenge)

        audio_btn = find_element_safely(
            self.driver,
            By.XPATH,
            '//*[@id="recaptcha-audio-button"]',
            timeout=1.5,
        )
        if audio_btn is None:
            return False

        audio_btn.click()

        download_link = find_element_safely(
            self.driver,
            By.CLASS_NAME,
            'rc-audiochallenge-tdownload-link',
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
            self.driver, By.ID, 'audio-response', self.config.default_element_waiting
        )
        if response_textbox is None:
            return False

        human_type(element=response_textbox, text=recognized_text)

        second_verify_button = find_element_safely(
            self.driver,
            By.ID,
            'recaptcha-verify-button',
            timeout=5,
        )
        if second_verify_button is None:
            return False

        js_click(self.driver, second_verify_button)

        return True
