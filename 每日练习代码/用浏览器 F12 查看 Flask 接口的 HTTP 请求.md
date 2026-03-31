📝 F12 查看 HTTP 请求速记笔记（全）
一、核心操作三步法
打开监控：按 F12 → 切换到「网络 (Network)」标签页 → 勾选「保留日志 (Preserve log)」。
触发请求：在地址栏输入接口地址，或点击页面按钮 / 提交表单。
查看详情：点击 Network 列表中的请求记录，重点分析 Headers、Payload、Response 三部分。
二、Network 列表速记
表格
列名	含义	速记
名称	请求的接口地址或资源路径	看接口名，如 /api/hello
状态	HTTP 状态码	200 = 成功，404 = 找不到，500 = 服务器错
类型	请求 / 资源类型	xhr/fetch= 接口，script=JS，img= 图片
时间	请求耗时	越小越快
三、Headers 详情速记（最核心）
1. 常规信息
请求 URL：协议://域名/路径?参数，如 https://www.baidu.com/sugrec?wd=flask
请求方法：
GET：获取数据，参数在 URL 里
POST：提交数据，参数在请求体里
状态代码：200 OK 表示成功。
2. Request Headers（你发给服务器的）
表格
字段	含义	速记
Host	目标服务器域名	告诉服务器 “你找谁”
User-Agent	浏览器 / 系统信息	告诉服务器 “我是谁”
Content-Type	请求体格式	application/json=JSON，x-www-form-urlencoded= 表单
Cookie	本地存储的用户信息	服务器用来 “认出你”
Referer	来源页面	告诉服务器 “我从哪来”
3. Response Headers（服务器发给你的）
表格
字段	含义	速记
Content-Type	响应体格式	application/json=JSON，text/html= 网页
Content-Length	响应体大小	单位字节
Set-Cookie	服务器要求设置的 Cookie	下次请求自动带上
四、Payload 速记（你传了什么）
GET 请求：参数在 URL 里，在 Query String Parameters 中查看，如 wd=flask。
POST 请求：
Form Data：表单格式，如 name=小明&age=18。
Request Payload：JSON 格式，如 {"name":"小明", "age":18}。
五、Response 速记（服务器返回了什么）
Preview：格式化预览，JSON 会自动排版，方便阅读。
Response：原始响应内容，即服务器返回的字符串。
六、对应 Flask 接口速记
表格
部分	百度接口示例	Flask 接口示例
请求 URL	https://www.baidu.com/sugrec?wd=flask	http://127.0.0.1:5000/api/hello?name=小明
Host	www.baidu.com	127.0.0.1:5000
请求方法	GET	GET 或 POST
状态码	200 OK	200 OK
Payload	wd=flask	name=小明 或 {"age":18}
Response	联想词 JSON	{"code":200, "msg":"Hello 小明"}
七、常见状态码速记
200：✅ 请求成功
404：❌ 接口地址不存在
400：❌ 请求参数错误
401：🔒 未授权，需要登录
500：🔥 服务器内部错误（代码有问题）