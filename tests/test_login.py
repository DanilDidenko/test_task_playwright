import time

from config.credentials import VALID_EMAIL, VALID_PASSWORD, INVALID_EMAIL, INVALID_PASSWORD, USERNAME
from pages.login_page import LoginPage
from pages.main_page import MainPage


def test_valid_login(browser):
    """Test a valid login and retrieve username from the profile menu."""
    main_page = MainPage(browser)
    main_page.navigate()

    main_page.handle_popup()
    main_page.navigate_to_login_page()

    login_page = LoginPage(browser)
    login_page.login(VALID_EMAIL, VALID_PASSWORD)
    login_page.continue_with_account()

    username = main_page.get_username()
    assert username == USERNAME, '❌ Username is incorrect'


def test_invalid_login(browser):
    """Test multiple failed login attempts and verify different error messages."""
    main_page = MainPage(browser)
    main_page.navigate()

    main_page.handle_popup()
    main_page.navigate_to_login_page()

    # First failed login attempt
    login_page = LoginPage(browser)
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)
    error_message = login_page.get_error_message()
    assert "Error\n\nThe account name or password that you have entered is incorrect." == error_message, "❌ First error message mismatch!"

    # Third failed login attempt (captcha should appear)
    time.sleep(2)
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)
    time.sleep(2)
    login_page.login(INVALID_EMAIL, INVALID_PASSWORD)
    assert login_page.wait_for_captcha(), "❌ CAPTCHA was expected but did not appear!"


def test_empty_fields(browser):
    """Tests the login attempt with empty email and password fields"""
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("", "")

    email_error = login_page.get_email_error()
    password_error = login_page.get_password_error()

    expected_error = "This field is required!"
    assert email_error == expected_error, f"❌ Email error message mismatch!"
    assert password_error == expected_error, f"❌ Password error message mismatch!"
