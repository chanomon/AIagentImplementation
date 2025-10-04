# AI Agent Implementation
## Implementing a simple AI agent with gemini api
If you've ever used Cursor or Claude Code as an "agentic" AI editor, you'll understand what we're building in this project.

We're building a toy version of Claude Code using Google's free Gemini API! As long as you have an LLM at your disposal, its actually surprisingly simple to build a (somewhat) effective custom agent.
What Does the Agent Do?

The program we're building is a CLI tool that:

  1. Accepts a coding task (e.g., "strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽")
  2. Chooses from a set of predefined functions to work on the task, for example:
        - Scan the files in a directory
        - Read a file's contents
        - Overwrite a file's contents
        - Execute the python interpreter on a file
  3. Repeats step 2 until the task is complete (or it fails miserably, which is possible)

For example, I have a buggy calculator app, so I used my agent to fix the code:

    > uv run main.py "fix my calculator app, its not starting correctly"
    # Calling function: get_files_info
    # Calling function: get_file_content
    # Calling function: write_file
    # Calling function: run_python_file
    # Calling function: write_file
    # Calling function: run_python_file
    # Final response:
    # Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.

### Prerequisites

- Python 3.10+ installed (see the bookbot project for help if you don't already have it)
- uv project and package manager
- Access to a Unix-like shell (e.g. zsh or bash)

### Learning Goals

The learning goals of this project are:

- Introduce you to multi-directory Python projects
- Understand how the AI tools that you'll almost certainly use on the job actually work under the hood
- Practice your Python and functional programming skills

The goal is not to build an LLM from scratch, but to instead use a pre-trained LLM to build an agent from scratch.
Learning Goals

To run the model use:

    uv main.py "This is the prompt the model will receive"
    
## Gemini
Large Language Models (LLMs) are the fancy-schmancy AI technology that have been making all the waves in the AI world recently. Products like:

- ChatGPT
- Claude
- Cursor
- Google Gemini

... are all powered by LLMs. For the purposes of this course, you can think of an LLM as a smart text generator. It works just like ChatGPT: you give it a prompt, and it gives you back some text that it believes answers your prompt. We're going to use Google's Gemini API to power our agent in this course. It's reasonably smart, but more importantly for us, it has a free tier.
# Tokens

You can think of tokens as the currency of LLMs. They are the way that LLMs measure how much text they have to process. Tokens are roughly 4 characters for most models. It's important when working with LLM APIs to understand how many tokens you're using.

We'll be staying well within the free tier limits of the Gemini API, but we'll still monitor our token usage!

Be aware that all API calls, including those made during local testing, consume tokens from your free tier quota. If you exhaust your quota, you may need to wait for it to reset (typically 24 hours) to continue the lesson. Regenerating your API key will not reset your quota.
Tokens

You can think of tokens as the currency of LLMs. They are the way that LLMs measure how much text they have to process. Tokens are roughly 4 characters for most models. It's important when working with LLM APIs to understand how many tokens you're using.

We'll be staying well within the free tier limits of the Gemini API, but we'll still monitor our token usage!

Be aware that all API calls, including those made during local testing, consume tokens from your free tier quota. If you exhaust your quota, you may need to wait for it to reset (typically 24 hours) to continue the lesson. Regenerating your API key will not reset your quota.

## Assignment

> Create an account on Google AI Studio if you don't already have one

> Click the "Create API Key" button. [Here](https://ai.google.dev/gemini-api/docs/api-key) are the docs if you get lost.

If you already have a GCP account and a project, you can create the API key in that project. If you don't, AI studio will automatically create one for you.

Copy the API key, then paste it into a new .env file in your project directory. The file should look like this:

´GEMINI_API_KEY=your_api_key_here´

Add the ´.env´ file to your ´.gitignore´

> Update the main.py file. When the program starts, load the environment variables from the .env file using the dotenv library and read the API key:

    import os
    from dotenv import load_dotenv

    load_dotenv()  
    api_key = os.environ.get("GEMINI_API_KEY")

> Import the genai library and use the API key to create a new instance of a Gemini client:

    from google import genai

    client = genai.Client(api_key=api_key)

> Use the client.models.generate_content() method to get a response from the gemini-2.0-flash-001 model! You'll need to use two named parameters:

  model: The model name: gemini-2.0-flash-001 (this one has a generous free tier)
  contents: The prompt to send to the model (a string). For now, hardcode this prompt:

    "Why is the free internet such a great place to learn backend development? Use one paragraph maximum."

The generate_content method returns a GenerateContentResponse object. Print the .text property of the response to see the model's answer.

If everything is working as intended, you should be able to run your code and see the model's response in your terminal!

In addition to printing the text response, print the number of tokens consumed by the interaction in this format:

    Prompt tokens: X
    Response tokens: Y

The response has a .usage_metadata property that has both:

- a prompt_token_count property (tokens in the prompt)
- a candidates_token_count property (tokens in the response)

Run and submit the CLI tests.
    
    uv run main.py


## Input

We've hardcoded the prompt that goes to gemini, which is... not very useful. Let's update our code to accept the prompt as a command line argument.

We don't want our users to have to edit the code to change the prompt!
## Assignment

> Update your code to accept a command line argument for the prompt. For example:

    uv run main.py "Why are episodes 7-9 so much worse than 1-6?"

💡 The sys.argv variable is a list of strings representing all the command line arguments passed to the script. The first element is the name of the script, and the rest are the arguments. Be sure to import sys to use it.

If the prompt is not provided, print an error message and exit the program with exit code 1.
    uv run main.py "Why are episodes 7-9 so much worse than 1-6? Use one paragraph."

- Expecting exit code: 0

## Messages

LLM APIs aren't typically used in a "one-shot" manner, they work the same way ChatGPT works: in a conversation. 
The conversation has a history, and if we keep track of that history, then with each new prompt,
the model can see the entire conversation and respond within the larger context of the conversation.

## Roles

Importantly, each message in the conversation has a "role". In the context of a chat app like ChatGPT, your conversations would look like this:

    user: "What is the meaning of life?"
    model: "42"
    user: "Wait, what did you just say?"
    model: "42. It's is the answer to the ultimate question of life, the universe, and everything."
    user: "But why?"
    model: "Because Douglas Adams said so."

So, while our program will still be "one-shot" for now, let's update our code to store a list of messages in the conversation, and pass in the "role" appropriately.
## Assigning messages list


> Create a new list of types.Content, and set the user's prompt as the only message (for now):

    from google.genai import types
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

> Update your call to models.generate_content to use the messages list:

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

In the future, we'll add more messages to the list as the agent does its tasks in a loop.

## Verbose

As you debug and build your AI agent, you'll probably want to dump a lot more context into the console... but at the same time, we don't want to make the user experience of our CLI tool too noisy...

Let's add an optional command line flag, --verbose, that will allow us to toggle "verbose" output on and off. When we want to see more info, we'll just turn that bad boy on.
Assignment

> Add a new command line argument, --verbose. It should be supplied after the prompt if included. For example:

´uv run main.py "What is the meaning of life?" --verbose´

If the --verbose flag is included, the console output should include:
- The user's prompt: "User prompt: {user_prompt}"
- The number of prompt tokens on each iteration: "Prompt tokens: {prompt_tokens}"
- The number of response tokens on each iteration: "Response tokens: {response_tokens}"

Otherwise, it should not print those things.

 Run the CLI commands to test your solution:

- Command 1:

´uv run main.py "Why is the Holy Grail the best Monty Python movie? Use one paragraph." --verbose´
  
  Expecting stdout to contain all of:
    
    User prompt:
    Prompt tokens:
    Response tokens:

- Comand 2:
    
´uv run main.py "Why is the Holy Grail the best Monty Python movie? Use one paragraph."´
  
Expecting stdout to contain none of:
    
            User prompt:
            Prompt tokens:
            Response tokens:
