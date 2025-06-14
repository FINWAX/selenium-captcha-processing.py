import base64
import random
import time

import requests
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

def human_type(element: WebElement, text: str) -> None:
    """
    Simulate human-like typing into a web element.
    :param element: The web element to type into.
    :param text: The text to type.
    """
    for c in text:
        element.send_keys(c)
        time.sleep(random.uniform(0.05, 0.1))

def js_click(driver, element: WebElement) -> None:
    """
    Perform a JavaScript click on a web element.
    :param driver: The Selenium WebDriver instance.
    :param element: The web element to click.
    """
    driver.execute_script('arguments[0].click();', element)

def find_element_safely(driver, by, value, timeout=0.01):
    """
    Safely find an element on the page with a short timeout.
    :param driver: The Selenium WebDriver instance.
    :param by: The method used to locate the element (e.g., By.ID, By.XPATH).
    :param value: The value for the locator.
    :param timeout: The maximum time to wait for the element, defaults to 0.01 seconds.
    :return: The found web element or None if not found.
    """
    try:
        return WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located((by, value))
        )
    except TimeoutException:
        return None

def is_element_absent_or_invisible(driver, by, value, timeout=10):
    """
    Check if an element is absent or invisible on the page.
    :param driver: The Selenium WebDriver instance.
    :param by: The method used to locate the element (e.g., By.ID, By.XPATH).
    :param value: The value for the locator.
    :param timeout: The maximum time to wait for the element to become invisible, defaults to 10 seconds.
    :return: True if the element is absent or invisible, False otherwise.
    """
    try:
        element = driver.find_element(by, value)
        if not element.is_displayed():
            return True
        WebDriverWait(driver, timeout).until(
            expected_conditions.invisibility_of_element_located((by, value))
        )
        return True
    except NoSuchElementException:
        return True
    except TimeoutException:
        return False

def download_audio(link_or_data, mp3_file):
    """
    Download audio content from a link or data URI and save it to a file.
    :param link_or_data: The URL or data URI of the audio content.
    :param mp3_file: The file path to save the audio content.
    """
    if link_or_data.startswith("data:audio"):
        base64_data = link_or_data.split(",")[1]
        audio_content = base64.b64decode(base64_data)
    else:
        audio_download = requests.get(url=link_or_data, allow_redirects=True)
        audio_content = audio_download.content

    with open(mp3_file, 'wb') as f:
        f.write(audio_content)
        f.close()