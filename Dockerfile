FROM python:3.12.4

WORKDIR /test_automation_python_saucedemo

COPY pageobjects pageobjects
COPY reports reports
COPY testdata testdata
COPY tests tests
COPY utilities utilities

RUN pip install --no-cache-dir  pytest==8.3.3
RUN pip install --no-cache-dir  pytest-html==4.1.1
RUN pip install --no-cache-dir  pytest-metadata==3.1.1
RUN pip install --no-cache-dir  selenium==4.36.0

WORKDIR /test_automation_python_saucedemo/tests