from selenium.webdriver.common.by import By

from pageobjects.products_page_objects import ProductsPageObjects

class LoginPageObjects:

    loginlogo = (By.CSS_SELECTOR, ".login_logo")
    usernamefield = (By.ID, "user-name")
    passwordfield = (By.ID, "password")
    loginbtn = (By.ID, "login-button")

    def __init__(self, driver):
        self.driver = driver

    def login_logo(self):
        return self.driver.find_element(*LoginPageObjects.loginlogo)

    def username_field(self):
        return self.driver.find_element(*LoginPageObjects.usernamefield)

    def password_field(self):
        return self.driver.find_element(*LoginPageObjects.passwordfield)

    def login_btn(self):
        self.driver.find_element(*LoginPageObjects.loginbtn).click()
        return ProductsPageObjects(self.driver)

