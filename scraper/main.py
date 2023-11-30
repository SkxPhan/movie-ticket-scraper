import os
import logging
import configparser

import slack_utils
import web_scraping


logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Create a file handler for the error log file
error_log_handler = logging.FileHandler("scraper_error.log")
error_log_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_log_handler.setFormatter(error_formatter)
logging.getLogger().addHandler(error_log_handler)


def read_config():
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), "config.ini")
    config.read(config_file)

    if "General" not in config:
        raise ValueError("Config file does not contain the 'General' section.")

    general_section = config["General"]
    movie = general_section.get("MOVIE_URL")
    expected_cinema = general_section.get("EXPECTED_CINEMA")
    expected_date = general_section.get("EXPECTED_DATE")
    expected_hall = general_section.get("EXPECTED_HALL")
    slack_webhook_url = general_section.get("SLACK_WEBHOOK_URL")

    if not all(
        [movie, expected_cinema, expected_date, expected_hall, slack_webhook_url]
    ):
        raise ValueError("Config file missing one or more required values.")

    return movie, expected_cinema, expected_date, expected_hall, slack_webhook_url


def main():
    (
        movie,
        expected_cinema,
        expected_date,
        expected_hall,
        slack_webhook_url,
    ) = read_config()

    driver = web_scraping.get_driver(headless=False)
    driver.get(movie)  # Should raise an error if bad inputs

    web_scraping.dismiss_cookie_popup(driver)

    cinema_dropdown = web_scraping.get_cinema_dropdown(driver)
    dates_dropdown = web_scraping.get_dates_dropdown(driver)

    # Should raise an error if bad inputs
    web_scraping.select_dropdown_option(cinema_dropdown, expected_cinema)
    web_scraping.select_dropdown_option(dates_dropdown, expected_date)

    if web_scraping.check_tickets_availability(driver, expected_hall):
        message = "Tickets are available!!! :)"
        slack_utils.send_slack_message(slack_webhook_url, message)
    else:
        message = "Tickets not available :("

    logging.info(message)

    driver.quit()


if __name__ == "__main__":
    main()
