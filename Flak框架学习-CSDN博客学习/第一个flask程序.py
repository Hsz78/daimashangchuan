#前提是要搭好虚拟环境
from flask import Flask #导入flask类

app = Flask(__name__) #实例化虚拟环境

@app.route('/') #使用的路由，给 hello 函数定义一个路由，然后通过浏览器通过http 请求得到相对的数据
def hello_world():
    return 'Hello,world' #输出

#核心补充, 启动flask的开发服务器
if __name__ == '__main__':
    #run（）方法启动服务器 debug=Ture开启调试模式（修改代码自动重启）
    app.run(debug=True)
