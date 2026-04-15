#GET_传参方法2

from flask import Flask,request #导入模块，request用于获取请求参数

app = Flask(__name__) #创建Flask应用实例


@app.route('/')#根路由
def home():#根路由对应的处理函数
    #输出内容
    return """ 
    这是根页面！
"""

@app.route("/api/get/<int:id>") # 指定参数类型为int，api/get/123 获取参数
def testGetPath(id): # 参数名必须与路由中的一致
    print(type(id)) # 打印参数类型
    return f"收到参数 {id}" # 返回参数值

if __name__ == '__main__':
    # 开启debug模式，方便开发时调试（修改代码自动重启，报错显示详细信息）
    app.run(debug=True)