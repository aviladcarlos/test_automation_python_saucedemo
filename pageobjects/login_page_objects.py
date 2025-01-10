from selenium.webdriver.common.by import By

from pageobjects.products_page_objects import ProductsPageObjects


class LoginPageObjects:

    loginlogo = (By.CSS_SELECTOR, ".login_logo")
    usernamefield = (By.ID, "user-name")
    passwordfield = (By.ID, "password")
    loginbtn = (By.ID, "login-button")
    errormsg = (By.CSS_SELECTOR, "[data-test='error']")
    loginbox = (By.CLASS_NAME, "login-box")

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

    def error_msg(self):
        return self.driver.find_element(*LoginPageObjects.errormsg)

    # Using find_element would trigger a 'NoSuchElementException' error which can be handled with a try block. If I use
    # find_elements instead, it returns an empty list and won't trigger an error when no element is found.
    # The empty considered is false when checked, so I can compare against it to determine if the element exists.
    # I decided to use find_elements as it would take fewer lines to check if the element exists compared to using a
    # try block to handle the NoSuchElementException with find_element.
    def login_box(self):
        return self.driver.find_elements(*LoginPageObjects.loginbox)
