# Selenium Captcha Processing

A Python package for detecting and solving captchas in Selenium-based web automation. It supports identifying various
captcha types, including reCAPTCHA, Cloudflare Turnstile, GeeTest, KeyCaptcha, Lemin Captcha, MTCaptcha, and unknown
image-based captchas. Currently, solvers are implemented for reCAPTCHA and Cloudflare Turnstile, with community
contributions welcome to expand solver support.

## Features

- **Captcha Detection**: Identifies multiple captcha types using detectors.
- **Captcha Solving**: Includes solvers for reCAPTCHA and Cloudflare Turnstile.
- **Speech Recognition**: Uses Google Speech API for audio-based captchas (requires FFmpeg).
- **Extensible Design**: Easily extendable with new detectors and solvers via a modular architecture.
- **Community-Driven**: Actively seeking contributions for additional captcha solvers.

## Installation

Install the package via pip:

```bash
pip install selenium-captcha-processing
```

### Prerequisites

- **Python**: Version 3.10 or higher.
- **FFmpeg**: Required for audio processing with `pydub`. Ensure FFmpeg is installed and added to your system's PATH.
  For installation instructions, see [FFmpeg's official site](https://ffmpeg.org/download.html). Example for Ubuntu:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
  For Windows or macOS, download FFmpeg and add it to your PATH as described in your OS documentation.

### Dependencies

The package requires the following Python libraries, which are automatically installed:

- `speechrecognition>=3.14.3,<4.0.0`
- `requests>=2.32.4,<3.0.0`
- `selenium>=4.33.0,<5.0.0`
- `pydub>=0.25.1,<0.26.0`

## Usage

Below is an example of how to use `selenium-captcha-processing` to detect and attempt to bypass captchas on various
websites. The example uses a Selenium WebDriver to navigate to demo pages and applies the `BypassCaptcha` class.

```python
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium_captcha_processing import BypassCaptcha

# Initialize Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run in headless mode (optional)
driver = WebDriver(service=Service(), options=options)

# List of URLs to test (including demo captchas and a non-captcha page)
urls = [
    "https://www.google.com/recaptcha/api2/demo",
    "https://2captcha.com/demo/cloudflare-turnstile",
    "https://2captcha.com/demo/cloudflare-turnstile-challenge",
    "https://2captcha.com/demo/normal",
    "https://2captcha.com/demo/keycaptcha",
    "https://2captcha.com/demo/lemin",
    "https://2captcha.com/demo/text",
    "https://2captcha.com/demo/mtcaptcha",
    "https://en.wikipedia.org/wiki/Entropy_(information_theory)",
]

# Initialize captcha bypasser
bypassing = BypassCaptcha(driver)

try:
    for url in urls:
        print(f"Navigating to: {url}")
        driver.get(url)

        # Wait for page to load
        sleep(10)

        try:
            # Attempt to bypass captcha
            result = bypassing.bypass()
            print(f"Captcha bypassed: {result}")
        except Exception as e:
            print(f"Error processing captcha at {url}: {str(e)}")

        # Wait before moving to the next URL
        sleep(5)

        print("-------------------------------------------")

finally:
    # Clean up
    if driver:
        driver.quit()
```

### Notes

- **Supported Captchas**: The package can detect reCAPTCHA, Cloudflare Turnstile, GeeTest, KeyCaptcha, Lemin Captcha,
  MTCaptcha, and unknown image captchas. Solvers are currently available for reCAPTCHA and Cloudflare Turnstile only.
- **Exceptions**: Be prepared to handle exceptions, as Selenium or utility functions (e.g., speech recognition) may fail
  due to network issues, missing elements, or invalid API responses. Wrap calls in try-except blocks as shown above.
- **FFmpeg**: Audio captcha solving requires FFmpeg for `pydub` to process audio files. Ensure it's installed and in
  your PATH.
- **Google API**: Audio captcha solving uses the Google Speech API, which requires a valid API key configured in
  `Config`.

## Community Contributions

This project supports a limited set of captcha solvers, and **community contributions are crucial** for expanding
support to other captcha types (e.g., GeeTest, KeyCaptcha, Lemin Captcha, MTCaptcha). We warmly welcome pull requests
and contributions! To contribute:

1. Fork the
   repository: [https://github.com/FINWAX/selenium-captcha-processing.py](https://github.com/FINWAX/selenium-captcha-processing.py)
2. Create a new branch for your feature or bug fix.
3. Implement a new detector or solver in the `detectors` or `solvers` directory, following the interfaces in
   `detectors/interfaces/detector.py` or `solvers/interfaces/solver.py`.
4. Submit a pull request with a clear description of your changes.


## Acknowledgments

This project builds upon ideas and code from the following repositories:

- [selenium-recaptcha-solver](https://github.com/thicccat688/selenium-recaptcha-solver): For reCAPTCHA solving
  techniques.
- [speech_recognition](https://github.com/Uberi/speech_recognition): For audio processing and Google Speech API
  integration.

## Issues and Support

Encounter a bug or have a feature request? Please open an issue
at [https://github.com/FINWAX/selenium-captcha-processing.py/issues](https://github.com/FINWAX/selenium-captcha-processing.py/issues).

## License

This project is licensed under the MIT License. See
the [LICENSE](https://github.com/FINWAX/selenium-captcha-processing.py/blob/main/LICENSE) file for details.