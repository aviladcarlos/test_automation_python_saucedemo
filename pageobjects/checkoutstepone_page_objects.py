from selenium.webdriver.common.by import By

from pageobjects.checkoutsteptwo_page_objects import CheckoutStepTwoPageObjects


class CheckoutStepOnePageObjects:

    firstnamefield = (By.ID, "first-name")
    lastnamefield = (By.ID, "last-name")
    zippostalcodefield = (By.ID, "postal-code")
    continuebtn = (By.ID, "continue")

    def __init__(self, driver):
        self.driver = driver

    def first_name_field(self):
        return self.driver.find_element(*CheckoutStepOnePageObjects.firstnamefield)

    def last_name_field(self):
        return self.driver.find_element(*CheckoutStepOnePageObjects.lastnamefield)

    def zip_postal_code_field(self):
        return self.driver.find_element(*CheckoutStepOnePageObjects.zippostalcodefield)

    def continue_btn(self):
        self.driver.find_element(*CheckoutStepOnePageObjects.continuebtn).click()
        return CheckoutStepTwoPageObjects(self.driver)
