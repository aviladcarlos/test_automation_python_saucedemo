from selenium.webdriver.common.by import By

from pageobjects.checkoutcomplete_page_objects import CheckoutCompletePageObjects


class CheckoutStepTwoPageObjects:

    cartitems = (By.CLASS_NAME, "cart_item")
    # Chains with cartitems:
    cartitems_name = (By.CLASS_NAME, "inventory_item_name")
    cartitems_quantity = (By.CLASS_NAME, "cart_quantity")

    finishbtn = (By.ID, "finish")

    def __init__(self, driver):
        self.driver = driver

    def cart_items(self):
        return self.driver.find_elements(*CheckoutStepTwoPageObjects.cartitems)

    def finish_btn(self):
        self.driver.find_element(*CheckoutStepTwoPageObjects.finishbtn).click()
        return CheckoutCompletePageObjects(self.driver)

