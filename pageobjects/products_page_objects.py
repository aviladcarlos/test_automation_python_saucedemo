from selenium.webdriver.common.by import By

from pageobjects.cart_page_objects import CartPageObjects


class ProductsPageObjects:

    pagetitle = (By.CSS_SELECTOR, ".title")
    productlist = (By.CSS_SELECTOR, ".inventory_item")
    # Chains with productlist:
    productlist_name = (By.CLASS_NAME, "inventory_item_name")
    productlist_image = (By.CSS_SELECTOR, "img")
    productlist_price = (By.CLASS_NAME, "inventory_item_price")
    productlist_btn_addtocard = (By.CSS_SELECTOR, "button")
    shoppingcartlink = (By.CLASS_NAME, "shopping_cart_link")


    def __init__(self, driver):
        self.driver = driver

    def page_title(self):
        return self.driver.find_element(*ProductsPageObjects.pagetitle)

    def product_list(self):
        return self.driver.find_elements(*ProductsPageObjects.productlist)

    def shopping_cart_link(self):
        self.driver.find_element(*ProductsPageObjects.shoppingcartlink).click()
        return CartPageObjects(self.driver)
