# Playwright Test Framework

## 📌 Overview

Automated login testing using **Playwright + Pytest**.  
Supports **cross-browser testing**, **HTML report generation**, and **screenshots on failures**.

## 🚀 Installation

```sh
git clone https://github.com/DanilDidenko/test_task_playwright.git
cd test_task_playwright
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
pip install -r requirements.txt
playwright install
```

## 🏃 Running Tests

Run tests with an HTML report (default: Firefox):

```sh
pytest --html=reports/report.html --self-contained-html
```

Run tests in Chrome:

```sh
pytest --browser=chromium --html=reports/report.html --self-contained-html
```

Run tests in headless mode (without UI)

```sh
pytest --headless --html=reports/report.html --self-contained-html
```

Run tests in Chrome + Headless mode

```sh
pytest --browser=chromium --headless --html=reports/report.html --self-contained-html
```

## 📄 Reports

📜 HTML report: reports/report.html

📸 Failure screenshots: reports/screenshots/