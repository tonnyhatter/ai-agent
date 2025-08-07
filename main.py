import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import system_prompt
from functions.get_files_info import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def main():
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=sys.argv[1],
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt.system_prompt))
    user_prompt=sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]    
    if len(sys.argv) < 2:
        print("No input provided. Please provide a prompt as a command line argument.")
        sys.exit(1)
    if response.function_calls:
        for function_call_item in response.function_calls:
            print(f"Calling function: {function_call_item.name}({function_call_item.args})")
        if "--verbose" in sys.argv:
            print(f"User prompt: {user_prompt} \nFunction Called \nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    else:
        if "--verbose" in sys.argv:
            print(f"User prompt: {user_prompt} \nResponse: {response.text} \nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}") 
        else:
            print(response.text)

if __name__ == "__main__":
    main()
