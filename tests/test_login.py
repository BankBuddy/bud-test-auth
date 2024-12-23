from playwright.sync_api import sync_playwright
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from actions.login_user import perform_login

def test_login_with_valid_credentials():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        perform_login(context, page, "sohan_beta1", "Sohan@4567", "https://beta1.studio.bankbuddy.me/console/login")
        assert "dashboard" in page.url, "Failed to redirect to dashboard after valid login."

        browser.close()

def test_invalid_attempts_lock_account():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        for _ in range(3):
            try:
                perform_login(context, page, "sohan", "Sohan@4567", "https://beta1.studio.bankbuddy.me/console/login")
            except Exception as e:
                assert "Account locked" in str(e), "Account not locked after 3 invalid attempts."
        
        browser.close()
