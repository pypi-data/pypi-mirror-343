"""
Browser core implementation for Playwright-based web crawling.

Contains:
- BrowserPool class
"""

import asyncio
from typing import Optional

from playwright.async_api import Browser, BrowserContext, Page

from .config import BrowserConfig, PageConfig
from .playwright_manager import PlaywrightManager
from cstoolbox.config import server_root


class BrowserPool:
    """Browser pool for managing browser instances"""

    def __init__(self, config: BrowserConfig):
        self.playwright_manager = PlaywrightManager(config)

        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._lock = asyncio.Lock()

    async def _get_browser(self) -> Browser:
        """Get or create browser instance"""
        if self._browser is None or not self._browser.is_connected():
            async with self._lock:
                if self._browser is None or not self._browser.is_connected():
                    self._browser = await self.playwright_manager.launch_browser()
        return self._browser

    async def _get_context(self) -> BrowserContext:
        """Get or create context instance"""
        async with self._lock:
            if self._context is None or not self._context.browser.is_connected():
                if self._browser is None:
                    self._browser = await self.playwright_manager.launch_browser()
                self._context = await self.playwright_manager.create_context(self._browser)
        return self._context

    async def new_page(self, config: PageConfig) -> Page:
        """Create new page with given configuration"""
        context = await self._get_context()
        page = await context.new_page()

        await page.set_extra_http_headers(
            {'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}
        )

        if not config.wait_until or not config.wait_until in ['domcontentloaded', 'load', 'networkidle']:
            config.wait_until = 'domcontentloaded'
        await page.wait_for_load_state(config.wait_until)

        if config.page_timeout:
            page.set_default_timeout(config.page_timeout)

        await page.add_init_script(script=config.init_js_code, path=f"{server_root}/schema/init_js/init.js")

        return page

    async def close(self):
        """Close browser and context"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
