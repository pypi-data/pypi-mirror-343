import time
import pyperclip
import logging

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from chatgpt_uoapi.browser import Browser

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")

class ChatGPTAPI:
    """Automates interactions with ChatGPT using Selenium."""

    def __init__(self):
        self.browser = Browser()
        self._launch_chatgpt()

    def chat(self):
        """Chat with ChatGPT using a loop."""
        logging.warning("Press 'q' to quit.")

        counter = 0
        while True:
            try:
                user_input = input("\nPrompt: ")
                if user_input.lower() == "q":
                    logging.info("Exiting program.")
                    self.exit()
                    break

                start_time = time.time()
                response = self.make_request(user_input)
                print(f'Response: {response}')

                counter += 1
                logging.info(f"{counter}: Response received in {time.time() - start_time:.2f}s")
                print(f"{counter}: Response received in {time.time() - start_time:.2f}s")

            except StaleElementReferenceException:
                logging.warning("Encountered StaleElementReferenceException. Retrying...")

            except Exception as e:
                logging.error(f"An error occurred: {e}", exc_info=True)

    def make_request(self, prompt: str) -> str:
        """Makes a single request to ChatGPT."""
        self._focus_on_input_field()
        self._update_input_tb(prompt)
        self._press_enter()
        self._wait_for_response()
        return self._copy_response_to_clipboard()

    def _launch_chatgpt(self):
        """Launches the ChatGPT website."""
        self.browser.launch()
        self.browser.visit_url()
        logging.info("ChatGPT website launched.")

    def _focus_on_input_field(self):
        """Shifts focus to the input field using keyboard shortcut."""
        actions = ActionChains(self.browser.driver)
        actions.key_down(Keys.SHIFT).send_keys(Keys.ESCAPE).key_up(Keys.SHIFT).perform()

    def _update_input_tb(self, text: str):
        """Updates the content inside an editable field using JavaScript."""
        script = """
        let editableDiv = document.querySelector("div[contenteditable='true']");
        if (!editableDiv) {
            console.warn("No contenteditable div found.");
            return;
        }
        
        let paragraph = editableDiv.querySelector("p");
        if (paragraph) {
            paragraph.innerHTML = arguments[0];
        } else {
            console.warn("No <p> element found inside the contenteditable div.");
        }
        """
        self.browser.driver.execute_script(script, text)

    def _press_enter(self):
        """Presses ENTER in the chat input field."""
        elem = self._get_body_element()
        self._wait_for_update()
        elem.send_keys(Keys.ENTER)
        self._wait_for_update()
    
    def _wait_for_response(self, timeout: int = 120):
        """Waits until the response is fully loaded."""
        WebDriverWait(self.browser.driver, timeout, 0.3, (NoSuchElementException)).until_not(
            lambda driver: driver.find_element(By.XPATH, "//*[@aria-label='Stop streaming']").is_displayed()
        )

    def _copy_response_to_clipboard(self) -> str:
        """Copies the latest response from ChatGPT using clipboard shortcuts."""
        self._get_body_element().send_keys(Keys.CONTROL, Keys.SHIFT, "C")
        self._wait_for_update(.3)
        response = pyperclip.paste()
        return response
    
    def _get_body_element(self):
        """Returns the body element of the page."""
        return self.browser.driver.find_element(By.TAG_NAME, "body")

    def _wait_for_update(self, secs: float = .1):
        time.sleep(secs)
    
    def exit(self) -> None:
        self.browser.quit()
    
    def _handle_login_popup(self):
        """Handles the 'Stay logged out' popup if it appears."""
        try:
            popup = WebDriverWait(self.browser.driver, 0.1).until(
                EC.presence_of_element_located((By.XPATH, "//a[text()='Stay logged out']"))
            )
            popup.click()
            logging.info("Login popup detected and dismissed.")
        except:
            pass  # No popup, continue execution




# if __name__ == "__main__":
#     api = ChatGPTAPI()
#     api.chat()
