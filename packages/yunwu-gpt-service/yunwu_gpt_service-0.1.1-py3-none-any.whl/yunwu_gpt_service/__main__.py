import os
import sys
import requests
import json

# 从环境变量获取API密钥，避免在代码中明文写死
API_KEY="sk-bNY36Va97vQ7FEqUu9gzg9UmiBgS399CPsDuILrPsKYqAfTu"

#API_KEY = os.environ.get("YUNWU_API_KEY")  # 部署时我们会在环境变量中配置这个值
API_ENDPOINT = "https://yunwu.ai/v1/chat/completions"
MODEL_NAME = "gpt-4o"  # 默认模型

# 构造请求头（与前面相同）
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def call_gpt_service(user_input: str) -> str:

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }
    try:
        resp = requests.post(API_ENDPOINT, headers=headers, json=data)
        print(f"[DEBUG] 当前读取到的API_KEY：{API_KEY}")

        if resp.status_code == 200:
            result = resp.json()
            # 提取返回的回复内容
            answer = result["choices"][0]["message"]["content"]
            return answer
        else:
            # 返回错误状态码和信息
            return f"[Error] API调用失败，状态码: {resp.status_code}, 响应: {resp.text}"
    except Exception as e:
        # 捕获其他异常
        return f"[Exception] 调用服务出错: {e}"

if __name__ == "__main__":
    print(f"[DEBUG] 当前读取到的API_KEY：{API_KEY}")

    # 读取标准输入（stdin）作为用户提问。
    # MCP服务在基础模式下每次调用会将请求内容通过STDIN传入。
    user_query = sys.stdin.read()
    if not user_query:
        # 如果没有读到输入，则使用一个默认提示（可选，便于测试）
        user_query = "你好"
    # 调用GPT接口获取回复
    output = call_gpt_service(user_query.strip())
    # 将结果输出到标准输出（stdout），供百炼平台读取
    print(output)
