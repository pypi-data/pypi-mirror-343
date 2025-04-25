import os
import asyncio
from datetime import datetime, timedelta
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import random

from logger import get_logger
from config import config

logger = get_logger(__name__)


class DynamicBrowserPool:
    """Dynamic browser pool, supports auto expansion/shrinkage and health check"""

    def __init__(self):
        self.timezone = self._detect_timezone()
        self.lang = os.getenv("CS_BROWSER_LANG", "en-US")
        logger.info(f"Browser Proxy: {config.proxy}")

        # min size pool
        self.min_size = int(config.browser_pool_min_size)
        self.max_size = int(config.browser_pool_max_size)
        self.idle_timeout = timedelta(seconds=300)  # Idle instance timeout

        # pool status
        self.pool = asyncio.Queue(maxsize=self.max_size)
        self._active_count = 0  # Total active instances (including in use and idle)
        self._last_used = {}  # Instance last used time {crawler: timestamp}
        self._initialized = False
        self._lock = asyncio.Lock()
        self._cleanup_task = None  # Background cleanup task

        # health check url
        self.health_check_url = "https://www.bing.com"

        # browser config
        self.browser_config = BrowserConfig(
            browser_type="chromium",
            headless=config.headless.lower() == "true",
            user_agent=config.user_agent,
            user_agent_mode=config.user_agent_mode,
            proxy=config.proxy,
            user_data_dir=config.user_data_dir,
            text_mode=True,
            light_mode=True,
            viewport_width=1280 + random.randint(-50, 50),
            viewport_height=710 + random.randint(-30, 30),
            extra_args=[
                # 核心参数
                "--lang=" + self.lang,
                "--timezone=" + self.timezone,
                "--no-sandbox",
                "--start-maximized",
                "--force-device-scale-factor=1",
                # GPU/渲染优化
                "--disable-gpu",
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
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-blink-features=AutomationControlled",
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
            headers={
                "Sec-CH-UA-Platform": "Windows",
                "Sec-CH-UA-Mobile": "?0",
            },
            verbose=True,
        )

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

    async def initialize(self):
        """Initialize browser pool"""
        async with self._lock:
            if self._initialized:
                return

            # Initialize minimum instances
            for _ in range(self.min_size):
                crawler = await self._create_crawler()
                await self._safe_put(crawler)

            # Start background cleanup task
            self._cleanup_task = asyncio.create_task(self._background_cleanup())
            self._initialized = True

    async def _create_crawler(self) -> AsyncWebCrawler:
        """Create and initialize browser instance"""
        crawler = AsyncWebCrawler(config=self.browser_config)
        await crawler.start()
        self._active_count += 1
        logger.debug(f"Created new browser instance. Total active: {self._active_count}")
        return crawler

    async def _destroy_crawler(self, crawler: AsyncWebCrawler):
        """Destroy browser instance"""
        try:
            await crawler.close()
            self._active_count -= 1
            logger.debug(f"Destroyed browser instance. Total active: {self._active_count}")
        except Exception as e:
            logger.error(f"Error destroying crawler: {e}")

    async def _safe_put(self, crawler: AsyncWebCrawler):
        """Safe return instance to pool"""
        if self.pool.full():
            await self._destroy_crawler(crawler)  # Exceed capacity, destroy
        else:
            self._last_used[crawler] = datetime.now()
            await self.pool.put(crawler)

    async def _background_cleanup(self):
        """安全清理逻辑"""
        while self._initialized:
            await asyncio.sleep(60)
            try:
                now = datetime.now()
                # 直接遍历最后使用时间字典
                stale_instances = []
                for crawler, last_used in list(self._last_used.items()):
                    if (now - last_used) > self.idle_timeout and self._active_count > self.min_size:
                        stale_instances.append(crawler)

                # 清理过期实例
                for crawler in stale_instances:
                    await self._destroy_crawler(crawler)
                    del self._last_used[crawler]

            except Exception as e:
                logger.error(f"Cleanup error: {str(e)[:200]}")

    async def _get(self) -> AsyncWebCrawler:
        """Get browser instance (auto expand)"""
        try:
            # Try to get from pool first
            return self.pool.get_nowait()
        except asyncio.QueueEmpty:
            # Create new instance when pool is empty
            if self._active_count < self.max_size:
                return await self._create_crawler()
            # Wait when reached limit
            return await self.pool.get()

    async def _put(self, crawler: AsyncWebCrawler):
        """Return browser instance to pool with enhanced safety checks"""
        try:
            # Strict health check with timeout
            if not await asyncio.wait_for(self._is_healthy(crawler), timeout=5):
                await self._destroy_crawler(crawler)
                return

            # Return instance to pool
            await self._safe_put(crawler)
        except Exception as e:
            logger.error(f"Error returning browser to pool: {str(e)[:200]}")
            await self._destroy_crawler(crawler)

    async def _is_healthy(self, crawler: AsyncWebCrawler) -> bool:
        """Health check"""
        try:
            # 通过访问空白页验证实例健康状态
            result = await crawler.arun(
                url=self.health_check_url,
                config=CrawlerRunConfig(page_timeout=5000, verbose=False),
            )
            return result is not None
        except Exception as e:
            logger.warning(f"Browser instance unhealthy: {e}")
            return False

    def get_crawler(self):
        """Get browser instance context manager"""
        return BrowserContext(self)

    async def close(self):
        """Close all resources"""
        self._initialized = False
        if self._cleanup_task:
            self._cleanup_task.cancel()

        # Empty the pool
        while not self.pool.empty():
            crawler = await self.pool.get()
            await self._destroy_crawler(crawler)


class BrowserContext:
    """Browser instance context manager"""

    def __init__(self, pool: DynamicBrowserPool):
        self.pool = pool
        self.crawler = None

    async def __aenter__(self) -> AsyncWebCrawler:
        self.crawler = await self.pool._get()
        logger.debug("Acquired browser instance")

        return self.crawler

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Return browser instance to pool"""
        if self.crawler:
            await self.pool._put(self.crawler)
            logger.debug("Returned browser instance")


# Global browser pool instance
browser_pool = DynamicBrowserPool()
