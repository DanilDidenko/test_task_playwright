import datetime
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    """Adds command-line options for browser selection and custom HTML report path."""
    parser.addoption("--browser", action="store", default="firefox",  # Default is Firefox
                     choices=["chromium", "firefox"], help="Select the browser: chromium or firefox")
    parser.addoption("--html-report", action="store", default="reports/report.html",
                     help="Set a custom path for the pytest-html report")
    parser.addoption("--headless", action="store_true", help="Run test in headless mode (without UI)")


@pytest.fixture(scope="function")
def browser(request):
    """Fixture to launch the browser based on the command-line option."""
    browser_type = request.config.getoption("--browser")
    headless_mode = request.config.getoption("--headless")
    with sync_playwright() as p:
        launch_options = {"headless": headless_mode}
        if browser_type == "chromium":
            launch_options["args"] = ["--disable-blink-features=AutomationControlled"]
        browser = getattr(p, browser_type).launch(**launch_options)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()


@pytest.fixture(scope="session")
def report_dir(request):
    """Determine the directory where the pytest-html report is saved."""
    html_report_path = request.config.getoption("--html-report")
    report_directory = Path(html_report_path).parent
    report_directory.mkdir(parents=True, exist_ok=True)
    return report_directory


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot on test failure and save it in the same folder as the HTML report."""
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        page = item.funcargs.get("browser")
        if page:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            report_directory = Path(item.config.getoption("--html-report")).parent
            screenshot_dir = report_directory / "screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            screenshot_path = screenshot_dir / f"{item.name}_{timestamp}.png"
            screenshot_relative_path = f"screenshots/{item.name}_{timestamp}.png"

            page.screenshot(path=str(screenshot_path))

            if hasattr(report, "extras"):
                pytest_html = item.config.pluginmanager.getplugin("html")
                extra = getattr(report, "extras", [])
                extra.append(pytest_html.extras.image(screenshot_relative_path))
                report.extra = extra
