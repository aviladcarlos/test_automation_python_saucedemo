from selenium.webdriver.common.by import By

from pageobjects.checkoutstepone_page_objects import CheckoutStepOnePageObjects


class CartPageObjects:

    cartitems = (By.CLASS_NAME, "cart_item")
    # Chains with cartitems:
    cartitems_name = (By.CLASS_NAME, "inventory_item_name")
    cartitems_quantity = (By.CLASS_NAME, "cart_quantity")
    checkoutbtn = (By.ID, "checkout")


    def __init__(self, driver):
        self.driver = driver

    def cart_items(self):
        return self.driver.find_elements(*CartPageObjects.cartitems)

    def checkout_btn(self):
        self.driver.find_element(*CartPageObjects.checkoutbtn).click()
        return CheckoutStepOnePageObjects(self.driver)

