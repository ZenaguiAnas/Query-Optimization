from openai import OpenAI
import os

from dotenv import dotenv_values
config = dotenv_values()

def optimizer(query):

    client = OpenAI(
        api_key = config.get("API_KEY"),  
        base_url = config.get("BASE_URL")
    )

    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": """You are a chatbot specializing in optimizing SQL queries within the Oracle syntax ecosystem. Your primary functionality is to receive SQL queries from users and provide them with optimized versions for better performance."""},
            {"role": "user", "content": query}
        ]
    )

    chatbot_response=response.choices[0].message.content
    return chatbot_response