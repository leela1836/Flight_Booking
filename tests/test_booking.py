import time
import pytest
from pages.home_page import HomePage
from pages.flight_page import FlightPage
from pages.Payments_page import PaymentPage
import os


# -----------------------
# Helper: Save Screenshot
# -----------------------
def save_screenshot(driver, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)   # create folder if not exists
    driver.save_screenshot(path)


# -----------------------
# Test: Flight Booking Flow
# -----------------------
@pytest.mark.order(1)   # keep only if pytest-order plugin is installed
def test_flight_booking(driver):
    driver.get("https://phptravels.net/")

    # Step 1: Select Flight
    home = HomePage(driver)
    home.select_first_flight()
    time.sleep(3)
    save_screenshot(driver, "reports/screenshots/flight_selected.png")
    assert "flights" in driver.current_url.lower()

    # Step 2: Fill Passenger Form
    flight = FlightPage(driver)
    flight.fill_passenger_details()
    save_screenshot(driver, "reports/screenshots/form_filled.png")

    # ✅ Verify passenger details are filled
    first_name_input = driver.find_element("id", "p-first-name")
    assert first_name_input.get_attribute("value") != "", "First Name field not filled!"

    # Step 3: Confirm Booking
    flight.confirm_booking_click()
    time.sleep(5)
    save_screenshot(driver, "reports/screenshots/booking_confirmed.png")
    assert "Booking" in driver.page_source or "checkout" in driver.current_url.lower()

    # Step 4: Pay with PayPal
    payment = PaymentPage(driver)
    payment.pay_with_paypal()
    time.sleep(5)
    save_screenshot(driver, "reports/screenshots/payment_done.png")
    assert "Payment" in driver.page_source or "paypal" in driver.current_url.lower()
