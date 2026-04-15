from flask import Flask, request, jsonify # 导入模块，request用于获取请求参数

app = Flask(__name__) # 创建Flask应用实例

class Student(): # 定义Student类

    def __init__(self, id, name,age): # 初始化方法
        self.id = id # id
        self.name = name # 名字
        self.age = age # 年龄

    def __repr__(self): # 返回对象的字符串表示
        return f"Student[id={self.id},name={self.name},age={self.age}]" # 返回字符串
@app.route("/api/put/json", methods=["PUT"]) # 指定只接受PUT请求
def testPutJson(): # 处理函数
    id = request.json.get("id") # 获取id
    name = request.json.get("name") # 获取name
    age = request.json.get("age") # 获取age
    stu = Student(id, name, age) # 创建Student对象
    print(stu) # 打印对象
    return f"PUT传json测试成功！ 数据是：id={id},name={name},age={age}"
    
if __name__ == '__main__':
    app.run()

"""
PUT请求示例
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/put/json" `
  -Method PUT `
  -ContentType "application/json" `
  -Body '{"id": 1, "name": "张三", "age": 18}'
"""