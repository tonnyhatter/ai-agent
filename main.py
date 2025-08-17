import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import system_prompt
from functions.get_files_info import *
from functions.functioncall import call_function

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
    if len(sys.argv) < 2:
        print("No input provided. Please provide a prompt as a command line argument.")
        sys.exit(1)
    is_verbose = "--verbose" in sys.argv
    user_prompt=sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
    for i in range(20):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt.system_prompt))
        candidate = response.candidates[0]
        if hasattr(candidate, "content"):
            messages.append(candidate.content)
        if getattr(response, "function_calls", None):
            for function_call_item in response.function_calls:
                function_call_item.args["working_directory"] = "./calculator"
                args_required = {"run_python_file", "wrie_file"}
                if function_call_item.name in args_required:
                    function_call_item.args.setdefault("args", [])
                fn_result = call_function(function_call_item, is_verbose)
                if (
                    not fn_result.parts 
                    or not isinstance(fn_result.parts, list)
                    or len(fn_result.parts) == 0
                    or not hasattr(fn_result.parts[0], "function_response")
                    or not hasattr(fn_result.parts[0].function_response, "response")
                ):
                    raise Exception("Unexpected response structure from function call.")    
                function_result = fn_result.parts[0].function_response.response["result"]
                tool_message = types.Content(
                    role="user",
                    parts=[types.Part(text=function_result)]
                )       
                messages.append(tool_message)
        elif getattr(response, "text", None):
            if "--verbose" in sys.argv:
                print(f"User prompt: {user_prompt} \nResponse: {response.text} \nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}") 
            else:
                print(response.text)
            break
        else:
            print("The agent reached the maximum number of steps without producing a final answer. Something may have gone wrong.")

if __name__ == "__main__":
    main()
