import pytest
from datetime import date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.web_scraping import (
    get_driver,
    dismiss_cookie_popup,
    select_dropdown_option,
    check_tickets_availability,
)

# Test data
URL = "https://kinepolis.be/fr/movies/detail/23479/HO00009565/0/oppenheimer"


@pytest.fixture(scope="module")
def driver():
    # Set up the WebDriver instance
    driver = get_driver(headless=False)
    driver.get(URL)
    yield driver
    # Tear down the WebDriver instance after all tests
    driver.quit()


def test_dismiss_cookie_popup(driver):
    """Test dismissing the cookie popup"""
    # Ensure the cookie popup is initially visible
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "onetrust-close-btn-container"))
    )

    # Dismiss the cookie popup
    dismiss_cookie_popup(driver)

    # Assert that the cookie popup is no longer visible
    WebDriverWait(driver, 5).until_not(
        EC.visibility_of_element_located((By.ID, "onetrust-close-btn-container"))
    )

    # The test will pass if the cookie popup is not visible after dismissing it
    assert True


@pytest.mark.parametrize(
    "cinema, date",
    [
        ("KBRU", date.today().strftime("%Y-%m-%d")),
        ("KBRAI", (date.today() + timedelta(weeks=2)).strftime("%Y-%m-%d")),
    ],
)
def test_select_dropdown_option(driver, cinema, date):
    """Test selecting options in the dropdowns"""
    cinema_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cinema_filters"))
    )
    dates_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dates_filter"))
    )

    select_dropdown_option(cinema_dropdown, cinema)
    # Assert that the cinema dropdown has the expected value selected
    assert cinema_dropdown.get_attribute("value") == cinema

    select_dropdown_option(dates_dropdown, date)
    # Assert that the dates dropdown has the expected value selected
    assert dates_dropdown.get_attribute("value") == date


@pytest.mark.parametrize(
    "cinema, date, hall, expected",
    [
        ("KBRU", date.today().strftime("%Y-%m-%d"), "Salle 28", True),
        (
            "KBRU",
            (date.today() + timedelta(weeks=2)).strftime("%Y-%m-%d"),
            "Salle 28",
            False,
        ),
    ],
)
def test_check_tickets_availability(driver, cinema, date, hall, expected):
    """Test availability of tickets for the expected hall"""
    cinema_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cinema_filters"))
    )
    dates_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dates_filter"))
    )
    select_dropdown_option(cinema_dropdown, cinema)
    select_dropdown_option(dates_dropdown, date)

    # Assert that the expected hall has available tickets
    assert check_tickets_availability(driver, hall) is expected
