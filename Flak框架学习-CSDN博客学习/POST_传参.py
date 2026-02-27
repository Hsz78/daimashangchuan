# 专门测试POST接口的代码
import requests

# 目标接口地址（和你的路由一致）
url = "http://127.0.0.1:5000/api/post/json"
# 要发送的表单参数
test_data = {
    "id": "1",
    "name": "yzj",
    "age": "18"
}

# 关键：发送POST请求（不是GET！）
try:
    # 仅增加超时设置，其余不变
    response = requests.post(url, data=test_data, timeout=10)
    print("✅ 请求成功！")
    print("状态码：", response.status_code)
    print("返回数据：", response.json())
except requests.exceptions.ConnectionError:
    # 只加这个针对性提示，其余异常保留你原来的写法
    print("❌ 连接失败！请先确认Flask服务是否已启动（终端有没有显示Running on http://127.0.0.1:5000）")
except Exception as e:
    print("❌ 请求失败：", e)