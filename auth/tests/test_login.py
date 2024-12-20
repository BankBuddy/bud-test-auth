import pytest
from playwright.async_api import async_playwright
from actions.login_user import login # type: ignore

@pytest.mark.asyncio
class TestConsole:
    async def test_login(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # Reuse the login action
                await login(
                    page,
                    username="sohan",    
                    password="Sohan@4567",  
                    url="https://superkycdev.kinabank.com.pg/console/login"  
                )
                await page.pause()  # Optional: Pause for debugging
            finally:
                # Cleanup
                await browser.close()
