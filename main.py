import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
function_name = response.function_calls[0].name
function_args = response.function_calls[0].args
if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Response: {response.text}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    if response.function_calls:
        print(f"Function call detected: '{function_name}' with args: {function_args}")
        print(response.text)
    else:
        print(response.text)
    

def main():
    print("Hello from ai-agent-project!")


if __name__ == "__main__":
    main()
