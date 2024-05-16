import os
import requests
import json
import logging
import pandas as pd
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datasets import load_dataset, Dataset
from transformers import (
    TrainingArguments,
    AutoTokenizer,
    AutoModelForCausalLM
)
from trl import SFTTrainer
from amazon_data_generator import AmazonOrderDataGenerator


class LLMInterface(ABC):
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def fine_tune(self, dataset_name, output_dir):
        raise NotImplementedError

    @abstractmethod
    def _call_llm(self, prompt, max_tokens=200):
        raise NotImplementedError

    # Data extraction method moved to subclass
    @abstractmethod
    def extract_order_data(self, html_content):
        raise NotImplementedError

    # Method for getting next page CSS selector moved to subclass
    @abstractmethod
    def find_next_page_element(self, html_content, driver):
        raise NotImplementedError

    # Method for getting order details URLs moved to subclass
    @abstractmethod
    def get_order_details_urls(self, html_content):
        raise NotImplementedError

    # Method for checking if there are more orders moved to subclass
    @abstractmethod
    def has_more_orders(self, html_content):
        raise NotImplementedError

    # Method for getting an element
    @abstractmethod
    def find_element_by_llm(self, html_content, driver):
        raise NotImplementedError


class LLaMAModel(LLMInterface):
    def __init__(self, api_url="https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"):
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_HUB_TOKEN')}"}
        self.model_name = "meta-llama/Llama-2-7b-chat-hf"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def fine_tune(
        self,
        dataset_name=None,
        output_dir="fine_tuned_llama",
        epochs=3,
        batch_size=4,
        learning_rate=2e-4,
        num_synthetic_examples=1000
    ):
        """Fine-tunes the LLaMA model on the specified dataset.

        Args:
            dataset_name: Name of the dataset on the Hugging Face Hub.
            output_dir: Directory to save the fine-tuned model.
            epochs: Number of training epochs.
            batch_size: Batch size for training.
            learning_rate: Learning rate for the optimizer.
            num_synthetic_examples: Number of synthetic examples to generate if no dataset_name is provided.
        """
        if dataset_name:
            dataset = load_dataset(dataset_name)
        else:
            generator = AmazonOrderDataGenerator()
            synthetic_data = generator.generate_dataset(num_synthetic_examples)
            dataset = Dataset.from_pandas(pd.DataFrame(synthetic_data))

        training_args = TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=learning_rate,  
            num_train_epochs=epochs, 
            optim="adamw_torch",
            evaluation_strategy="epoch", 
        )

        # Create the SFTTrainer (PEFT technique for fine-tuning)
        trainer = SFTTrainer(
            model=self.model,
            train_dataset=dataset["train"],
            eval_dataset=dataset["validation"],
            args=training_args,
            tokenizer=self.tokenizer,
        )

        # Start training
        trainer.train()

        # Save the fine-tuned model
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)

    def _call_llm(self, prompt, max_tokens=200):
        data = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": max_tokens}
        }
        response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()[0]['generated_text']

    def extract_order_data(self, html_content):
        prompt = f"""Extract the following information from this Amazon order confirmation HTML, in JSON format:

        {
            "order_id": "",
            "order_date": "",
            "order_total": "",
            "shipping_address": "",
            "delivery_status": "",
            "items": [
                {
                    "name": "",
                    "quantity": "",
                    "price": ""
                }
            ]
        }

        Replace the empty string values ("") with the corresponding data from the HTML. If a piece of information is not present in the HTML, fill the corresponding value with "N/A".

        HTML:
        ```
        {html_content}
        ```
        JSON:
        """
        
        json_string = self._call_llm(prompt)
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            # Handle cases where the LLM doesn't output valid JSON
            logging.warning("LLM did not return valid JSON for order data extraction")
            return {}

    def find_next_page_element(self, html_content, driver):
        prompt = f"""Analyze this HTML content and return the CSS selector for the "Next Page" button or link that takes you to another page, if it exists. If there is no next page, return "NONE".

        HTML:
        ```
        {html_content}
        ```
        CSS Selector:"""

        selector = self._call_llm(prompt).strip()
        return driver.find_element(By.CSS_SELECTOR, selector) if selector != "NONE" else None
    
    def get_order_details_urls(self, html_content):
        prompt = f"""Extract the URLs for each order details page from this Amazon order history page HTML.

        HTML:
        ```
        {html_content}
        ```
        URLs (comma-separated):"""
        response = self._call_llm(prompt).strip()
        return [url.strip() for url in response.split(',')] if response else []

    def find_element_by_description(self, element_description, driver):
        prompt = f"""Analyze the current page HTML and find the element that best matches the following description:

        ```
        {element_description}
        ```
        
        If multiple elements match the description, prioritize interactive elements like buttons, links, or input fields. Return the CSS selector for this element. If no element is found, return "NOT_FOUND".

        HTML:
        ```
        {driver.get_page_source()}
        ```

        CSS Selector:"""

        selector = self._call_llm(prompt).strip()
        if selector == "NOT_FOUND":
            raise NoSuchElementException(f"Element not found: {element_description}")
        return driver.find_element(By.CSS_SELECTOR, selector)

    def find_element_by_llm(self, html_content, driver):
        prompt = f"""Analyze the current page HTML and find the element that matches the following description:

        ```
        {html_content}
        ```
        Return the CSS selector for this element. If the element is not found, return "NOT_FOUND".
        """
        css_selector = self.llm_model._call_llm(prompt).strip()
        if css_selector == "NOT_FOUND":
            raise NoSuchElementException(f"Element not found: {html_content}")
        return driver.find_element(By.CSS_SELECTOR, css_selector)

    def has_more_orders(self, html_content):
        prompt = f"""Does this Amazon order history page contain a "Next Page" button? 

        HTML:
        ```
        {html_content}
        ```
        Answer (Yes/No):"""
        response = self._call_llm(prompt).strip()
        return response.lower() == "yes"
