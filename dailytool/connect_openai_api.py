import os
import openai

"""
使用openai API的方式访问ChatGPT/azure GPT
"""
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = os.getenv("OPENAI_API_BASE")  # Your Azure OpenAI resource's endpoint value.
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    engine="gpt-35-turbo", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
)

print(response)

print(response['choices'][0]['message']['content'])