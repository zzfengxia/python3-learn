import os
import yaml
import openai

"""
使用openai API的方式访问ChatGPT/azure GPT
"""
def set_env(cfg_file):
    with open(cfg_file) as f:
        config_data = yaml.safe_load(f)
        azure = config_data["azure"]
        if azure is not None:
            for k, v in azure.items():
                os.environ[k] = v
    os.environ['MY_VARIABLE'] = 'my_value'


def ai_chat(msgs=None):
    openai.api_type = "azure"

    openai.api_version = "2023-03-15-preview"
    openai.api_base = os.getenv("api-base")  # Your Azure OpenAI resource's endpoint value.
    openai.api_key = os.getenv("api-key")

    response = openai.ChatCompletion.create(
        # 报错：openai.error.InvalidRequestError: The API deployment for this resource does not exist
        # 解决：只能使用账号已经部署的模型，通过OpenAI Studio查看部署了哪些模型
        engine="gpt-35-turbo-test",  # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.

        # 目前只能通过每次请求上传已有上下文的方式来记忆上下文/多轮对话
        messages=msgs
    )

    print(response)

    print(response['choices'][0]['message']['content'])


if __name__ == '__main__':
    set_env('D:\\qiyu-work\\openaikey.yaml')
    messages = [
        # {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        #{"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "system", "content": "你现在是一名汽车4S店专业的销售顾问，客户咨询你价格，请把下面的话用可爱的语气表达出来，不要重复我说的话，回复不能超过30个字"},
        {"role": "user", "content": "价格会受多因素的影响实时发生变化，具体我让销售跟您聊哈"}
    ]
    ai_chat(messages)
