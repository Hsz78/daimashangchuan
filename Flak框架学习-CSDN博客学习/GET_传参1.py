# GET传参的方式1
from flask import Flask, request  # 导入模块，request用于获取请求参数

app = Flask(__name__)

# 显式指定只接受GET请求，更规范
@app.route('/api/get', methods=['GET'])
def testGet():
    # 修复核心问题：给get方法加默认值，避免参数为空时name=None
    name = request.args.get('name', '默认用户')
    
    # 移除无效的('name')行
    print(name)  # 控制台打印获取到的参数值
    
    # 字符串拼接（此时name一定有值，不会报NoneType错误）
    return f"{name}是大哥！"

# 补充根路由，避免访问/时报404（可选但友好）
@app.route('/')
def index():
    return "请访问 /api/get?name=你的名字 测试GET传参，例如：/api/get?name=张三"

if __name__ == '__main__':
    # 开启debug模式，方便开发时调试（修改代码自动重启，报错显示详细信息）
    app.run(debug=True)