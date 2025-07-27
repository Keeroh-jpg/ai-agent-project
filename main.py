import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
verbose = "--verbose" in sys.argv
client = genai.Client(api_key=api_key)
user_prompt = sys.argv[1]
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ]

if len(sys.argv) < 2:
    print("Error! Incorrect input. Usage: uv run main.py <prompt>")
    sys.exit(1)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python,
        schema_get_file_content,
        schema_write_file
    ]
)


response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

function_call_part = response.function_calls[0]
function_name = function_call_part.name
function_args = function_call_part.args



def call_function(function_call_part, verbose=False):
    args_with_working_directory = function_args.copy()
    args_with_working_directory["working_directory"] = "./calculator"
    function_mapping = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }
    if verbose == True:
        print(f"Calling function: {function_call_part.name} with args: {function_call_part.args}")
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name in function_mapping:
        
        
        function_to_call = function_mapping[function_call_part.name]
        function_result = function_to_call(**args_with_working_directory)
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=function_name, response={"result": function_result})])

    else:
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=function_name, response={"error": f"Unknown function: {function_name}"})])

    




if response.function_calls:
    function_call_result = call_function(response.function_calls[0], verbose)
    try:
        response_data = function_call_result.parts[0].function_response.response
        if response_data is None:
            raise Exception("Function call returned no response.")
    except (AttributeError, IndexError):
        raise Exception("Function call result missing expected response structure.")
    if verbose:
        print(f"-> {response_data}")  
          

         
    

def main():
    print("Hello from ai-agent-project!")


if __name__ == "__main__":
    main()
