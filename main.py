import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from google.genai import errors
from  prompts import system_prompt
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from call_function import call_function

verbose = False


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    #print(f"API Key: {api_key}") 

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    #user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    if not user_prompt:
        print("Error: Something went wrong!", file=sys.stderr)
        sys.exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    #response = client.models.generate_content(model=model,contents=messages)
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file],
    )
    final_answer_ready = False
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model=model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),#types.GenerateContentConfig(system_instruction=system_prompt),
            )
            if final_answer_ready:
                print("final response:")
                print(...)
                return


        
        except errors.ClientError as e:
            print("Model call failed:",e)
            #return
            continue
        ###checking candidates content of the response and appendig to messages
        for candidates in response.candidates:
            messages.append(candidates.content)

        #prompt_tokens = response.usage_metadata.prompt_token_count
        #response_tokens = response.usage_metadata.candidates_token_count
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                function_call_result = call_function(function_call, verbose=verbose)
                
                # Check if the result has the expected structure
                if (not function_call_result.parts or 
                    not function_call_result.parts[0].function_response or
                    not function_call_result.parts[0].function_response.response):
                    raise ValueError(f"Invalid function call response structure: {function_call_result}")
                

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                function_responses.append(function_call_result.parts[0])#.function_response.response)
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(response.text)
            final_answer_ready = True
            break
        #if sys.argv[2]=="--verbose":
        #    print(f"User prompt: {user_prompt}")
        #    print(f"Prompt tokens: {prompt_tokens}")
        #    print(f"Response tokens: {response_tokens}")
        #print(response.text)


        

        #if not response.functions_calls:
        #    print(response.text)
        #    break
    if not final_answer_ready:#response.functions_calls:
        print("The maximum number of iterations was reached and the model still hasn't producen a final response")
        sys.exit(1)
#def main():
#    print("Hello from llmagent!")


if __name__ == "__main__":
 
    main()
