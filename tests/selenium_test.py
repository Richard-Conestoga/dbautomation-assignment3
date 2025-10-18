import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

BASE_URL = "http://localhost:5000"  # Flask app must be running locally

@pytest.fixture(scope="module")
def driver():
    """Set up Selenium WebDriver (Chrome in headless mode)."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_positive_search_returns_results(driver):
    """Positive test: valid search returns results."""
    driver.get(BASE_URL)
    # Fill out valid filters
    borough_box = driver.find_element(By.NAME, "borough")
    borough_box.clear()
    borough_box.send_keys("MANHATTAN")

    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)

    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    assert len(rows) > 1, "Expected table rows with data but found none."


def test_negative_invalid_filter_returns_no_results(driver):
    """Negative test: nonsense filters should return 0 results."""
    driver.get(BASE_URL)
    borough_box = driver.find_element(By.NAME, "borough")
    borough_box.clear()
    borough_box.send_keys("INVALIDBOROUGHXYZ")

    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)

    page_source = driver.page_source.lower()
    assert "0 results found" in page_source or "results found" in page_source, \
        "Expected 0 results message, not found."


def test_aggregate_page_loads(driver):
    """Aggregate test: verifies complaints per borough page loads and contains table."""
    driver.get(f"{BASE_URL}/aggregate")
    time.sleep(1)
    heading = driver.find_element(By.TAG_NAME, "h2").text
    assert "Complaints per Borough" in heading
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    assert len(rows) > 1, "Aggregate table did not display any rows."

