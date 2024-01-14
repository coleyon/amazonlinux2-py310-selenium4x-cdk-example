import json
import os
import pathlib
import tempfile
from tempfile import mkdtemp
from typing import Optional

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from libs.log import get_logger

log = get_logger(__name__)

# DOWNLOAD_DIR = "/tmp"
PAGE_LOAD_TIMEOUT = 120  # selenium.webdriver().set_page_load_timeout(n)
IMPLICITY_TIMEOUT = 60  # selenium.webdriver().implicitly_wait(n)
# # See: https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md

CHROME_PATH = os.getenv("CHROME_PATH", "/opt/chrome/chrome")
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", "/opt/chromedriver")

class BaseWebDriver:
    download_dir: Optional[pathlib.Path] = None
    driver: Optional[webdriver.Chrome] = None
    wait: Optional[WebDriverWait] = None
    actionchain: Optional[ActionChains] = None
    remote_debugging_port: str = 9222

    def __init__(self):
        self.user_data_dir = mkdtemp()
        self.data_path = mkdtemp()
        self.disk_cache_dir = mkdtemp()
        self.download_dir = mkdtemp()
        self.remote_debugging_port = "9222"

        options = webdriver.ChromeOptions()
        options.binary_location = CHROME_PATH
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={self.user_data_dir}")
        options.add_argument(f"--data-path={self.data_path}")
        options.add_argument(f"--disk-cache-dir={self.disk_cache_dir}")
        options.add_argument(f"--remote-debugging-port={self.remote_debugging_port}")
        options.add_argument(f"--download.default_directory={self.download_dir}")

        service = webdriver.ChromeService(CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(options=options, service=service)

        options.enable_downloads = True
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self.driver.implicitly_wait(IMPLICITY_TIMEOUT)
        log.debug(f"WebDriver session opened sesion-id={self.driver.session_id}.")
        # for waiting routine
        log.debug("WebDriver wait routine generated.")
        self.wait = WebDriverWait(self.driver, PAGE_LOAD_TIMEOUT)
        # generate action chain
        log.debug("WebDriver action chain generated.")
        self.actionchain = ActionChains(self.driver)
        log.debug(f"Using {options._binary_location} as Chrome binary.")
        log.debug(f"Capabilities: {json.dumps(self.driver.capabilities)}")
        log.info("WebDriver initialized.")



class GoogleSearchSampleDriver(BaseWebDriver):
    """
    Google検索サンプルWebDriver
    """

    def test(self):
        # googleにアクセスしキーワードを入れて検索する
        self.driver.get("https://www.google.com")
        quer = self.wait.until(EC.visibility_of_element_located((By.NAME, "q")))
        quer.send_keys("test")
        quer.send_keys(Keys.ENTER)
        # 検索結果画面への遷移を待機し、Google検索結果のウインドウタイトルを取得する
        self.wait.until(EC.presence_of_all_elements_located)
        # 検索結果のページタイトルを返す
        return self.driver.title
