from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class PaymentPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        # Locators
        self.proceed = (By.XPATH, "//input[@id='form']")
        self.paypal = (By.XPATH, "//div[contains(@class, 'paypal-button')]")
        self.paypal_email = (By.XPATH, "//input[@id='email']")
        self.emailbtn = (By.XPATH, "//button[@name='btnNext']")
        self.paypal_password = (By.XPATH, "//input[@id='password']")
        self.login_button = (By.XPATH, "//button[@id='btnLogin']")
        self.payments = (By.XPATH, "//button[@data-id='payment-submit-btn']")

    def pay_with_paypal(self):
        # Step 1: Click proceed
        proceed_btn = self.wait.until(EC.element_to_be_clickable(self.proceed))
        proceed_btn.click()

        # Step 2: Try locating PayPal button (main page or iframes)
        paypal_btn = None
        try:
            paypal_btn = self.wait.until(EC.element_to_be_clickable(self.paypal))
        except TimeoutException:
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for i, iframe in enumerate(iframes):
                self.driver.switch_to.frame(iframe)
                try:
                    paypal_btn = self.wait.until(EC.element_to_be_clickable(self.paypal))
                    print(f"✅ Found PayPal button inside iframe {i}")
                    break
                except TimeoutException:
                    self.driver.switch_to.default_content()
                    continue

        if not paypal_btn:
            raise NoSuchElementException("❌ PayPal button not found in main page or iframes.")

        # Step 3: Click PayPal button
        paypal_btn.click()
        self.driver.switch_to.default_content()

        # Step 4: Switch to PayPal popup window
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Step 5: Login flow
        email_input = self.wait.until(EC.visibility_of_element_located(self.paypal_email))
        email_input.send_keys("sb-itxir5994130@personal.example.com")

        next_btn = self.wait.until(EC.element_to_be_clickable(self.emailbtn))
        next_btn.click()

        password_input = self.wait.until(EC.visibility_of_element_located(self.paypal_password))
        password_input.send_keys("testpayment")

        login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
        login_btn.click()

        # ✅ Step 6: Handle "change password" popup
        try:
            # Case 1: JavaScript Alert
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print("⚠️ Alert detected: ", alert.text)
            alert.dismiss()  # or alert.accept()
            print("✅ Alert dismissed successfully")
        except TimeoutException:
            print("ℹ️ No JS alert found, checking for iframe popup...")
            # Case 2: HTML modal in iframe
            try:
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                for i, iframe in enumerate(iframes):
                    self.driver.switch_to.frame(iframe)
                    try:
                        # Try to close popup with JS
                        self.driver.execute_script(
                            "document.querySelector('div[class*=\"popup\"], div[class*=\"modal\"]')?.remove();"
                        )
                        print(f"✅ Password change popup bypassed in iframe {i}")
                        break
                    finally:
                        self.driver.switch_to.default_content()
            except Exception as e:
                print("❌ Could not handle password change popup:", str(e))

        # Step 7: Final payment submit
        pay_btn = self.wait.until(EC.element_to_be_clickable(self.payments))
        pay_btn.click()
