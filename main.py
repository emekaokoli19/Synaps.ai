from agent import Agent
from llm_interface import LLaMAModel

if __name__ == "__main__":
    username = "your_email@example.com"
    password = "your_amazon_password"

    llama_model = LLaMAModel()
    agent = Agent(
        llm_model=llama_model
    )

    agent.fetch_order_details()
