from selenium.webdriver.common.by import By


class ProductsPageObjects:

    pagetitle = (By.CSS_SELECTOR, ".title")

    def __init__(self, driver):
        self.driver = driver

    def page_title(self):
        return self.driver.find_element(*ProductsPageObjects.pagetitle)
