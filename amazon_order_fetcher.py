import os
import json
import time
import logging
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)
from llm_interface import LLaMAModel
from browser_automation_interface import SeleniumAdapter

class AmazonOrderFetcher():
    def __init__(self, driver: SeleniumAdapter):
        self.driver = driver
        self.llm_model = LLaMAModel()
    
    def fetch_orders(self, max_retries=3, retry_delay=5):
        retry_count = 0
        while retry_count < max_retries:
            try:
                logging.info("Fetching order history page...")
                content = self.driver.get_page_source()
                # Use LLM to find the "order-history" page
                element_description = "Find the button for returns & orders that displays the order history"
                order_history = self.llm_model.find_element_by_description(element_description, self.driver)
                if order_history:
                    order_history.click()
                else:
                    self.driver.navigate_to("https://www.amazon.com/gp/css/order-history")
                time.sleep(2)

                orders = []
                while True:
                    html_content = self.driver.get_page_source()

                    # Get order details URLs using LLM
                    order_details_urls = self.llm_model.get_order_details_urls(html_content)

                    for order_details_url in order_details_urls:
                        try:
                            logging.info(f"Navigating to order details: {order_details_url}")
                            self.driver.navigate_to(order_details_url)  # Navigate to order details page
                            time.sleep(2) # Ensure page loads
                            raw_html = self.driver.get_page_source()

                            # Extract order data using the LLM
                            order_data = {
                                "json": self.llm_model.extract_order_data(raw_html),
                                "raw_html": raw_html
                            }
                            orders.append(order_data)  # Append extracted order data
                            self.driver.go_back() # go back to order history 

                            time.sleep(2)  # Give the browser time to load the previous page

                        except (NoSuchElementException, StaleElementReferenceException) as e:
                            logging.warning(f"Error processing order: {e}. Skipping to next order.")
                            continue # Skipping this order if issue arises

                    try:
                        # Use LLM to find the "Next Page" button (or element)
                        next_page_element = self.llm_model.find_next_page_element(html_content, self.driver) 
                        if next_page_element:
                            next_page_element.click()
                            time.sleep(2)
                        else:
                            break  # No more pages
                    except NoSuchElementException: # No more pages
                        logging.info("No more pages found. All orders fetched.")
                        break

                self.save_orders_as_html(orders=orders)
                self.save_orders_as_json(orders=orders)

                return orders
            
            except TimeoutException:
                retry_count = retry_count + 1
                logging.warning(f"Timeout_error. Retry attempt {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(retry_delay) # wait before retrying
                else:
                    logging.error("Error: Max retries exceeded while loading order history page.")
                    return []

    def save_orders_as_html(self, orders, directory="order_html"):
        os.makedirs(directory, exist_ok=True) # Create directory if not exists
        for order in orders:
            filename = f"{directory}/order_{order['json']['order_id']}_{order['json']['order_date'].replace(' ', '_').replace(',', '')}.html"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(order['raw_html']) # Save the raw HTML

    def save_orders_as_json(self, orders, directory="order_json"):
        os.makedirs(directory, exist_ok=True)  # Create directory if not exists
        for order in orders:
            filename = f"{directory}/order_{order['json']['order_id']}_{order['json']['order_date'].replace(' ', '_').replace(',', '')}.json"
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(order['json'], file, indent=4)  # Save the 'json' part of the order
