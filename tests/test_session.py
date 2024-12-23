from asyncio import run
import os
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from actions.session_redirect import load_session_state

def test_session_management():
    state_file = "state.json"
    with sync_playwright() as playwright:
        # Initial login and save session
        if not os.path.exists(state_file):
            print("No session state found. Performing login...")
            run(playwright)
            assert os.path.exists(state_file), "Session state file was not created after login."

        # Reuse session and check dashboard redirection
        browser, context, page = load_session_state(playwright, state_file)
        page.goto("https://beta1.studio.bankbuddy.me/console/dashboard")
        assert page.url == "https://beta1.studio.bankbuddy.me/console/dashboard", "Did not redirect to dashboard with saved session."

        # Simulate session expiry and test fallback
        # os.remove(state_file)
        # print("Deleted session state. Testing fresh login...")
        # run(playwright)
        # assert os.path.exists(state_file), "Session state file was not recreated after re-login."

test_session_management()
