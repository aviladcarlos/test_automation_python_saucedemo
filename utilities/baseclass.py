from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

import pytest
import inspect
import logging


@pytest.mark.usefixtures("setup")
class BaseClass:

    def verify_link_presence(self, text):
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.presence_of_element_located((By.LINK_TEXT, text)))

    def select_drop_down_option_by_text(self, locator, text):
        sel = Select(locator)
        return sel.select_by_visible_text(text)

    def get_logger(self):
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler("../reports/logfile.log")
        formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
        file_handler.setFormatter(formatter)

        # To Clear logger object after each test run if not log will have duplicates
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(file_handler)  # filehandler object

        logger.setLevel(logging.DEBUG)
        return logger
