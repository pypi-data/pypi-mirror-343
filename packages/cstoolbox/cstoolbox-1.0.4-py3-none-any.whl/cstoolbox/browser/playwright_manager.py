"""
Playwright browser implementation for web crawling.
"""

import os
import random
from pathlib import Path

from playwright.async_api import Browser, BrowserContext, async_playwright

from . import BrowserConfig, BrowserType
from cstoolbox.logger import get_logger

logger = get_logger(__name__)

BROWSER_DISABLE_OPTIONS = [
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-breakpad",
    "--disable-client-side-phishing-detection",
    "--disable-component-extensions-with-background-pages",
    "--disable-default-apps",
    "--disable-extensions",
    "--disable-features=TranslateUI",
    "--disable-hang-monitor",
    "--disable-ipc-flooding-protection",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-sync",
    "--force-color-profile=srgb",
    "--metrics-recording-only",
    "--no-first-run",
    "--password-store=basic",
    "--use-mock-keychain",
]

BROWSER_TEXT_MODE_OPTIONS = [
    "--blink-settings=imagesEnabled=false",
    "--disable-remote-fonts",
    "--disable-images",
    "--disable-software-rasterizer",
    "--disable-dev-shm-usage",
]


class PlaywrightManager:
    """Playwright implementation of browser pool"""

    def __init__(self, config: BrowserConfig):
        if not config.type:
            config.type = BrowserType.CHROMIUM
        if not config.viewport:
            config.viewport = {"width": 1280 + random.randint(-200, 200), "height": 710 + random.randint(-100, 100)}

        def update_args(args: dict, new_args: list):
            for arg in new_args:
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    args[key] = value
                else:
                    args[arg] = None

        args = {}
        if config.extra_args:
            update_args(args, config.extra_args)
        if config.proxy:
            args["--proxy-server"] = config.proxy
        if config.light_mode:
            update_args(args, BROWSER_DISABLE_OPTIONS)
        if config.text_mode:
            update_args(args, BROWSER_TEXT_MODE_OPTIONS)

        config.extra_args = []
        for key, value in args.items():
            if value:
                config.extra_args.append(f"{key}={value}")
            else:
                config.extra_args.append(key)

        self.config = config

    async def launch_browser(self) -> Browser:
        """Launch browser with configuration"""
        playwright = await async_playwright().start()

        launch_options = {
            "headless": self.config.headless,
            "timeout": self.config.timeout,
            "args": self.config.extra_args,
            "env": self.config.env,
        }

        if self.config.executable_path:
            launch_options["executable_path"] = self.config.executable_path

        if self.config.type == BrowserType.CHROMIUM:
            return await playwright.chromium.launch(**launch_options)
        elif self.config.type == BrowserType.FIREFOX:
            return await playwright.firefox.launch(**launch_options)
        else:
            return await playwright.webkit.launch(**launch_options)

    async def create_context(self, browser: Browser) -> BrowserContext:
        """Create browser context with configuration"""
        context_options = {
            "ignore_https_errors": self.config.ignore_https_errors,
            "java_script_enabled": self.config.java_script_enabled,
        }

        if self.config.user_agent:
            context_options["user_agent"] = self.config.user_agent
        if self.config.viewport:
            context_options["viewport"] = self.config.viewport

        if self.config.user_data_dir:
            try:
                user_data_dir = Path(self.config.user_data_dir)
                if not user_data_dir.exists():
                    os.makedirs(user_data_dir, exist_ok=True)
                state_file = user_data_dir.joinpath("state.json")
                if not state_file.exists():
                    state_file.touch()
                context_options["storage_state"] = str(state_file)
            except Exception as e:
                logger.warning(f"Failed to setup user data dir: {e}")

        return await browser.new_context(**context_options)
