import pytest

from pageobjects.login_page_objects import LoginPageObjects
from testdata.login_page_data import LoginPageData
from testdata.products_page_data import ProductsPageData
from utilities.baseclass import BaseClass


class TestE2EFewItemsPurchase(BaseClass):

    def test_e2e_few_items_purchase(self, login_page_data):

        log = self.get_logger()
        login_page = LoginPageObjects(self.driver)

        log.info(f'Entering "{login_page_data["username"]}" for username')
        login_page.username_field().send_keys(login_page_data["username"])

        log.info(f'Entering password for "{login_page_data["username"]}"')
        login_page.password_field().send_keys(login_page_data["password"])

        log.info('Clicking "Login" btn')
        products_page = login_page.login_btn()

        # Verifying user has successfully logged in by checking if they have landed on the Products page.
        assert "Products" in products_page.page_title().text, log.critical(
            "Test failed: user did not login successfully")

        log.info("User logged in successfully")

        products = products_page.product_list()
        purchase = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie"]

        for product in products:

            product_name = product.find_element(*products_page.productlist_name).text
            product_btn_addtocard = product.find_element(*products_page.productlist_btn_addtocard)

            if product_name in purchase:
                log.info(f'Adding "{product_name}" to cart')
                product_btn_addtocard.click()

        log.info("Navigating to cart page")
        cart_page = products_page.shopping_cart_link()

        cart_items = cart_page.cart_items()
        cart_items_names = [item.find_element(*cart_page.cartitems_name).text for item in cart_items]

        # Verify the cart is not empty.
        assert cart_items, log.critical("Test failed: Cart is empty")

        # Verify the cart has the same amount of items as the expected purchase list
        assert len(cart_items) == len(purchase), log.critical(
            f"Test failed: {len(cart_items)} items are in cart, {len(purchase)} items are expected")

        # Verify if specified item was added to cart
        for item in purchase:
            assert item in cart_items_names, log.critical(
                f'Test failed: "{item}" was not added to cart')

        # Verify quantity of each specified item in purchase list is not more than 1
        for item in cart_items:
            assert 2 > int(item.find_element(*cart_page.cartitems_quantity).text), log.critical(
                f'Test failed: Quantity of "{item.find_element(*cart_page.cartitems_name).text}"'
                f" added to cart was more than 1")

        # Verify quantity of specified item is not 0
        for item in cart_items:
            assert 0 != int(item.find_element(*cart_page.cartitems_quantity).text), log.critical(
                f'Test failed: Quantity of "{item.find_element(*cart_page.cartitems_name).text}" added to cart is 0')

        log.info("Clicking 'Checkout' button")
        check_out_step_one_page = cart_page.checkout_btn()

        log.info(f'Entering "{login_page_data["first name"]}" for first name')
        check_out_step_one_page.first_name_field().send_keys(login_page_data["first name"])

        log.info(f'Entering "{login_page_data["last name"]}" for last name')
        check_out_step_one_page.last_name_field().send_keys(login_page_data["last name"])

        log.info(f'Entering "{login_page_data["zip code"]}" for zip/postal code')
        check_out_step_one_page.zip_postal_code_field().send_keys(login_page_data["zip code"])

        log.info('Clicking "Continue" button')

        check_out_step_two_page = check_out_step_one_page.continue_btn()

        checkout_overview_cart_items = check_out_step_two_page.cart_items()
        checkout_overview_cart_items_names = [
            item.find_element(*check_out_step_two_page.cartitems_name).text for item in checkout_overview_cart_items]

        # Verify the overview cart is not empty.
        assert checkout_overview_cart_items, log.critical("Test failed: Overview cart is empty")

        # Verify the overview cart has the same amount of items as the expected purchase list
        assert len(checkout_overview_cart_items) == len(purchase), log.critical(
            f"Test failed: {len(checkout_overview_cart_items)} items displayed in overview cart, "
            f"{len(purchase)} items are expected")

        # Verify if specified item is displayed in overview cart
        for item in purchase:
            assert item in checkout_overview_cart_items_names, log.critical(
                f'Test failed: "{item}" is not displayed in overview cart')

        # Verify quantity of specified item is not more than 1
        for item in checkout_overview_cart_items:
            assert 2 > int(item.find_element(*check_out_step_two_page.cartitems_quantity).text), log.critical(
                f'Test failed: Quantity of "{item.find_element(*check_out_step_two_page.cartitems_name).text}" '
                f"displayed in overview cart was more than 1")

        # Verify quantity of specified item is not 0
        for item in checkout_overview_cart_items:
            assert 0 != int(item.find_element(*check_out_step_two_page.cartitems_quantity).text), log.critical(
                f'Test failed: Quantity of "{item.find_element(*check_out_step_two_page.cartitems_name).text}" '
                f"displayed in overview cart is 0")

        log.info('Clicking "Finish" button')

        check_out_complete_page = check_out_step_two_page.finish_btn()

        # Verify order completed successfully by checking if [think of something to write]
        assert "Thank you for your order!" == check_out_complete_page.complete_header().text, log.critical(
            "Test failed: Order did not fully complete")

        log.info(f"Purchase of {', '.join(f'"{item}"'for item in purchase)} was successful")

    @pytest.fixture(params=LoginPageData.standard_user)
    def login_page_data(self, request):
        return request.param
