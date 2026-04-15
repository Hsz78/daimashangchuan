# 导入核心库：Flask（搭建web接口）、request（接收客户端数据）、jsonify（返回JSON格式）
from flask import Flask, request, jsonify
# 导入bcrypt库：专门用于密码加密/验证（教学点：不可逆加密）
import bcrypt  
# 导入pymysql库：用于连接MySQL数据库（教学点：数据库操作）
import pymysql  

# 初始化Flask应用实例（固定写法）
app = Flask(__name__)

# ===================== 基础配置（教学标注：仅改这里） =====================
# 数据库配置：仅需修改password为自己的MySQL密码
# 数据类型：字典（key为字符串，value为字符串/整数）
DB_CONFIG = {
    'host': 'localhost',      # 数据库地址：本地（固定）
    'port': 3306,             # 数据库端口：MySQL默认3306（整数）
    'user': 'root',           # 数据库用户名：默认root（字符串）
    'password': '123456',     # 数据库密码：改成自己的（字符串，教学重点修改项）
    'database': 'user',       # 数据库名：提前创建好的user库（字符串）
    'charset': 'utf8mb4'      # 字符集：支持中文/特殊字符（字符串）
}

# ===================== 1. 初始化数据表（教学标注：自动建表） =====================
def init_user_table():
    """
    函数作用：程序启动时自动创建user表，避免手动写SQL（教学点：表结构设计）
    表结构说明：
    - username：主键（唯一），VARCHAR(50)，存储用户名（字符串）
    - password：TEXT类型，存储加密后的密码（字符串，长度约60位）
    """
    # 建立数据库连接（数据类型：pymysql连接对象）
    conn = pymysql.connect(**DB_CONFIG)
    # 创建游标（用于执行SQL语句，数据类型：pymysql游标对象）
    cursor = conn.cursor()
    # 执行建表SQL（教学点：TEXT类型适配长加密串，VARCHAR存不下）
    create_sql = """
    CREATE TABLE IF NOT EXISTS user (
        username VARCHAR(50) NOT NULL PRIMARY KEY,  # 用户名：主键，唯一不重复
        password TEXT NOT NULL                      # 密码：TEXT类型存加密串
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(create_sql)
    # 提交操作（数据库修改必须提交）
    conn.commit()
    # 关闭游标和连接（释放资源，教学点：避免资源泄露）
    cursor.close()
    conn.close()
    print("✅ 数据表初始化成功（user表已创建/存在）")

# ===================== 2. 注册接口（加密存库，教学核心） =====================
@app.route('/register', methods=['POST'])  # 仅允许POST请求（教学点：接口请求方式）
def register():
    """
    接口作用：接收客户端明文密码，加密后存入数据库（教学点：密文存储）
    请求参数（JSON格式）：{"username": "用户名", "password": "明文密码"}
    返回结果（JSON格式）：{"msg": "提示信息"}
    """
    # 步骤1：接收客户端传的JSON数据（数据类型：字典）
    # request.get_json()：解析POST请求的JSON体（教学点：前后端数据交互格式）
    data = request.get_json()
    
    # 步骤2：参数校验（教学点：防空值、防参数缺失）
    if not data or 'username' not in data or 'password' not in data:
        # jsonify：返回JSON格式响应，400=参数错误（HTTP状态码）
        return jsonify({'msg': '❌ 参数错误：必须传username和password！'}), 400
    
    # 步骤3：提取参数并统一转字符串（教学点：兼容数字/字符串密码）
    # 数据类型：字符串（strip()去掉首尾空格，防用户误输入）
    username = str(data['username']).strip()
    plain_password = str(data['password']).strip()
    
    # 步骤4：空值二次校验（教学点：防空用户名/密码）
    if not username or not plain_password:
        return jsonify({'msg': '❌ 用户名/密码不能为空！'}), 400

    try:
        # 步骤5：密码加密（教学核心：bcrypt不可逆加密）
        # 5.1 明文转字节串（bcrypt要求输入为字节串，数据类型：bytes）
        plain_bytes = plain_password.encode('utf-8')
        # 5.2 生成随机盐值（数据类型：bytes，教学点：每个用户盐值唯一，更安全）
        salt = bcrypt.gensalt()  # gensalt()：默认生成12轮加密的盐值
        # 5.3 加盐加密（数据类型：bytes，教学点：明文+盐→密文，不可逆）
        hashed_bytes = bcrypt.hashpw(plain_bytes, salt)
        # 5.4 字节串转字符串（数据类型：字符串，教学点：方便存入数据库）
        hashed_password = hashed_bytes.decode('utf-8')

        # 步骤6：存入数据库（教学点：故意保留SQL注入漏洞）
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # 拼接SQL（教学核心：SQL注入漏洞演示点！不用参数化，方便演示注入）
        # 数据类型：字符串（f-string拼接，危险但适合教学）
        insert_sql = f"INSERT INTO user (username, password) VALUES ('{username}', '{hashed_password}')"
        print(f"📝 拼接后的注册SQL：{insert_sql}")  # 打印SQL，方便教学演示
        cursor.execute(insert_sql)
        conn.commit()  # 提交插入操作

        # 步骤7：关闭连接+返回成功
        cursor.close()
        conn.close()
        return jsonify({'msg': f'✅ 用户【{username}】注册成功！数据库存的是加密密码：{hashed_password}'}), 200

    # 异常处理1：用户名重复（主键冲突，教学点：主键唯一性）
    except pymysql.IntegrityError:
        return jsonify({'msg': f'❌ 用户名【{username}】已存在！'}), 409
    # 异常处理2：其他错误（教学点：异常捕获，方便调试）
    except Exception as e:
        print(f"❌ 注册错误详情：{str(e)}")  # 打印错误，教学时调试用
        return jsonify({'msg': '❌ 服务器错误！'}), 500

# ===================== 3. 登录接口（验证密文，教学核心） =====================
@app.route('/login', methods=['POST'])
def login():
    """
    接口作用：接收客户端明文密码，验证数据库中的密文密码（教学点：密文验证）
    请求参数（JSON格式）：{"username": "用户名", "password": "明文密码"}
    返回结果（JSON格式）：{"msg": "提示信息"}
    """
    # 步骤1：接收并解析JSON参数（同注册接口）
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'msg': '❌ 参数错误：必须传username和password！'}), 400
    
    # 步骤2：提取并统一转字符串（兼容数字密码）
    username = str(data['username']).strip()
    plain_password = str(data['password']).strip()

    try:
        # 步骤3：查询数据库中的加密密码（教学点：SQL注入漏洞演示点）
        conn = pymysql.connect(**DB_CONFIG)
        # cursor=DictCursor：查询结果返回字典（教学点：方便按字段名取值）
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 拼接SQL（故意留注入漏洞，教学演示用）
        select_sql = f"SELECT password FROM user WHERE username = '{username}'"
        print(f"📝 拼接后的登录SQL：{select_sql}")  # 打印SQL，方便演示注入
        cursor.execute(select_sql)
        # fetchone()：获取一条结果（数据类型：字典/None，教学点：None=用户不存在）
        user = cursor.fetchone()
        conn.close()  # 及时关闭连接

        # 步骤4：核心修改——注入演示专用逻辑（绕过所有验证）
        if user:  # 只要SQL查到用户（注入payload让条件为真），就直接登录成功
            return jsonify({'msg': f'✅ 用户【{username}】登录成功！'}), 200
        else:  # 没查到用户（正常情况），提示用户名错误
            return jsonify({'msg': '❌ 用户名错误！'}), 401

    # 异常处理：捕获所有错误（教学点：调试用）
    except Exception as e:
        print(f"❌ 登录错误详情：{str(e)}")
        return jsonify({'msg': '❌ 服务器错误！'}), 500

# ===================== 程序入口（固定写法） =====================
if __name__ == '__main__':
    # 启动前先初始化数据表（教学点：自动建表，无需手动操作）
    init_user_table()
    # 启动Flask服务（debug=True：调试模式，代码改了自动重启，教学方便）
    app.run(debug=True)