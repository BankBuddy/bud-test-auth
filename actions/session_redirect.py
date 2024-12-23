from playwright.sync_api import Playwright, sync_playwright, expect

# Constants for login details and URLs
USERNAME_VALID = "sohan_beta1"
PASSWORD_VALID = "Sohan@4567"
USERNAME_INVALID = "sohan_invalid1"  # Change if needed
PASSWORD_INVALID = "WrongPassword"  # Change if needed
LOGIN_URL = "https://beta1.studio.bankbuddy.me/console/login"
DASHBOARD_URL = "https://beta1.studio.bankbuddy.me/console/dashboard"
STATE_FILE = "state.json"


def save_session_state(context, state_file=STATE_FILE):
    """Saves the current session state to a file."""
    context.storage_state(path=state_file)
    print(f"Session state saved to {state_file}")


def load_session_state(playwright: Playwright, state_file=STATE_FILE):
    """Loads session state from a file."""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state=state_file)
    page = context.new_page()
    return browser, context, page


def login(page, username, password):
    """Attempts to log in with the provided credentials."""
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="SUBMIT").click()


def check_invalid_login(page):
    """Checks for the error message for invalid credentials."""
    error_message_locator = page.locator("text=Invalid username or password")
    try:
        expect(error_message_locator).to_be_visible()
        print("Invalid credentials error message displayed.")
        return True
    except AssertionError:
        print("No error message displayed for invalid credentials.")
        return False


def run(playwright: Playwright):
    # Try loading the saved session state
    try:
        browser, context, page = load_session_state(playwright, STATE_FILE)
        print("Loaded session state. Checking session...")
        page.goto(DASHBOARD_URL)  # If session is valid, go directly to the dashboard
    except Exception:
        # No valid session found, so attempt login with invalid credentials first
        print("No valid session state found. Logging in...")

        # Launch browser and perform login
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(LOGIN_URL)

        # Try invalid login
    MAX_ATTEMPTS = 2  # Maximum login attempts

    for attempt in range(MAX_ATTEMPTS):
        print(f"Attempt {attempt + 1}: Logging in...")

        # Perform login with the provided credentials
        login(page, USERNAME_VALID, PASSWORD_VALID)

        if not check_invalid_login(page):  # Successful login
            save_session_state(context, STATE_FILE)
            page.goto(DASHBOARD_URL)
            print("Successfully logged in and redirected to the dashboard.")
            break  # Exit the loop on successful login
        else:
            print(f"Attempt {attempt + 1}: Login failed. Retrying...")

    else:
        # If all attempts fail
        print("Login failed after maximum attempts.")
        raise Exception("Unable to log in after multiple attempts.")

    # Clean up
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
