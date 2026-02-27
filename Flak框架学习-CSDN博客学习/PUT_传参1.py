from flask import Flask #导入模块

app = Flask(__name__) #创建Flask应用实例


@app.route("/api/put/<int:id>") # 指定参数类型为int
def testPut(id): # 参数名必须与路由中的一致
    print(type(id)) # 打印参数类型
    return f"上传参数 {id}" # 返回参数值

if __name__ == '__main__':
    app.run()

# 浏览器测试：http://127.0.0.1:5000/api/put/123
#直接在浏览器上测试