import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from browser_automation_interface import SeleniumAdapter
from llm_interface import LLaMAModel


class AmazonAuthenticator:
    def __init__(self, llm_model: LLaMAModel):
        self.email = os.environ.get('AMAZON_EMAIL')
        self.password = os.environ.get('AMAZON_PASSWORD')
        self.driver = None
        self.llm_model = llm_model

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless for automation
        self.driver = SeleniumAdapter(webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options))
        
    def login(self):
        if not self.email or not self.password:
            raise ValueError("Amazon username and password must be set as environment variables")
        # self.driver.get("https://www.amazon.com/ap/signin")
        try:
            self.driver.navigate_to("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=900&openid.return_to=https%3A%2F%2Fwww.amazon.com%3Fpd_rd_w%3DPPDJf%26content-id%3Damzn1.sym.80f55c46-3037-42ea-9b77-ed938babf4c3%3Aamzn1.sym.80f55c46-3037-42ea-9b77-ed938babf4c3%26pf_rd_p%3D80f55c46-3037-42ea-9b77-ed938babf4c3%26pf_rd_r%3D99F6MEPQCWMQNJNGQSR4%26pd_rd_wg%3DgqVUc%26pd_rd_r%3D405e8053-f439-45a9-b7fa-4f9dd4c2981d%26qid%3D1715897200%26ref%3Dsxts_aspa_qna%26c_c%3D-802937953&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
            time.sleep(2)
        except NoSuchElementException:
            print("Error: Login elements not found.")
            raise
        
        # Use LLM to find the email field element
        email_field_prompt = "Find the input field where you enter your email address on the Amazon sign-in page."
        email_elem = self.llm_model.find_element_by_description(email_field_prompt, self.driver)
        email_elem.send_keys(self.email)

        # Use LLM to find the "Continue" button element
        continue_button_prompt= "Find the button that says 'Continue' on the Amazon sign-in page."
        continue_button = self.llm_model.find_element_by_description(continue_button_prompt, self.driver)
        continue_button.click()

        time.sleep(2)

        # Use LLM to find the password field element
        password_field_prompt = "Find the input field where you enter your password on the Amazon sign-in page."
        password_elem = self.llm_model.find_element_by_description(password_field_prompt, self.driver)
        password_elem.send_keys(self.password)

        # Use LLM to find the "Sign In" button element
        signin_button_prompt = "Find the button that says 'Sign In' on the Amazon sign-in page."
        signin_button = self.llm_model.find_element_by_description(signin_button_prompt, self.driver)
        signin_button.click()
        
        time.sleep(2)
        
        # Check if login was successful
        if "Your Account" in self.driver.get_page_source():
            print("Login successful")
        else:
            raise Exception("Login failed")

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.quit()
