import logging
from llm_interface import LLaMAModel
from amazon_authenticator import AmazonAuthenticator
from amazon_order_fetcher import AmazonOrderFetcher


class Agent:
    def __init__(self, llm_model):
        self.llm_model = LLaMAModel()
        self.authenticator = AmazonAuthenticator(llm_model)
        self.authenticator.init_driver()
        self.authenticator.login()
        self.order_fetcher = AmazonOrderFetcher(self.authenticator.get_driver())
        logging.basicConfig(filename='amazon_order_agent.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def fetch_order_details(self):
        try:  
            orders = self.order_fetcher.fetch_orders()
            if orders:
                print("Orders fetched and saved successfully!")
            else:
                print("No orders found in history")
        finally:
            self.authenticator.close_driver()