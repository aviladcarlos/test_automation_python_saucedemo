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
        products_names = [product.find_element(*products_page.productlist_name).text for product in products]
        products_incorrect_cost = []
        products_incorrect_image = []

        # If there is more products on the site than in expected products lists throws a warning that
        # prints the products on the site that are not included in expected products list.
        if len(products) > len(ProductsPageData.expected_products):
            log.warning(f"The following {len(products) - len(ProductsPageData.expected_products)}"
                        f" products on the site are not listed in expected products list:")

            for product in products_names:
                if product not in ProductsPageData.expected_products:
                    log.warning(f"    -{product}")

        # If there is more products in the expected products list than what is listed on the site throws a warning that
        # prints the products on the expected products list that are not included on the site.
        elif len(products) < len(ProductsPageData.expected_products):
            log.warning(f"The following {len(ProductsPageData.expected_products) - len(products)}"
                        f"products in expected products list are not listed on the site:")

            for product in ProductsPageData.expected_products:
                if product not in products_names:
                    log.warning(f"    -{product}")

        for product in products:

            product_name = product.find_element(*products_page.productlist_name).text
            product_image = product.find_element(*products_page.productlist_image).get_attribute("src")
            product_cost = product.find_element(*products_page.productlist_price).text
            expected_image = ProductsPageData.expected_products[product.find_element(*products_page.productlist_name).text]["image"]
            expected_cost = ProductsPageData.expected_products[product.find_element(*products_page.productlist_name).text]["cost"]

            if product_name not in ProductsPageData.expected_products:
                log.critical(f"{product_name}"
                             f" was not found in expected product list!")
            elif product_name in ProductsPageData.expected_products:
                log.info(f"Verifying image url and cost of"
                         f" {product_name}")
                # Verify image url matches with expected url
                if product_image != expected_image:
                    log.critical(f"Test failed: Image url does not match with expected image url:")
                    log.critical(f"Result: {product_image}")
                    log.critical(f"Expected Result: {expected_image}")
                    products_incorrect_image.append(product_name)
                # Verify displayed cost matches with expected cost
                if product_cost != expected_cost:
                    log.critical(f"Test failed: Listed cost does not match with expected cost:")
                    log.critical(f"Result: {product_cost}")
                    log.critical(f"Expected Result: {expected_cost}")
                    products_incorrect_cost.append(product_name)

        # If there is incorrect information on a product throws this error:
        assert (len(products_incorrect_image) == 0
                and len(products_incorrect_cost) == 0), log.critical(
            "Test failed: 1 or more products on site has incorrect information, view log for more information.")
    @pytest.fixture(params=LoginPageData.standard_user)
    def login_page_data(self, request):
        return request.param
