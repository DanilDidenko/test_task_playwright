from playwright.sync_api import Page
from config.urls import LOGIN_PAGE


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = self.page.locator("input[name='email']")
        self.password_input = self.page.locator("input[name='password']")
        self.submit_button = self.page.locator("input[name='submit']")
        self.continue_with_account_button = self.page.locator("#continue_with_this_account")
        self.error_message = self.page.locator("div.cmpTrayAlert .text")
        self.captcha_input = self.page.locator("input[name='captcha[input]']")
        self.email_error = self.page.locator("span#email-error")
        self.password_error = self.page.locator("span#password-error")

    def navigate(self):
        """Navigate to the login page."""
        self.page.goto(LOGIN_PAGE)

    def login(self, email, password):
        """Fill in login credentials and submit the form."""
        self.email_input.wait_for()
        self.email_input.clear()
        self.email_input.fill(email)
        self.password_input.clear()
        self.password_input.fill(password)
        self.submit_button.click()

    def continue_with_account(self):
        """Click the 'Continue' button after login."""
        self.continue_with_account_button.wait_for()
        self.continue_with_account_button.click()

    def get_error_message(self):
        """Retrieve the error message text after a failed login."""
        self.error_message.wait_for()
        return self.error_message.inner_text().strip()

    def get_email_error(self):
        """Returns the error message displayed under the email input field."""
        self.email_error.wait_for(state="visible")
        return self.email_error.inner_text().strip()

    def get_password_error(self):
        """Returns the error message displayed under the password input field."""
        self.password_error.wait_for(state="visible")
        return self.password_error.inner_text().strip()

    def wait_for_captcha(self):
        """Wait for the captcha to appear."""
        self.captcha_input.wait_for()
        return self.captcha_input.is_visible()
