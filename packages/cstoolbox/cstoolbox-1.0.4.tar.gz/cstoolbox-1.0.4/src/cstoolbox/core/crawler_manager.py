import asyncio
import os
from datetime import datetime, timedelta

from cstoolbox.browser.config import BrowserConfig, BrowserType
from cstoolbox.browser.crawler import Crawler
from cstoolbox.browser.pool import BrowserPool
from cstoolbox.config import config
from cstoolbox.logger import get_logger

logger = get_logger(__name__)


class CrawlerManager:
    """Dynamic browser pool, supports auto expansion/shrinkage and health check"""

    def __init__(self):
        self.timezone = self._detect_timezone()
        self.lang = os.getenv("CS_BROWSER_LANG", "en-US")

        self.idle_timeout = timedelta(seconds=300)  # Idle instance timeout

        # pool status
        self._lock = asyncio.Lock()

        # health check url
        self.health_check_url = "https://www.bing.com"

        # browser config
        logger.info(f"Set Browser Env: proxy: {config.proxy}, lang: {self.lang}, timezone: {self.timezone}")
        self.browser_config = BrowserConfig(
            type=config.browser_type or BrowserType.CHROMIUM,
            headless=config.headless.lower() == "true",
            proxy=config.proxy,
            user_data_dir=None if config.executable_path else config.user_data_dir,
            text_mode=True,
            light_mode=True,
            executable_path=config.executable_path,
            extra_args=[
                # 核心参数
                "--lang=" + self.lang,
                "--timezone=" + self.timezone,
                "--force-device-scale-factor=1",
                # GPU/渲染优化
                "--enable-gpu-rasterization",  # 平衡性能与兼容性
                "--disable-software-rasterizer",
                "--disable-gl-drawing-for-tests",
                # 指纹混淆
                "--use-gl=desktop",
                "--use-angle=swiftshader",
                "--disable-linux-dmabuf",
                "--disable-accelerated-video",
                # 安全限制
                "--disable-dev-shm-usage",
                "--no-sandbox",
                # 进程控制
                "--no-zygote",
                # 网络优化
                "--disable-background-networking",
                "--disable-sync",
                "--disable-default-apps",
                "--disable-component-update",
                # 功能限制
                "--disable-popup-blocking",
                "--mute-audio",
                "--disable-notifications",
                # 环境模拟
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--disable-features=IsolateOrigins,site-per-process,AudioServiceOutOfProcess",
                "--enable-features=NetworkService",
                # 隐藏自动化特征
                "--disable-infobars",
                "--no-first-run",
                "--hide-scrollbars",
                "--remote-debugging-port=0",
                # 内存优化
                "--js-flags=--max-old-space-size=512",
                # 增加稳定性参数
                "--disable-2d-canvas-clip-aa",
                "--disable-breakpad",
                "--disable-cloud-import",
                "--disable-domain-reliability",
                "--disable-ios-physical-web",
                "--disable-partial-raster",
                "--disable-speech-api",
                # 其他
                "--disable-extensions",
                "--autoplay-policy=user-gesture-required",
            ],
        )
        self.pool = BrowserPool(self.browser_config)
        self.crawler = Crawler(self.pool)

    def _detect_timezone(self) -> str:
        """
        Auto detect timezone
        """
        # Get timezone from environment variables
        if tz := os.environ.get('CS_BROWSER_TZ'):
            return tz

        # Try to get timezone from /etc/timezone file
        try:
            with open('/etc/timezone') as f:
                return f.read().strip()
        except FileNotFoundError:
            pass

        # Get system current timezone
        return datetime.now().astimezone().tzinfo.tzname(None) or 'Etc/UTC'

    def get_crawler(self):
        """Get browser instance context manager"""
        return BrowserContext(self)


class BrowserContext:
    """Browser instance context manager"""

    def __init__(self, manager: CrawlerManager):
        self.manager = manager

    async def __aenter__(self) -> Crawler:
        return self.manager.crawler

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Return browser instance to pool"""
        pass


# Global browser pool instance
crawler_manager = CrawlerManager()
