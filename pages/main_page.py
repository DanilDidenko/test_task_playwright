from playwright.sync_api import Page

from config.urls import MAIN_PAGE


class MainPage:

    def __init__(self, page: Page):
        self.page = page
        self.user_avatar_button = self.page.locator(".user_avatar-desktop")
        self.login_button = self.page.locator(".user_avatar-desktop .login")
        self.popup_iframe = self.page.frame_locator("div[id^='sp_message_container_'] iframe")
        self.popup_accept_button = self.page.locator("//button[contains(text(), 'Accept')]")
        self.popup_container = self.page.locator("div[id^='sp_message_container_']")
        self.profile_registration = self.page.locator("div.user_avatar div.m1-desktop-registration")
        self.username_field = self.page.locator(".m1-header-main-box-wrapper .desktop-reg-message .username")

    def navigate(self):
        """Navigate to the main page."""
        self.page.goto(MAIN_PAGE)

    def handle_popup(self):
        """Close the 'Accept' popup if it appears."""
        self.popup_container.wait_for(timeout=5000)
        self.popup_iframe.locator(self.popup_accept_button).click()
        self.popup_container.wait_for(state="detached", timeout=5000)

    def click_user_avatar_button(self):
        """Click user avatar with hover and delay to avoid flickering issues."""
        self.user_avatar_button.wait_for()
        self.user_avatar_button.hover()
        self.user_avatar_button.click(delay=100)

    def navigate_to_login_page(self):
        """Click the avatar, then open the login form."""
        self.click_user_avatar_button()
        self.login_button.wait_for()
        self.login_button.click()

    def get_username(self):
        """Click avatar after login and retrieve the displayed username."""
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts: #Workaround to fix infinite load on main page after login
            self.click_user_avatar_button()
            try:
                self.username_field.wait_for(timeout=5000)
                return self.username_field.inner_text().strip()
            except:
                attempt += 1
                if attempt < max_attempts:
                    self.login_button.wait_for()
                    self.login_button.click()
                else:
                    raise Exception("❌ Failed to retrieve username after multiple attempts.")
