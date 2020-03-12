from io import BytesIO
from typing import List, Union

import allure
from PIL import Image
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.browser.common_selectors import Selector, SelectorsEnum


def convert_png_to_jpg(screenshot_png: bytes) -> bytes:
    raw_image = Image.open(BytesIO(screenshot_png))
    image = raw_image.convert('RGB')
    with BytesIO() as f:
        image.save(f, format='JPEG', quality=90)
        return f.getvalue()


def attach_jpg_screenshot(
        browser: WebDriver, page_name: str, *,
        selector: Union[Selector, SelectorsEnum] = None
):
    if selector:
        element = find_element(browser, selector)
        screenshot_png = element.screenshot_as_png
    else:
        screenshot_png = browser.get_screenshot_as_png()
    screenshot_jpg = convert_png_to_jpg(screenshot_png)
    allure.attach(
        screenshot_jpg,
        name=page_name,
        attachment_type=allure.attachment_type.JPG,
        extension='jpg'
    )


def is_element_present(browser: WebDriver, selector: Selector) -> bool:
    """Check if sought element is present (doesn't have to be visible).

    If selector returns more than 1 element then find_element() will return the first
    element from the list.
    """
    is_present = True
    try:
        browser.find_element(by=selector.by, value=selector.selector)
    except NoSuchElementException:
        is_present = False
    return is_present


def is_element_visible(browser: WebDriver, selector: Selector) -> bool:
    """Check if sought element is visible.

    If element is not present it will also return False.
    """
    try:
        is_visible = browser.find_element(
            by=selector.by, value=selector.selector
        ).is_displayed()
    except NoSuchElementException:
        is_visible = False
    return is_visible


def find_element(browser: WebDriver, selector: Selector) -> WebElement:
    return browser.find_element(selector.by, selector.selector)


def find_elements(browser: WebElement, selector: Selector) -> List[WebElement]:
    return browser.find_elements(selector.by, selector.selector)


def wait_for_element_visibility(
        driver: WebDriver, selector: Selector, *, time_to_wait: int = 3
):
    """Wait until element is visible."""
    locator = (selector.by, selector.selector)
    WebDriverWait(driver, time_to_wait).until(
        expected_conditions.visibility_of_element_located(locator)
    )


@allure.step('Should see all elements from: {selectors_enum}')
def should_see_all_elements(browser, selectors_enum):
    for selector in selectors_enum:
        if not selector.is_visible:
            continue
        error = f'Expected element "{selector}" is not visible'
        if not is_element_visible(browser, selector):
            attach_jpg_screenshot(browser, error)
        assert is_element_visible(browser, selector), error


@allure.step('Should not see elements from: {selectors_enum}')
def should_not_see(browser, selectors_enum):
    for selector in selectors_enum:
        if not selector.is_visible:
            continue
        assertion_error = f'Unexpected element is visible "{selector}"'
        try:
            assert not is_element_visible(browser, selector), assertion_error
        except AssertionError:
            attach_jpg_screenshot(browser, assertion_error)
            raise
        except StaleElementReferenceException:
            attach_jpg_screenshot(browser, 'StaleElementReferenceException')
            raise


@allure.step('Should not see errors')
def should_not_see_errors(browser):
    assertion_error = ''
    page_source = browser.page_source
    try:
        assertion_error = f'500 ISE on {browser.current_url}'
        assert 'there is a problem with the service' not in page_source, assertion_error
        assert 'Internal Server Error' not in page_source, assertion_error
    except AssertionError:
        attach_jpg_screenshot(browser, assertion_error)
        raise
