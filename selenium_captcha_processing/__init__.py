"""
selenium_captcha_processing package.

This package provides tools for detecting and solving various types of captchas in Selenium-based web automation.
It includes detectors for identifying captchas, solvers for bypassing them, and utilities for tasks like speech recognition.
"""

import logging

from .bypassing import BypassCaptcha
from .captcha import Captcha
from .classification import Classify
from .config import Config
from .data import CaptchaNote
from .factory import make_detector_type, make_solver_type, make_default_utils, make_default_config
from .helpers import human_type, js_click, find_element_safely, is_element_absent_or_invisible, download_audio
from .solving import Solve
from .utils.container import Utils
from .utils.recognize_speech_by_google_api import RecognizeSpeechByGoogleApi
from .detectors.interfaces.detector import DetectCaptchaI
from .solvers.interfaces.solver import SolveCaptchaI
from .utils.interfaces.speech_recogniser import SpeechRecogniserI

__version__ = "1.0.0"

__all__ = [
    'BypassCaptcha',
    'Captcha',
    'Classify',
    'Config',
    'CaptchaNote',
    'make_detector_type',
    'make_solver_type',
    'make_default_utils',
    'make_default_config',
    'human_type',
    'js_click',
    'find_element_safely',
    'is_element_absent_or_invisible',
    'download_audio',
    'Solve',
    'Utils',
    'RecognizeSpeechByGoogleApi',
    'DetectCaptchaI',
    'SolveCaptchaI',
    'SpeechRecogniserI',
]

logging.getLogger(__name__).addHandler(logging.NullHandler())