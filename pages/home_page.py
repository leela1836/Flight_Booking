from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.featured_flights = (By.XPATH, "//strong[text()='Lahore']")

    def select_first_flight(self):
        # Wait until element is visible & clickable
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.featured_flights)
        )
        # Scroll and click with JavaScript to avoid interception
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("arguments[0].click();", element)
