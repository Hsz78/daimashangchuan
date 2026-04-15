#向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。
# 数据被包含在请求体中。POST
# 请求可能会导致新的资源的建立和/或已有资源的修改。

from flask import Flask, request,jsonify # 导入模块，request用于获取请求参数

app = Flask(__name__)   #创建Flask应用实例

@app.route('/')#根路由
def home():#根路由对应的处理函数
    #输出内容
    return """ 
    这是根页面！
    请访问 /api/post/form 提交POST请求
"""
#post from-data
@app.route('/api/post/form', methods=['POST']) # 指定只接受POST请求
def testPost(): # 处理函数
    print("收到POST请求，开始解析参数")
    username = request.form.get('username', '默认用户') # 获取表单名字
    password = request.form.get('password', '默认密码') # 获取表单密码
    print(f"用户：{username}，密码：{password}") #输出
    data = { # 返回数据
        'username': username, # 返回名字
        'password': password  # 返回密码     
    }
    return jsonify(data) # 返回数据

if __name__ == '__main__': # 入口函数
    app.run(debug=True)#开启debug模式，方便开发时调试（修改代码自动重启，报错显示详细信息）