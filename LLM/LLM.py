import socket, openai,os

def get_local_project_name():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.basename(current_directory)

if __name__ == "__main__":
    project_name = get_local_project_name()
    print("Local name of the project:", project_name)

###################################
# Set your OpenAI API key
openai.api_key = "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"

# Example prompt
prompt = "fix this problem code from bandit usinig minimum words"

# Send a request to GPT-3.5 to complete the prompt
response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)

# Get the generated text from the response
generated_text = response['choices'][0]['text']
Fix_basedir = './LLM/Fix'

# Print the generated text
if __name__ == "__main__":
            directory_path = Fix_basedir
            output_path = Fix_basedir+"/Fix_results/"
            file_path=os.path.join(directory_path, "Fix_First")
            with open(file_path,"w") as file:
                file.write(generated_text)
        
