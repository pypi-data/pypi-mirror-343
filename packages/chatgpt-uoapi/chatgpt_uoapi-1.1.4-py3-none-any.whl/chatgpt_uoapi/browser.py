import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager
from chatgpt_uoapi.utils import load_config

class Browser:
    def __init__(self) -> None:
        self.url = 'https://chatgpt.com/'
        self.driver = None
        self.config = load_config()
        self.options = self._get_options()

    def launch(self) -> uc.Chrome:
        driver_path = ChromeDriverManager().install()
        driver = uc.Chrome(service=Service(driver_path), options=self.options, headless=False)
        driver.minimize_window()
        self.driver = driver

    def _get_options(self) -> uc.ChromeOptions:
        options = uc.ChromeOptions()
        options.add_argument(f'--user-data-dir={self.config['PROFILE_PATH']}')
        options.add_argument('--disable-features=WebAuthentication')
        return options
    
    def visit_url(self) -> None:
        try:
            self.driver.get(self.url)
            time.sleep(2)
        except TimeoutException:
            print("Selenium Timeout: The request took too long!")
        except requests.exceptions.ReadTimeout:
            print("Request Timeout: The WebDriver took too long to respond!")
        except WebDriverException as e:
            print(f"Error while getting url. Error: {e}")

    def quit(self) ->  None:
        try:
            self.driver.close()
        except:
            pass