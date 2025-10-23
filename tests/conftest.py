from datetime import datetime
from selenium import webdriver

import os
import pytest


driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--local_browser", action="store", default="chrome", choices=("chrome", "firefox", "edge"),
        help="Specify browser to run locally (e.g., chrome, firefox, edge)"
    )
    parser.addoption(
        "--docker_browser", action="store", default="", choices=("chrome", "firefox", "edge"),
        help="Specify browser to run in docker (e.g., chrome, firefox, edge)"
    )


@pytest.fixture(scope="class")
def setup(request):

    global driver

    local_browser = request.config.getoption("local_browser")
    docker_browser = request.config.getoption("docker_browser")

    if docker_browser == "chrome":
        driver = webdriver.Remote(command_executor="http://selenium-chrome:4444",
                                  options=webdriver.ChromeOptions())
    elif docker_browser == "firefox":
        driver = webdriver.Remote(command_executor="http://selenium-firefox:4444",
                                  options=webdriver.FirefoxOptions())
    elif docker_browser == "edge":
        driver = webdriver.Remote(command_executor="http://selenium-edge:4444",
                                  options=webdriver.EdgeOptions())

    if docker_browser == "":
        if local_browser == "chrome":
            driver = webdriver.Chrome()
        elif local_browser == "firefox":
            driver = webdriver.Firefox()
        elif local_browser == "edge":
            driver = webdriver.Edge()

    driver.get("https://www.saucedemo.com/")
    driver.implicitly_wait(5)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()


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
