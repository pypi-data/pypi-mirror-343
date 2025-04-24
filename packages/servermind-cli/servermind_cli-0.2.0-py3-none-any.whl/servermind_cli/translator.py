import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def translate_to_command(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates natural language into Linux commands. Only respond with the command, no explanation."},
            {"role": "user", "content": text}
        ]
    )
    
    return response.choices[0].message.content 