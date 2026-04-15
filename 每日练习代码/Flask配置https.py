from flask import Flask

# 创建Flask应用实例
app = Flask(__name__)

# 定义一个简单的路由，测试HTTPS是否生效
@app.route('/')
def index():
    return "Hello, HTTPS!"

# 主程序入口
if __name__ == '__main__':
    # 配置HTTPS并启动服务
    # ssl_context参数传入 (证书文件路径, 私钥文件路径)
    try:
        app.run(
            host='0.0.0.0',  # 允许外部访问
            port=5000,       # 端口号
            ssl_context=('cert.pem', 'key.pem'),  # SSL证书和私钥路径
            debug=False      # 生产环境关闭debug模式
        )
    except FileNotFoundError as e:
        print("错误：找不到SSL证书文件！")
        print("请确认cert.pem和key.pem文件存在，且路径正确。")
        print("具体错误信息：", e)
    except Exception as e:
        print("启动失败，错误信息：", e)