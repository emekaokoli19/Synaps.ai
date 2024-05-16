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

## Architecture of the system

1. User:
   
  -Initiates the order fetching process by providing their Amazon credentials and any preferences.
   
3. Agent(Orchestrator):
  -The central controller of the system.
  -Manages the overall workflow and coordinates actions between different components.
  -Responsible for high-level decision-making based on information from the LLM and the web scraper.
   
4. Amazon Authenticator:
  -Handles user authentication securely.
  -Retrieves credentials from environment variables or a secure store.
  -Interacts with the Amazon website to log the user in.
   
5. Web Scraper (Selenium WebDriver):
  -Automates browser actions to navigate the Amazon website.
  -Retrieves the HTML content of order history and order details pages.
  -Interacts with web elements like buttons and links.
   
6. LLM Service (Hugging Face Inference API):
  -Communicates with the external LLM (e.g., LLaMA 2 on Hugging Face).
  -Sends prompts containing HTML content to the LLM.
  -Receives responses from the LLM, including extracted order data and instructions for navigation.
  -Optionally, implements caching to optimize performance.
  
7. LLM Model (Local or Cached):
  -Processes the HTML content received from the web scraper.
  -Extract relevant order details using the LLM's language understanding capabilities.
  -Analyze the page structure to determine navigation actions (e.g., finding "Next Page" buttons).
  -Construct prompts for the LLM service.
   
8. Data Storage:
  -Saves extracted order data in a structured format (e.g., JSON).
  -May also store raw HTML files for future reference.
  -Can be implemented using local files or a database.
  
9. Logger:
  -Records important events, errors, and warnings throughout the process.
  -Helps in monitoring and debugging the agent's behavior.
