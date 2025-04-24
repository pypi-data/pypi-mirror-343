import os
import click
from dotenv import load_dotenv
from .translator import translate_to_command
from .executor import execute_command
from .interpreter import interpret_command
from .logger import setup_logger
from .utils import setup_openai_api_key

@click.command()
def main():
    """ServerMind CLI - AI-powered command line interface"""
    load_dotenv()
    logger = setup_logger()
    
    if not setup_openai_api_key():
        logger.error("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables or .env file.")
        return
    
    try:
        user_input = click.prompt("Enter your command in natural language", type=str)
        command = translate_to_command(user_input)
        interpreted_command = interpret_command(command)
        execute_command(interpreted_command)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return

if __name__ == "__main__":
    main() 