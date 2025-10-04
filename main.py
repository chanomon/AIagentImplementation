import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
#print(f"API Key: {api_key}") 

client = genai.Client(api_key=api_key)

model = "gemini-2.0-flash-001"
user_prompt = sys.argv[1]
#"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
if not user_prompt:
    print("Error: Something went wrong!", file=sys.stderr)
    sys.exit(1)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
response = client.models.generate_content(model=model,contents=messages)
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count
print(response.text)
if sys.argv[2]=="--verbose":
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


def main():
    print("Hello from llmagent!")


if __name__ == "__main__":
    main()
