import logging
from playwright.sync_api import Page, BrowserContext

login_attempt_count = 0  # Global variable to track login attempts

def reset_count():
    global login_attempt_count
    login_attempt_count = 0
    logging.info("Login attempt count reset to zero.")

def increment_count():
    global login_attempt_count
    login_attempt_count += 1
    logging.info(f"Login attempt count incremented to {login_attempt_count}.")

def perform_login(context: BrowserContext, page: Page, username: str, password: str, login_url: str, state_file: str = "state.json"):
    """
    Performs login and handles login attempt counts.
    """
    try:
        # Navigate to the login page
        reset_count()  # Reset count when accessing login URL
        page.goto(login_url)

        # Enter login credentials
        page.get_by_label("Username").fill(username)
        page.get_by_label("Password").fill(password)
        page.get_by_role("button", name="SUBMIT").click()

        # Check for successful login
        
        # Check for invalid login error
        if page.get_by_role("heading", name="Invalid username or password").is_visible():
            increment_count()
            if login_attempt_count >= 3:
                logging.error("Account locked after 3 unsuccessful attempts.")
                raise Exception("Account locked.")
            else:
                logging.warning("Invalid login attempt.")
                return

        # Check for successful login
        if "dashboard" in page.url:
            reset_count()  # Reset count on successful login
            context.storage_state(path=state_file)
            logging.info("Login successful and session state saved.")
        else:
            logging.error("Unexpected error during login process.")
    except Exception as e:
        logging.error(f"Login error: {e}")
        raise
