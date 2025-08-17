from functions.get_files_info import *
from google import genai
from google.genai import types
import os

FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part: types.FunctionCall, verbose=False):
    function_name = function_call_part.name
    args = dict(function_call_part.args)

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")
    
    args["working_directory"] = "./calculator"
    fn = FUNCTIONS.get(function_name)
    if not fn:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )
    result = fn(**args)

    if verbose:
        print(f" -> {result}")

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result}
            )
        ]
    )