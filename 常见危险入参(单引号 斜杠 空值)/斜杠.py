# 斜杠（/ 或 \）：路径遍历 / 目录穿越攻击
#危害场景：当用户输入的路径包含../（上级目录）、/（根目录）时，可能访问到程序无权访问的文件。

# 假设程序想让用户读取./files/目录下的文件
filename = input("请输入要读取的文件名：")  # 恶意输入：../config/db_password.txt
file_path = f"./files/{filename}"
with open(file_path, "r") as f:
    print(f.read())
# 结果：用户本应只能读./files/下的文件，却读取了上级目录的密码文件
#进行了数据泄露，数据的越权

# 防护方法：
# 1. 限制路径的范围
# 2.过滤用户输入的特殊字符
import os
# 定义允许访问的根目录
ALLOWED_DIR = os.path.abspath("./files")

filename = input("请输入要读取的文件名：")
# 拼接路径并转为绝对路径
file_path = os.path.abspath(os.path.join(ALLOWED_DIR, filename))

# 检查路径是否在允许的目录内
if not file_path.startswith(ALLOWED_DIR):
    print("非法访问！")
else:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            print(f.read())
    else:
        print("文件不存在！")

#斜杠：主要引发路径遍历攻击，核心防护是限制访问目录 + 校验路径合法性；