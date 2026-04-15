# 导入Flask核心模块：Flask（创建应用）、request（接收前端参数）、jsonify（返回JSON格式）
from flask import Flask, request, jsonify
# 导入PyMySQL模块：用于连接MySQL数据库
import pymysql  

# 创建Flask应用实例，__name__是Python内置变量，代表当前文件名称
app = Flask(__name__)  

# ====================== 数据库配置项（根据你的实际MySQL修改） ======================
MYSQL_CONFIG = {
    "host": "localhost",    # 本地MySQL服务器地址（默认localhost）
    "user": "root",         # MySQL登录用户名（默认root）
    "password": "123456",   # MySQL登录密码（替换成你的实际密码）
    "database": "user",     # 要连接的数据库名（需提前创建）
    "charset": "utf8mb4"    # 字符集，防止中文乱码（必加）
}

# ====================== 1. 特殊字符过滤函数（核心防SQL注入/XSS） ======================
def filter_special_char(text):
    """
    过滤SQL注入、XSS攻击的危险字符
    :param text: 要过滤的字符串（如用户名、密码）
    :return: 过滤后的安全字符串
    """
    # 处理None值：如果传入的是空，直接返回空字符串，避免后续报错
    if text is None:
        return ""
    # 统一转成字符串类型：即使传入数字（如age=18），也转成字符串处理
    text = str(text)

    # 定义需要过滤的危险字符字典：键=危险字符，值=替换后的内容（空字符串=删除）
    replace_dict = {
        "'": "",    # 单引号（SQL注入核心字符，删除）
        '"': "",    # 双引号（防止闭合SQL语句）
        ';': "",    # 分号（截断SQL语句，防止注入后续指令）
        '--': "",   # SQL注释符（防止注释掉后续SQL）
        '/*': "",   # SQL多行注释符（防止注入）
        '*/': "",   # SQL多行注释符（防止注入）
        '<': "",    # 左尖括号（防止XSS跨站脚本攻击）
        '>': "",    # 右尖括号（防止XSS跨站脚本攻击）
        'or': "",   # or关键字（防止 or 1=1 注入）
        'AND': "",  # AND关键字（防止 AND 1=1 注入）
        '=': ""     # 等号（防止拼接注入）
    }
    # 遍历字典，逐个替换危险字符
    for bad_char, good_char in replace_dict.items():
        text = text.replace(bad_char, good_char)

    # 去掉字符串首尾的空格（如输入" 小明  " → 变成"小明"）
    text = text.strip()
    # 【修复】函数必须有返回值！你之前漏掉了这行，导致过滤后的值无法返回
    return text

# ====================== 2. 非空校验函数（确保必填参数不为空） ======================
def check_required_params(params, required_list):
    """
    校验接口必填参数是否为空
    :param params: 接口接收的所有参数（字典格式）
    :param required_list: 必填参数列表（如['username', 'password']）
    :return: (校验结果, 错误信息) → (True/False, 字符串)
    """
    # 遍历每个必填参数，逐个检查
    for param_name in required_list:
        # 校验逻辑：1.参数不存在 2.参数值是空字符串 3.参数值是全空格
        if param_name not in params or not str(params[param_name]).strip():
            # 只要有一个参数不满足，返回“失败”+具体错误信息
            return False, f"参数 {param_name} 不能为空！"
    
    # 所有必填参数都满足，返回“成功”+提示语
    return True, "校验通过"

# ====================== 3. 获取数据库连接（优化版） ======================
def get_db_conn():
    """
    安全获取MySQL数据库连接
    :return: 连接对象（成功）/ None（失败）
    """
    try:
        # 建立数据库连接（解包配置字典）
        conn = pymysql.connect(**MYSQL_CONFIG)
        # 【修复】原代码多了空格，且游标应在使用时创建，这里只返回连接
        # conn .cursor(...) → 去掉空格，且无需在这里创建游标
        return conn  
    except Exception as e:  # 捕获所有连接异常（如密码错误、数据库不存在）
        print(f"数据库连接失败：{str(e)}")  # 打印异常信息，方便调试
        return None  # 连接失败返回None

# ====================== 4. 核心接口：用户登录查询（带过滤+防注入） ======================
@app.route('/user/login', methods=['POST'])  # 接口路径：http://127.0.0.1:5000/user/login，仅支持POST请求
def test_api():
    """
    用户登录查询接口
    入参：JSON格式 → {"username": "用户名", "password": "密码"}
    功能：1.非空校验 2.特殊字符过滤 3.安全查询数据库 4.返回登录结果
    """
    # 步骤1：接收前端传入的JSON参数（如果没传参数，返回空字典）
    params = request.get_json() or {}
    print(f"【调试】接口原始入参：{params}\n")  # 打印原始参数，方便调试

    # 步骤2：定义该接口的必填参数（登录必须传用户名和密码）
    required_params = ['username', 'password']

    # 步骤3：执行非空校验
    is_valid, msg = check_required_params(params, required_params)
    if not is_valid:  # 校验失败
        # 返回400错误（请求参数错误）+错误信息
        return jsonify({'code': 400, 'msg': msg}), 400

    # 步骤4：对用户名/密码做特殊字符过滤（核心！防止注入）
    # 【修复】先把过滤后的值赋值给变量，方便后续使用
    username = filter_special_char(params['username'])
    password = filter_special_char(params['password'])
    print(f"【调试】过滤后参数 → 用户名：{username}，密码：{password}\n")

    # 步骤5：执行数据库查询（核心防注入：参数化查询）
    try:
        # 获取数据库连接
        conn = get_db_conn()
        if not conn:  # 连接失败
            return jsonify({'code': 500, 'msg': '数据库连接失败'}), 500
        
        # 定义SQL语句：用%s占位符（参数化查询），绝对不要字符串拼接！
        sql = "SELECT * FROM user WHERE username=%s AND password=%s"
        print(f"【调试】待执行的SQL：{sql} → 参数：({username}, {password})\n")

        # 创建游标（DictCursor：查询结果返回字典格式，方便取值）
        # with语句：自动关闭游标，无需手动close
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 执行SQL：把过滤后的参数传入（第二个参数是元组，必须和%s数量对应）
            cursor.execute(sql, (username, password))
            # 获取查询结果（只取第一条，因为用户名唯一）
            user = cursor.fetchone()  

        # 步骤6：关闭数据库连接（用完必须关，避免资源泄露）
        conn.close()

        # 步骤7：根据查询结果返回登录状态
        if user:  # 查询到用户（用户名密码正确）
            return jsonify({
                'code': 200,
                'msg': '登录成功',
                'data': user  # 返回用户信息（测试用，生产环境可隐藏密码）
            }), 200  # 200：请求成功
        else:  # 未查询到用户（用户名/密码错误）
            return jsonify({'code': 401, 'msg': '用户名或密码错误'}), 401  # 401：未授权

    except Exception as e:  # 捕获查询过程中的所有异常（如SQL语法错、表不存在）
        print(f"【调试】接口执行异常：{str(e)}")  # 打印异常详情，方便调试
        # 返回500错误（服务器内部错误）
        return jsonify({'code': 500, 'msg': '服务器内部错误'}), 500

# ====================== 启动应用 ======================
if __name__ == '__main__':
    # 启动Flask服务：debug=True（代码修改自动重启），端口5000，允许本地访问
    app.run(debug=True, port=5000, host='127.0.0.1')