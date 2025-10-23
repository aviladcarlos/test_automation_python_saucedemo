## Overview
For my first QA automation project, I built a test automation framework using the practice website Sauce Demo(https://www.saucedemo.com/). Applying what I've learned from Udemy courses, I structured the framework following the Page Object Model (POM) design pattern. The framework supports multiple browsers, generates detailed HTML reports, logging, and automatically captures screenshots upon test failures.

## Created With
| Name | Version |
| --- | --- |
| [Python](https://www.python.org/) | 3.12.4 |
| [Pytest](https://pypi.org/project/pytest/) | 8.3.3 |
| [Pytest-html]( https://pypi.org/project/pytest-html/) | 4.1.1 |
| [Selenium](https://pypi.org/project/selenium/) | 4.36.0 |
## Walkthrough
[![Walkthrough Video](https://github.com/user-attachments/assets/be1cbde6-94d0-40c5-9faa-b925ce0cb501)](https://drive.google.com/file/d/1Q3soSmEk7vSJ1OlhLwU3In3mxGzJTMmL/view?usp=drive_link)
## Usage
> [!Note]
> All commands are ran within the `tests` folder/directory.

To run all test in the test suite from the command prompt (cmd) with the following command:
```
pytest
```
To run a specific test from the test suite:
```
pytest test_login_standard_user.py
```
To generate a html report `--html [where to generate report]` needs to be included in the command, example:
```
pytest test_login_standard_user.py --html ../reports/report.html
```
Chrome is the default browser to specify which browser to run the tests on `--local_browser [chrome/firefox/edge]` needs to be included in the command, example:
```
pytest test_login_standard_user.py --html ../reports/report.html --local_browser firefox
```
## Example Report
![Example image of generated report](examples/example_report_img.PNG)

## Running on Docker
Download selenium/standalone docker images for each supported browser. On a command prompt(cmd)/terminal enter the following commands:
* For chrome:
  ```
  docker pull selenium/standalone-chrome:139.0.7258.154-chromedriver-139.0.7258.154-grid-4.35.0-20250909
  ```
* For firefox:
  ```
  docker pull selenium/standalone-firefox:125.0-geckodriver-0.36-grid-4.36.0-20251001
  ```
* For edge:
  ```
  docker pull selenium/standalone-edge:137.0-edgedriver-137.0-grid-4.36.0-20251001
  ```
Create a network so all the containers can communicate with one another:
```
docker network create selenium-net --driver bridge
```
To remove the network after the use:
```
docker rm selenium-net
```
To build Docker image of project:
> [!Note]
> Command is ran within the root folder `test_automation_python_saucedemo`.
```
docker build -t python_saucedemo .
```
Commands to create and run a container of each image:
* For python_saucedemo:
  ```
  docker run -d -it --network selenium-net --name python-saucedemo python_saucedemo
  ```
  * For chrome selenium standalone:
  ```
  docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" --network selenium-net --name selenium-chrome selenium/standalone-chrome:139.0.7258.154-chromedriver-139.0.7258.154-grid-4.35.0-20250909
  ```
  * For firefox selenium standalone:
  ```
  docker run -d -p 4445:4444 -p 7901:7900 --shm-size="2g" --network selenium-net --name selenium-firefox selenium/standalone-firefox:125.0-geckodriver-0.36-grid-4.36.0-20251001
  ```
  * For edge selenium standalone:
  ```
  docker run -d -p 4446:4444 -p 7902:7900 --shm-size="2g" --network selenium-net --name selenium-edge selenium/standalone-edge:137.0-edgedriver-137.0-grid-4.36.0-20251001
  ```
Once the selenium standalone containers are running. You can connect to each of them using a browser to visually see the tests run:
  * For chrome selenium standalone:
  ```
  http://localhost:7900/?autoconnect=1&resize=scale&password=secret
  ```
  * For firefox selenium standalone:
  ```
  http://localhost:7901/?autoconnect=1&resize=scale&password=secret
  ```
  * For edge selenium standalone:
  ```
  http://localhost:7902/?autoconnect=1&resize=scale&password=secret
  ```
To connect the current cmd/terminal to a terminal within the python-saucedemo container:
```
docker exec -it python-saucedemo /bin/sh
```
Once connected to a terminal within python-saucedemo container, the following commands can be used to run the tests:
> [!Note]
> Terminal inside the container is already set to the `tests` folder/directory.
  * `--docker_browser` needs to be included in the command in order to run on docker and a browser needs to be specified `[chrome/firefox/edge]`. To run all tests in the test suite:
    ```
    pytest --docker_browser chrome
    ```
* To run a specific test from the test suite:
  ```
  pytest test_login_standard_user.py --docker_browser chrome
  ```
* To generate a html report --html [where to generate report] needs to be included in the command, example::
  ```
  pytest test_login_standard_user.py --html ../reports/report.html --docker_browser chrome
  ```
