import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=sys.argv[1])
    user_prompt=sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]    
    if len(sys.argv) < 2:
        print("No input provided. Please provide a prompt as a command line argument.")
        sys.exit(1)
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt} \nResponse: {response.text} \nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}") 
    else:
        print(response.text)

if __name__ == "__main__":
    main()
