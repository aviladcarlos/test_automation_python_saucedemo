import pytest

from pageobjects.login_page_objects import LoginPageObjects
from testdata.login_page_data import LoginPageData
from testdata.products_page_data import ProductsPageData
from utilities.baseclass import BaseClass


class TestProductsVerifyProductsListed(BaseClass):

    def test_products_verifyproductslisted(self, login_page_data):

        log = self.get_logger()
        login_page = LoginPageObjects(self.driver)

        log.info(f"Entering '{login_page_data["username"]}' for username")
        login_page.username_field().send_keys(login_page_data["username"])

        log.info(f"Entering password for '{login_page_data["username"]}'")
        login_page.password_field().send_keys(login_page_data["password"])

        log.info("Clicking 'Login' btn")
        products_page = login_page.login_btn()

        # Verifying user has successfully logged in by checking if they have landed on the Products page.
        assert "Products" in products_page.page_title().text, log.critical(
            "Test failed: user did not login successfully")
        log.info("User logged in successfully")

        products = products_page.product_list()
        purchase = "Sauce Labs Backpack"

        for product in products:

            product_name = product.find_element(*products_page.productlist_name).text
            product_btn_addtocard = product.find_element(*products_page.productlist_btn_addtocard)

            if purchase == product_name:
                log.info(f"Adding {product_name} to cart")
                product_btn_addtocard.click()
                break

        log.info("Navigating to cart page")
        cart_page = products_page.shopping_cart_link()

        cart_items = cart_page.cart_items()
        cart_items_names = [item.find_element(*cart_page.cartitems_name).text for item in cart_items]

        # Verify the cart is not empty.
        assert cart_items, log.critical("Test failed: Cart is empty")

        # Verify only 1 item is listed in the cart
        assert len(cart_items) < 2, log.critical("Test failed: More than 1 item was added to cart")

        # Verify if specified item was added to cart
        assert purchase in cart_items_names, log.critical(
            f"Test failed: '{purchase}' was not added to cart")

        # Verify quantity of specified item is not more than 1
        assert 2 > int(cart_items[0].find_element(*cart_page.cartitems_quantity).text), log.critical(
            f"Test failed: Quantity of '{purchase}' added to cart was more than 1"
        )

        # Verify quantity of specified item is not 0
        assert 0 != int(cart_items[0].find_element(*cart_page.cartitems_quantity).text), log.critical(
            f"Test failed: Quantity of '{purchase}' added to cart is 0"
        )

        log.info("Clicking 'Checkout' button")
        check_out_step_one_page = cart_page.checkout_btn()

        log.info(f"Entering '{login_page_data["first name"]}' for first name")
        check_out_step_one_page.first_name_field().send_keys(login_page_data["first name"])

        log.info(f"Entering '{login_page_data["last name"]}' for last name")
        check_out_step_one_page.last_name_field().send_keys(login_page_data["last name"])

        log.info(f"Entering '{login_page_data["zip code"]}' for zip/postal code")
        check_out_step_one_page.zip_postal_code_field().send_keys(login_page_data["zip code"])

        log.info("Clicking 'Continue' button")

        check_out_step_two_page = check_out_step_one_page.continue_btn()
        checkout_overview_cart_items = check_out_step_two_page.cart_items()

        checkout_overview_cart_items_names = [
            item.find_element(*check_out_step_two_page.cartitems_name).text for item in checkout_overview_cart_items]

        # Verify the overview cart is not empty.
        assert checkout_overview_cart_items, log.critical("Test failed: Overview cart is empty")

        # Verify only 1 item is listed in the overview cart
        assert len(checkout_overview_cart_items) < 2, log.critical("Test failed: "
                                                                   "More than 1 item is displayed in overview cart")

        # Verify if specified item is displayed in overview cart
        assert purchase in checkout_overview_cart_items_names, log.critical(
            f"Test failed: '{purchase}' is not displayed in overview cart")

        # Verify quantity of specified item is not more than 1
        assert 2 > int(checkout_overview_cart_items[0].find_element(*check_out_step_two_page.cartitems_quantity).text), log.critical(
            f"Test failed: Quantity of '{purchase}' displayed in overview cart was more than 1"
        )

        # Verify quantity of specified item is not 0
        assert 0 != int(checkout_overview_cart_items[0].find_element(*check_out_step_two_page.cartitems_quantity).text), log.critical(
            f"Test failed: Quantity of '{purchase}' displayed in overview cart is 0"
        )

        log.info("Clicking 'Finish' button")

        check_out_complete_page = check_out_step_two_page.finish_btn()

        # Verify order completed successfully by checking if [think of something to write]
        assert "Thank you for your order!" == check_out_complete_page.complete_header().text, log.critical(
            "Test failed: Order did not fully complete")

        log.info(f"Purchase of '{purchase}' was successful")

    @pytest.fixture(params=LoginPageData.standard_user)
    def login_page_data(self, request):
        return request.param
