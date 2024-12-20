from playwright.async_api import Page

async def login(page: Page, username: str, password: str, url: str):
    """
    Perform the login action.

    Args:
        page (Page): Playwright page object.
        username (str): Username for login.
        password (str): Password for login.
        url (str): The URL to navigate to for login.

    Raises:
        AssertionError: If the login fails to navigate to the dashboard.
    """
    await page.goto(url)
    await page.fill('input[type="text"][aria-invalid="false"]', username)
    await page.fill('input[type="password"]', password)
    await page.click('text=Submit')

    await page.wait_for_load_state("networkidle")
    assert "dashboard" in page.url, "Failed to login and navigate to the dashboard"
