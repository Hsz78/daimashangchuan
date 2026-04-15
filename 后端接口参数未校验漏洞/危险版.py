# 导入Flask框架核心模块：
# Flask：创建web应用实例
# request：接收前端传的参数
# jsonify：返回JSON格式的响应
from flask import Flask, request, jsonify, make_response  # 新增make_response

# 创建Flask应用实例，__name__是固定参数，代表当前文件
app = Flask(__name__)

# 关键配置：关闭JSON的ASCII编码，让返回的中文正常显示（解决昵称问号问题）
app.config['JSON_AS_ASCII'] = False

# 模拟数据库：用字典存储用户信息
# 键（key）=用户ID（user_id），值（value）=用户详情（包含昵称）
fake_db = {
    1: {"nickname": "张三"},  # 用户1：ID=1，昵称=张三
    2: {"nickname": "李四"}   # 用户2：ID=2，昵称=李四
}

# 新增：查询昵称接口（用来验证修改结果）
@app.route('/get_nickname', methods=['GET'])
def get_nickname():
    # 获取要查询的用户ID
    user_id = request.args.get('user_id')
    # 校验是否为数字（简单处理，避免报错）
    if not user_id or not user_id.isdigit():
        return jsonify({"msg": "请传正确的user_id（数字）"}), 400
    user_id = int(user_id)
    # 查数据库，返回当前昵称
    if user_id in fake_db:
        response = make_response(jsonify({
    "msg": "查询成功",
    "user_id": user_id,
    "current_nickname": fake_db[user_id]['nickname']
}))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# 定义修改昵称接口：
# @app.route：路由装饰器，指定接口地址和请求方式
# /update_nickname：接口访问地址
# methods=['POST']：只接受POST请求（改数据常用POST）
@app.route('/update_nickname', methods=['POST'])
def update_nickname():
    # 1. 直接获取前端传的参数，无任何校验（漏洞核心）
    # request.form.get('user_id')：获取前端表单里的user_id参数
    # int()：转成数字（前端传的是字符串，要转成数字才能匹配数据库的键）
    user_id = int(request.form.get('user_id'))
    # 获取前端传的新昵称，不校验是否为空、长度、特殊字符
    new_nick = request.form.get('new_nick')
    
    # 2. 直接修改数据库，无权限校验（漏洞核心）
    # 不管当前登录的是谁，传哪个user_id就改哪个用户的昵称
    fake_db[user_id]['nickname'] = new_nick
    
    # 3. 返回修改结果：jsonify把字典转成JSON格式返回给前端
    return jsonify({
        "msg": "改好了",       # 提示信息
        "user_id": user_id,    # 新增：明确显示修改的是哪个用户
        "new_nickname": new_nick  # 新增：明确显示改成了什么昵称
    })

# 程序入口：启动Flask应用
# debug=True：调试模式，代码改了会自动重启（开发用，生产环境要关掉）
if __name__ == '__main__':
    app.run(debug=True)

#简单来说只是不进行参数校验，直接获取参数，然后进行修改，
#谁都可以修改可以登录的用户的昵称，1可以改成2，2可以改成1，名字可以被修改，简单易懂