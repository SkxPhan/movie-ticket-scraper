from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement


def get_driver(headless: bool = False) -> Chrome:
    """Launches a Chrome web browser.

    Args:
        headless (bool, optional): Whether to run the browser in headless mode.
                                   Defaults to False.

    Returns:
        WebDriver: A web browser object representing the Chrome browser.
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Not always working with JS
    return Chrome(options=chrome_options)


def dismiss_cookie_popup(driver: Chrome) -> None:
    """Dismisses the privacy cookie popup.

    Args:
        driver (WebDriver): The web browser object.

    Raises:
        TimeoutException: If the cookie popup is not found or not clickable.
    """
    try:
        wait = WebDriverWait(driver, 10)
        cookie_popup = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-close-btn-container"))
        )
        cookie_popup.find_element(
            By.XPATH, "//button[contains(text(), 'Continuer sans accepter')]"
        ).click()
    except TimeoutException:
        print("No cookie popup found or it's not clickable.")


def get_cinema_dropdown(driver: Chrome) -> WebElement:
    """Returns the cinema selection dropdown.

    Args:
        driver (WebDriver): The web browser object.

    Returns:
        WebElement: The dropdown element with the cinema options.
    """
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cinema_filters"))
    )


def get_dates_dropdown(driver: Chrome) -> WebElement:
    """Returns the date selection dropdown.

    Args:
        driver (WebDriver): The web browser object.

    Returns:
        WebElement: The dropdown element with the date options.
    """
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dates_filter"))
    )


def select_dropdown_option(dropdown_element: WebElement, option_value: str) -> None:
    """Selects the value inside a dropdown.

    Args:
        dropdown_element (WebElement): The selected dropdown element.
        option_value (str): The option we want to select.
    """
    select = Select(dropdown_element)
    select.select_by_value(option_value)


def check_tickets_availability(driver: Chrome, expected_hall: str) -> bool:
    """Checks if tickets are available for the expected hall (e.g., "Imax").

    Args:
        driver (WebDriver): The web browser object.
        expected_hall (str): The expected hall name to check availability.

    Returns:
        bool: True if tickets are available for the expected hall, else False.
    """
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{expected_hall}')]")
            )
        )
        showtimes_wrapper_div = driver.find_element(
            By.XPATH, "//div[@class='showtimes-wrapper']"
        )
        return expected_hall in showtimes_wrapper_div.text
    except TimeoutException:
        return False
