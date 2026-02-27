from flask import Flask, request, jsonify # 导入Flask和request

import pymysql  # 导入PyMySQL模块

app = Flask(__name__)  # 创建Flask应用实例

DB_CONFIG = {  # 数据库配置：主机名，端口号，用户名，密码，数据库名，字符集，
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'user',
    'charset': 'utf8mb4'
}

@app.route('/unsafe_login', methods=['POST']) # 定义路由和请求方法post
def unsafe_login(): # 定义视图函数
    data = request.get_json() # 获取请求数据
    if not data or 'username' not in data or 'password' not in data: # 检查参数是否存在
        return jsonify({'code': 400, 'msg': '参数错误,请输入正确的用户名和密码'}),400  # 返回错误信息
    
    username = data['username']  # 获取用户名和密码
    password = data['password'] 

    sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'" # 拼接SQL语句
    print(f"输出拼接后的SQL语句：{sql}")

    try:
        conn = pymysql.connect(**DB_CONFIG) # 连接数据库
        cursor = conn.cursor(pymysql.cursors.DictCursor) # 创建游标，返回字典格式

        cursor.execute(sql) # 执行SQL语句
        user = cursor.fetchone() # 获取查询结果

        cursor.close() # 关闭游标
        conn.close() # 关闭连接

        if user:
            return jsonify({'code': 200, 'msg': '登录成功'}),200
        else:
            return jsonify({'code': 401, 'msg': '用户名或密码错误'}),401
    except Exception as e: # 捕获异常
        # 优化：把异常信息打印出来，方便调试（线上可注释，线下必加）
        print(f"服务器错误详情：{str(e)}") # 打印异常信息
        return jsonify({
            'code': 500,
            'msg': '服务器错误'
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True)