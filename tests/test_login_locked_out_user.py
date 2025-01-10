import time

import pytest

from pageobjects.login_page_objects import LoginPageObjects
from testdata.login_page_data import LoginPageData
from utilities.baseclass import BaseClass


class TestLoginLockedOutUser(BaseClass):

    def test_login_standard_user(self, login_page_data):

        log = self.get_logger()
        login_page = LoginPageObjects(self.driver)

        log.info(f"Entering '{login_page_data["username"]}' for username")
        login_page.username_field().send_keys(login_page_data["username"])

        log.info(f"Entering password for '{login_page_data["username"]}'")
        login_page.password_field().send_keys(login_page_data["password"])

        log.info("Clicking 'Login' btn")
        login_page.login_btn()

        # Verifying locked out message is displayed when user attempts to login with a locked out user.
        assert "user has been locked out" in login_page.error_msg().text, log.critical("Test failed: user locked out "
                                                                                       "message did not display")
        log.info("User locked out message displayed successfully")

        # Verifying that user remains on login page after locked out message is displayed by checking if login
        # box still exists.
        assert login_page.login_box(), log.critical("Test failed: user did not remain on login page after "
                                                    "locked out message")
        log.info("User remains on login page after locked out message")


    @pytest.fixture(params=LoginPageData.locked_out_user)
    def login_page_data(self, request):
        return request.param
