#!/usr/bin/python
import subprocess # 导入子进程模块
import sys # 导入系统模块

# ===================== 配置你的MySQL信息 =====================
MYSQL_USER = "root"          # 你的MySQL用户名
MYSQL_PASS = "123456"        # 你的MySQL密码
MYSQL_DB = "student_db"      # 要连接的数据库名
TABLE_NAME = "student_info"       # 要查询的表名（替换成你的实际表名）
# ============================================================

# 构造MySQL查询命令（和你在CMD里执行的格式一致） 
mysql_cmd = f'mysql -u{MYSQL_USER} -p{MYSQL_PASS} -D{MYSQL_DB} -e "SELECT * FROM {TABLE_NAME}"' 

try:
    # 执行MySQL查询命令
    result = subprocess.check_output( 
        mysql_cmd, # 替换成你的实际查询命令
        shell=True, # 使用shell执行
        # encoding="utf8",  # 删掉这行，因为gbk和utf8编码不兼容
        stderr=subprocess.STDOUT  # 捕获错误输出
    )
    
    # ========== 第2处修改：用gbk解码（Windows MySQL默认编码） ==========
    result = result.decode("gbk")  # 核心修改：把utf8换成gbk
    
    # 打印查询结果
    print("MySQL查询结果：")
    print("-" * 50)
    print(result)
    
except subprocess.CalledProcessError as e:
    # ========== 第3处修改：错误信息也用gbk解码 ==========
    error_output = e.output.decode("gbk")  # 新增：错误输出也适配gbk
    print(f"执行失败！错误信息：{error_output}")
    print("\n可能的原因：")
    print("1. MySQL服务未启动（执行net start mysql80）")
    print("2. 用户名/密码错误")
    print("3. 数据库/表名不存在")
    print("4. 未配置mysql环境变量（临时配置：set path=%path%;你的MySQL/bin路径）")
except Exception as e:
    print(f"其他错误：{str(e)}")

"""
MySQL-python 又叫 MySQLdb，
是 Python 连接 MySQL 最流行的一个驱动，
很多框架都也是基于此库进行开发，
遗憾的是它只支持 Python2.x，而且安装的时候有很多前置条件，
因为它是基于C开发的库，
在 Windows 平台安装非常不友好，经常出现失败的情况，
现在基本不推荐使用，取代的是它的衍生版本。
"""