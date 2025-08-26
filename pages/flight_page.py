import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FlightPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        # Passenger 1 (primary)
        self.first_name = (By.XPATH, "//input[@id='p-first-name']")
        self.last_name = (By.XPATH, "//input[@id='p-last-name']")
        self.email = (By.XPATH, "//input[@id='p-email']")
        self.phone = (By.XPATH, "//input[@id='p-phone']")
        self.address = (By.XPATH, "//input[@id='p-address']")

        # Traveler (secondary passenger)
        self.t_first_name = (By.XPATH, "//input[@id='t-first-name-1']")
        self.t_last_name = (By.XPATH, "//input[@id='t-last-name-1']")
        self.passport = (By.XPATH, "//input[@name='passport_1']")
        self.t_email = (By.XPATH, "//input[@id='t-email-1']")
        self.t_phone = (By.XPATH, "//input[@id='t-phone-1']")

        # Actions
        self.terms = (By.XPATH, "//input[@id='agreechb']")
        self.confirm_booking = (By.XPATH, "//button[@id='booking']")
        self.select_flight = (By.XPATH, "(//button[contains(normalize-space(text()), 'Select Flight')])[1]")

    def _enter_text(self, locator, value):
        """Helper method: waits, clears, and types into input field."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def fill_passenger_details(self):
        # Click "Select Flight"
        select_btn = self.wait.until(EC.element_to_be_clickable(self.select_flight))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", select_btn)
        select_btn.click()

        # Passenger 1
        self._enter_text(self.first_name, "Leela")
        self._enter_text(self.last_name, "Mohan")
        self._enter_text(self.email, "chemuruleelamohan@gmail.com")
        self._enter_text(self.phone, "9876543210")
        self._enter_text(self.address, "Hyderabad")

        time.sleep(1)  # small buffer

        # Traveler (secondary passenger)
        self._enter_text(self.t_first_name, "Leela")
        self._enter_text(self.t_last_name, "Mohan")
        self._enter_text(self.passport, "A1234567")
        self._enter_text(self.t_email, "chemuruleelamohan@gmail.com")
        self._enter_text(self.t_phone, "9876543210")

        time.sleep(2)

        # Accept terms
        terms_chk = self.wait.until(EC.element_to_be_clickable(self.terms))
        if not terms_chk.is_selected():
            self.driver.execute_script("arguments[0].scrollIntoView(true);", terms_chk)
            try:
                terms_chk.click()
            except:
                # ✅ fallback: JS click (avoids interception)
                self.driver.execute_script("arguments[0].click();", terms_chk)

    def confirm_booking_click(self):
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.confirm_booking))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", confirm_btn)
        try:
            confirm_btn.click()
        except:
            # ✅ fallback: JS click (avoids interception)
            self.driver.execute_script("arguments[0].click();", confirm_btn)

