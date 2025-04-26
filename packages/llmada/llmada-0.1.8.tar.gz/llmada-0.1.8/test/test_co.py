# pip install openai
from openai import OpenAI

# 配置客户端指向你的本地服务
client = OpenAI(
    base_url="http://localhost:8000/v1", # 关键：指向你的 FastAPI 服务
    api_key="12341234"   # 使用你在 .env 中设置的 key
)



# 非流式调用
try:
    completion = client.chat.completions.create(
        model="llama3_1", # 替换为你可用的模型
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is FastAPI?"}
        ],
        temperature=0.7,
    )
    print("Non-streaming response:")
    print(completion.choices[0].message.content)
    print(f"Usage: {completion.usage}")

except Exception as e:
    print(f"An error occurred (non-streaming): {e}")

print("\n---\n")





# 流式调用
try:
    stream = client.chat.completions.create(
        model="llama3_2", # 替换为你可用的模型
        messages=[
            {"role": "user", "content": "Write a haiku about Python."}
        ],
        stream=True,
    )
    print("Streaming response:")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print() # 换行
except Exception as e:
     print(f"An error occurred (streaming): {e}")

curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-dummy-key" \
  -d '{
    "model": "your-model-name-1",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello! How are you?"}
    ],
    "stream": false,
    "max_tokens": 50,
    "temperature": 0.7
  }'