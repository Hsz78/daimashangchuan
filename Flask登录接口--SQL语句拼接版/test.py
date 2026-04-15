import requests

# 接口地址
url = "http://127.0.0.1:5000/unsafe_login"
# 要发送的参数（JSON格式）
data = {"username": "yzj", "password": "200821"}
# 发送 POST 请求（关键：用 post 方法）
res = requests.post(url, json=data)
# 打印结果
print(res.json())