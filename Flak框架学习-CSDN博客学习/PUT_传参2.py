from flask import Flask, request #导入模块

app = Flask(__name__) #创建Flask应用实例

# 同时支持PUT和GET，方便浏览器测试
@app.route("/api/put", methods=["PUT", "GET"]) # 指定同时支持PUT和GET请求
def testPut(): # 处理函数
    name = request.args.get('name') # 获取name参数
    if not name: # 如果name参数为空
        return "请传入name参数，格式：http://127.0.0.1:5000/api/put?name=你好", 400 # 返回错误信息
    print(type(name)) # 打印参数类型
    return f"上传参数 {name}" # 返回参数值

if __name__ == '__main__':
    app.run()

# 浏览器测试：http://127.0.0.1:5000/api/put?name=你好



""" 
下面为另一种实现方式，单独写一个函数
from flask import Flask, request #导入模块

app = Flask(__name__) #创建Flask应用实例

# PUT传参——2 
@app.route("/api/put", methods=["PUT"]) # 指定只接受PUT请求
def testPut(): # 处理函数
    name = request.args.get('name') # 获取name参数
    print(type(name)) # 打印参数类型
    return f"上传参数 {name}" # 返回参数值

if __name__ == '__main__':
    app.run()

    验证方式为
复制下面的命令直接执行，这是 PowerShell 专属的 PUT 请求写法：
powershell
# 严格匹配代码规则：PUT方法 + 正确路径 + ?name=参数
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/put?name=你好" -Method PUT
"""
