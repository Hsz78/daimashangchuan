# 导入需要的模块（注意：没有text这个模块，删掉）
from flask import Flask, request, jsonify

# 初始化 Flask 应用
app = Flask(__name__)

# ======================
# 1. 最简单的特殊字符过滤函数
# 功能：把最危险的几个特殊字符替换掉
# ======================
def filter_special_char(text):
    """
    过滤特殊字符（新手版）
    :param text: 要过滤的字符串
    :return: 过滤后的字符串
    """
    # 如果传入的是None(空)，则返回空字符串，避免报错
    if text is None:
        return ""
    # 把非字符串类型（比如数字）转成字符串
    text = str(text)

    # 定义需要替换的危险字符（只保留最常见的几个）
    # 左边是要替换的字符，右边是替换成的内容
    replace_dict = {
        '<': '',  # 左尖括号直接删掉（防止XSS攻击）
        '>': '',  # 右尖括号直接删掉
        "'": '',  # 单引号直接删掉（防止SQL注入）
        '"': '',  # 双引号直接删掉
        ';': ''   # 分号直接删掉
    }
    # 逐个替换字符（你之前写的是“逐渐”，笔误）
    for bad_char, good_char in replace_dict.items():
        text = text.replace(bad_char, good_char)

    # 去掉字符串两端的空格
    text = text.strip()
    # 函数必须有返回值（你之前漏掉了这行）
    return text

# ======================
# 2. 最简单的非空校验函数
# 功能：检查必填参数是否为空
# ======================
def check_required_params(params, required_list):
    """
    校验必填参数（新手版）
    :param params: 接口收到的所有参数（字典）
    :param required_list: 需要校验的必填参数列表
    :return: 校验结果（True/False）和错误信息
    """
    # 遍历每个必填参数
    for param_name in required_list:
        # 检查：1. 参数不存在  2. 参数值是空字符串  3. 参数值是全空格
        if param_name not in params or params[param_name] == "" or str(params[param_name]).strip() == "":
            # 只要有一个参数不满足，就返回失败和错误信息
            return False, f"参数 {param_name} 不能为空！"
    
    # 所有参数都满足，返回成功
    return True, "校验通过"

# ======================
# 3. 最简单的测试接口
# ======================
@app.route('/test', methods=['POST'])  # 只支持 POST 请求
def test_api():
    """新手测试接口：只处理 JSON 入参，逻辑极简"""
    # 第一步：获取接口传入的 JSON 参数（如果没有，返回空字典）
    # request.get_json() 是 Flask 获取 JSON 入参的核心方法
    params = request.get_json() or {}

    # 第二步：定义必填参数列表（变量名改得更语义化）
    required_params = ['name', 'age']

    # 第三步：执行非空校验
    is_valid, msg = check_required_params(params, required_params)
    if not is_valid:
        # 返回错误时也要带状态码400，符合HTTP规范
        return jsonify({'code': 400, 'msg': msg}), 400
    
    # 第四步：执行特殊字符过滤
    params['name'] = filter_special_char(params['name'])
   
    # 第五步：返回结果
    return jsonify({
        'status': 'success',
        'msg': '参数校验和过滤成功！',
        'data': {
            '过滤后的姓名': params['name'],
            '年龄': params['age']
        }
    }), 200

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)  # debug=True 可以实时看到代码修改效果