from flask import Flask, request
from markupsafe import escape  # 放顶部导入
# 类型注解：标注核心对象的类型
app: Flask = Flask(__name__)

@app.route('/product')
def get_product() -> str:
    """获取商品信息接口，返回字符串响应"""
    # 1. 获取ID：request.args.get返回值类型为 字符串|None
    id: str | None = request.args.get('id')

    # 2. 先做参数校验（必须写在最前面！）
    if not id:
        return "参数不能为空"
    if not id.isdigit():
        return "id必须是数字"
    if len(id) > 10:
        return "id长度超出限制"

    # 3. 安全SQL：字符串类型
    sql: str = "SELECT * FROM products WHERE id = ?"

    # 4. 安全输出（防XSS）
    return escape(f"查询成功！ID：{id}，执行的SQL：{sql}")


@app.route('/about')
def about() -> str:
    """关于页面接口，返回静态HTML字符串"""
    return '<h1>这是静态页面</h1>'

if __name__ == '__main__':
    app.run(debug=True)