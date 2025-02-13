from selenium.webdriver.common.by import By


class CheckoutCompletePageObjects:

    completeheader = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver

    def complete_header(self):
        return self.driver.find_element(*CheckoutCompletePageObjects.completeheader)
