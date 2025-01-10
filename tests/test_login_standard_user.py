import pytest

from pageobjects.login_page_objects import LoginPageObjects
from testdata.login_page_data import LoginPageData
from utilities.baseclass import BaseClass


class TestLoginStandardUser(BaseClass):

    def test_login_standard_user(self, login_page_data):

        log = self.get_logger()
        login_page = LoginPageObjects(self.driver)

        log.info(f"Entering '{login_page_data["username"]}' for username")
        login_page.username_field().send_keys(login_page_data["username"])

        log.info(f"Entering password for '{login_page_data["username"]}'")
        login_page.password_field().send_keys(login_page_data["password"])

        log.info("Clicking 'Login' btn")
        products_page = login_page.login_btn()

        # Verifying user has successfully logged in by checking if they have landed on the Products page.
        assert "Products" in products_page.page_title().text, log.critical("Test failed: user did not login successfully")
        log.info("User logged in successfully")

    @pytest.fixture(params=LoginPageData.standard_user)
    def login_page_data(self, request):
        return request.param
