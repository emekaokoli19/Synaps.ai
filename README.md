# Amazon Order Fetching Agent
This project leverages a large language model (LLM) and web scraping techniques to automatically extract and save your Amazon order history.

Features
Fetches order details from your Amazon account.
Extracts key information like order ID, date, total, shipping address, delivery status, and item details.
Saves each order's details as both:
A raw HTML file for reference.
A structured JSON file for easy analysis.
Uses a powerful LLM (currently LLaMA 2 via Hugging Face Inference API) for intelligent data extraction and page navigation.
Robust error handling for potential issues like network problems or website changes.
Detailed logging for monitoring and debugging.

## Requirements
Python 3.6>: Make sure you have Python installed.
Libraries:  Install the required Python libraries

Bash
```
pip install selenium requests beautifulsoup4 transformers datasets trl
```
Use code with caution.
ChromeDriver: Download and install the ChromeDriver executable compatible with your Chrome browser version. Ensure it's in your system's PATH or provide the path to the webdriver.Chrome() function in the amazon_authenticator.py file.

Hugging Face Account and API Token: You'll need a Hugging Face account and an API token to use their Inference API for LLaMA 2. You can get your token from your Hugging Face profile settings.

Environment Variables
Before running the agent, you need to set the following environment variables:

HUGGINGFACE_HUB_TOKEN: Your Hugging Face API token.
AMAZON_USERNAME: Your Amazon email address.
AMAZON_PASSWORD: Your Amazon password.
You can set these either directly in your terminal or by creating a .env file in the project root directory and loading it with python-dotenv:

## .env file
HUGGINGFACE_HUB_TOKEN=your_hugging_face_token
AMAZON_USERNAME=your_amazon_email
AMAZON_PASSWORD=your_amazon_password
How to Run
Clone the Repository:

Bash
```
git clone https://github.com/emekaokoli19/Synaps.ai.git)
```
Install Dependencies
Run the Agent:

Bash
```
python main.py
```

The script will automatically enter your Amazon email and password from environment variables.
The script will automatically open Amazon using selenium. Login using the information provided in the terminal.

## Output:

Raw HTML files will be saved in the order_html directory.
Structured JSON data for all orders will be saved in orders.json.
A log file (amazon_order_agent.log) will be created to track the agent's progress and any errors encountered.
Important Note:

This project uses web scraping techniques, so be mindful of Amazon's terms of service and avoid excessive requests to their website.
