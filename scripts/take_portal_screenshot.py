import os
from playwright.sync_api import sync_playwright

INDEX_URL = f"file:///{os.path.abspath('index.html').replace(os.sep, '/')}"
SCREENSHOT_DIR = os.path.abspath("screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
SCREENSHOT_PATH = os.path.join(SCREENSHOT_DIR, "frontpage_portal.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"PAGEERROR: {err}"))
    print(f"Navigating to {INDEX_URL}")
    page.goto(INDEX_URL)
    page.wait_for_timeout(2000)
    page.screenshot(path=SCREENSHOT_PATH, full_page=True)
    browser.close()

print(f"Captured screenshot at: {SCREENSHOT_PATH}")
