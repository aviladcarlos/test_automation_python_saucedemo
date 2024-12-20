from datetime import datetime
from selenium import webdriver

import os
import pytest


driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="my option: type1 or type2"
    )


@pytest.fixture(scope="class")
def setup(request):

    global driver

    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "ie":
        driver = webdriver.Ie()

    driver.get("https://www.saucedemo.com/")
    driver.implicitly_wait(5)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.close()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not os.path.exists("../reports"):
        os.makedirs("../reports")
        config.option.htmlpath = (
            "../reports/" + datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ".html"
        )
    if os.path.isfile("../reports/logfile.log"):
        with open("../reports/logfile.log", 'w'):
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
     Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
     :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = "../reports/" + report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extras = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
