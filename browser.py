import asyncio
import base64
import os
import sys
from typing import Optional
import asyncio

from playwright.__main__ import main
from playwright.async_api import Browser, async_playwright

_browser: Optional[Browser] = None

from config import base_url, dy_images_dir
from PIL import Image, ImageDraw, ImageFont


async def init(**kwargs) -> Browser:
    global _browser
    global playwright
    # browser = await async_playwright()
    playwright = await async_playwright().start()
    # _browser = await playwright.chromium.launch(**kwargs)
    _browser = await playwright.chromium.launch(**kwargs)
    return _browser


async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)


async def get_dynamic_screenshot_mobile(url):
    browser = await get_browser()
    page = None
    try:
        file_name = url.split('/')[-1] + '.jpeg'
        file_dir = dy_images_dir + file_name
        iphone = playwright.devices["iPhone 13"]
        context = await browser.new_context(**iphone)
        page = await context.new_page()
        await page.set_viewport_size({"width": 480, "height": 2080})
        await page.goto(url, wait_until="networkidle", timeout=10000)
        #await page.evaluate('document.body.style.fontFamily = "宋体"')
        #屏蔽关注按钮
        await page.evaluate('document.getElementsByClassName("dyn-header__right")[0].style.display="none"')
        card = await page.query_selector(".dyn-card")
        assert card
        #dyn_follow = page.query_selector(".dyn-header__right")
        #doucumnet.body
        clip = await card.bounding_box()
        assert clip
        image = await page.screenshot(clip=clip, type='jpeg', path=file_dir, full_page=True)

        width = int(clip["width"])
        height = int(clip["height"])
        if width / height > 2.78:
            old_im = Image.open(file_dir)
            new_im = Image.new(old_im.mode, (old_im.size[0], int(old_im.size[0]/2.78)), (255, 255, 255, 255))
            new_im.paste(old_im, (0, 0, old_im.size[0], old_im.size[1]))
            new_im.save(file_dir)

        await page.close()
        return base_url + file_name
    except Exception:
        if page:
            await page.close()
        raise


async def get_dynamic_screenshot(url):
    playwright = await get_browser()
    page = None
    try:
        filename = url.split('/')[-1] + '.jpeg'
        page = await playwright.new_page(device_scale_factor=2)
        await page.goto(url, wait_until="networkidle", timeout=10000)
        await page.set_viewport_size({"width": 1440, "height": 1080})
        card = await page.query_selector(".card")
        assert card
        clip = await card.bounding_box()
        assert clip
        bar = await page.query_selector(".text-bar")
        assert bar
        bar_bound = await bar.bounding_box()
        assert bar_bound
        clip["height"] = bar_bound["y"] - clip["y"]
        width = clip["width"]
        height = clip["height"]
        if width / height > 2.78:
            height = width / 2.78
        clip["height"] = height
        image = await page.screenshot(clip=clip, type='jpeg', path="/home/images/" + filename, full_page=True)
        await page.close()
        return base64.b64encode(image).decode()
    except Exception:
        if page:
            await page.close()
        raise


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_dynamic_screenshot_mobile('https://t.bilibili.com/687435805223813174'))
    loop.close()

def install():
    """自动安装、更新 Chromium"""

    def restore_env():
        pass

    sys.argv = ["", "install", "chromium"]
    original_proxy = os.environ.get("HTTPS_PROXY")
    os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = "https://playwright.sk415.workers.dev"
    success = False
    try:
        main()
    except SystemExit as e:
        if e.code == 0:
            success = True
    if not success:
        os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = ""
        try:
            main()
        except SystemExit as e:
            if e.code != 0:
                restore_env()
                raise RuntimeError("未知错误，Chromium 下载失败")
    restore_env()


async def check_playwright_env():
    """检查 Playwright 依赖"""
    try:
        async with async_playwright() as p:
            await p.chromium.launch()
    except Exception:
        raise ImportError(
            "加载失败，Playwright 依赖不全，"
            "解决方法：https://haruka-bot.sk415.icu/faq.html#playwright-依赖不全"
        )


if __name__ == '__main__':
    install()
