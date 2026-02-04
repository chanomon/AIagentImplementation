from google.genai import types
from functions.config import WORKING_DIR
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    """
    Calls one of the four file operations functions based on the function call object.
    
    Args:
        function_call_part: A types.FunctionCall object with name and args properties
        verbose: If True, print detailed information about the function call
    
    Returns:
        types.Content object with the function response or error
    """
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_name = function_call_part.name
    
    # Dictionary mapping function names to their implementations
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    
    # Check if the requested function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Get the function to call
    function_to_call = function_map[function_name]
    
    # Add the working_directory argument to the args dictionary
    args_with_wd = dict(function_call_part.args)# function_call_part.args.copy() if function_call_part.args else {}
    args_with_wd["working_directory"] = WORKING_DIR
    
    try:
        # Call the function with the expanded arguments
        function_result = function_to_call(**args_with_wd)
        
        # Return the result as a types.Content object
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        # Return error as types.Content object
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing {function_name}: {str(e)}"},
                )
            ],
        )
