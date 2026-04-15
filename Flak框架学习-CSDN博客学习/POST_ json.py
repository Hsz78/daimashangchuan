from flask import Flask, request, jsonify # 导入模块，request用于获取请求参数

app = Flask(__name__) # 创建Flask应用实例

class Student(): # 定义Student类

    def __init__(self, id, name, age): # 初始化方法
        self.id = id # id
        self.name = name # 名字
        self.age = age # 年龄

# toString
def __repr__(self): # 返回对象的字符串表示
        return f"Student[id={self.id},name={self.name},age={self.age}]" # 返回字符串
@app.route("/api/post/json",methods=["POST"]) # 指定只接受POST请求
def testPostJson(): # 处理函数
    if not request.is_json: # 判断请求体是否是JSON格式
        return jsonify({"code": 400, "msg": "请求体必须是JSON格式！"}), 400 # 返回错误信息

    id = request.json.get("id","")   # 获取id
    name = request.json.get("name","") # 获取name
    age = request.json.get("age",0)  # 获取age
    stu = Student(id,name,age) # 创建Student对象
    print(stu) # 打印对象
    return "测试OK了！"
    
if __name__ == '__main__':
    app.run()

