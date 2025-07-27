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

system_prompt = """You are a helpful coding assistant with access to file system tools. You can:

1. get_files_info() - Get information about files in the working directory
2. get_file_content(file_path) - Read the contents of a specific file
3. write_file(file_path, content) - Write content to a file
4. run_python_file(file_path) - Execute a Python file and see its output

When a user asks about code or files, you should:
1. First use get_files_info() to see what files are available
2. Use get_file_content() to examine relevant files
3. Provide detailed explanations based on the actual code you find

The working directory contains a calculator application. When users ask questions about "the calculator", they're referring to the files in this directory.

Always use your tools to investigate before answering questions about code or functionality."""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python,
        schema_get_file_content,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    function_args = function_call_part.args
    function_name = function_call_part.name
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
    
    if verbose == False:
        print(f"Calling function: {function_call_part.name}")
        

    if function_call_part.name in function_mapping:
        function_to_call = function_mapping[function_call_part.name]
        function_result = function_to_call(**args_with_working_directory)
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=function_name, response={"result": function_result})])

    else:
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=function_name, response={"error": f"Unknown function: {function_name}"})])



max_iterations = 20
for i in range(max_iterations):
    try:
        response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        
        for candidate in response.candidates:
            messages.append(candidate.content)
        
        has_function_calls = False
        for candidate in response.candidates:
            if candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_calls = True
                        function_call_part = part.function_call
                        function_name = function_call_part.name
                        function_args = function_call_part.args
                        tool_response = call_function(function_call_part, verbose=True)
                        messages.append(tool_response)


        if not has_function_calls and response.text:
            print("Final response:")
            print(response.text)
            break

    except Exception as e:
        print(f"Error occurred: {e}")
        break


if response.function_calls:
    function_call_result = call_function(response.function_calls[0], verbose)
    try:
        response_data = function_call_result.parts[0].function_response.response
        if response_data is None:
            raise Exception("Function call returned no response.")
    except (AttributeError, IndexError):
        raise Exception("Function call result missing expected response structure.")
    
          

         
    

def main():
    print("Hello from ai-agent-project!")


if __name__ == "__main__":
    main()
