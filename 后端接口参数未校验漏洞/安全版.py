from flask import Flask, request, jsonify, make_response # 新增make_response

app = Flask(__name__)
# 解决中文显示问题
app.config['JSON_AS_ASCII'] = False

# 模拟数据库：新增token字段（代表用户登录令牌，相当于登录密码）
# token=tk1 → 对应用户1；token=tk2 → 对应用户2
fake_db = {
    1: {"nickname": "张三", "token": "tk1"},
    2: {"nickname": "李四", "token": "tk2"}
}

# 新增：查询昵称接口（用来验证修改结果）
@app.route('/get_nickname', methods=['GET'])
def get_nickname():
    user_id = request.args.get('user_id')
    if not user_id or not user_id.isdigit():
        return jsonify({"msg": "请传正确的user_id（数字）"}), 400
    user_id = int(user_id)
    if user_id in fake_db:
        # 手动指定编码，避免乱码
        response = make_response(jsonify({
            "msg": "查询成功",
            "user_id": user_id,
            "current_nickname": fake_db[user_id]['nickname']
        }))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    else:
        return jsonify({"msg": "用户不存在"}), 404

@app.route('/update_nickname', methods=['POST'])
def update_nickname():
    # 1. 获取所有参数（新增token，代表当前登录用户）
    token = request.form.get('token')
    user_id = request.form.get('user_id')
    new_nick = request.form.get('new_nick')

    # 2. 第一步校验：参数不能为空
    if not (token and user_id and new_nick):
        return jsonify({"msg": "参数不能空"}), 400

    # 3. 第二步校验：user_id必须是数字
    if not user_id.isdigit():
        return jsonify({"msg": "用户ID必须是数字"}), 400
    user_id = int(user_id)

    # 4. 第三步校验：权限核心！根据token找当前登录用户
    current_user_id = None
    for uid, info in fake_db.items():
        if info['token'] == token:
            current_user_id = uid
            break

    # 5. 验证：只能改自己的昵称（操作人=被操作人）
    if current_user_id != user_id:
        # 手动指定编码，返回中文无乱码
        response = make_response(jsonify({"msg": "不能改别人的昵称"}))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    # 6. 所有校验通过，才修改昵称
    fake_db[user_id]['nickname'] = new_nick

    # 7. 返回结果（无乱码）
    response = make_response(jsonify({
        "msg": "改好了",
        "user_id": user_id,
        "new_nickname": new_nick
    }))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True)

'''
安全版核心修复点：新增token校验，通过token找到「当前登录用户」，只有「登录用户 ID」和「要修改的用户 ID」一致时，才允许修改；
漏洞修复效果：越权操作（改别人）被拒绝，合法操作（改自己）正常执行；
后端安全原则：所有涉及用户数据的操作，必须做「身份绑定校验」，这是防越权攻击的核心。
'''