from flask import Flask, request, jsonify# 导入模块，request用于获取请求参数

app = Flask(__name__) # 创建Flask应用实例


@app.route('/api/delete', methods=["DELETE"])    # 方式1, 指定只接受DELETE请求
def testDelete(): # 处理函数
    name = request.args.get('name') # 获取name参数
    print(name) # 控制台打印获取到的参数值
    return name + "是大哥！" # 返回参数值，加上大哥后缀

@app.route("/api/delete/<int:ID>", methods=["DELETE"])    #方式2
def testGetPath(ID): # 处理函数，接收路径参数ID
    print(type(ID)) # 打印参数类型
    return f"测试值为 {ID}" # 返回参数值，显示ID

if __name__ == '__main__':
    app.run()

# 方法一：
# # 发送DELETE请求，传name参数（方式1）
# Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/delete?name=张三" -Method DELETE
# 方法二：
# # 发送DELETE请求，传整数ID（方式2）
# Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/delete/123" -Method DELETE