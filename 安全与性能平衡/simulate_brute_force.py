# 暴力破解脚本（修复版）
import requests
import time 

# 你现在唯一可用的接口
TARGET = "http://127.0.0.1:5000/debug/db-pool"

print("开始模拟暴力破解...")

for i in range(20):
    try:
        # 改成 GET，因为你的接口只支持 GET！
        resp = requests.get(TARGET)
        
        # 只打印状态码，不解析json，绝对不报错
        print(f"第{i+1}次  | 状态码: {resp.status_code}  |  请求成功")
        
    except Exception as e:
        print(f"第{i+1}次  | 请求失败：{e}")
        
    time.sleep(0.5)