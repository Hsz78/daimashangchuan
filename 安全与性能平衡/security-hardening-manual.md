# Flask + MySQL 安全加固手册 v1.0
作者：你的名字
日期：2026-04-15

## 一、安全配置
- 连接池：pool_size=10 max_overflow=20
- 限流：登录 5次/5分钟
- IP封禁：失败5次临时封禁15分钟
- Gunicorn timeout=30

## 二、应急命令
# 查看封禁IP
redis-cli keys "temp_ban:*"

# 解封
redis-cli del "temp_ban:127.0.0.1"

# 降级服务
redis-cli setex "service:degrade:recommend" 3600 1


你现在应该有这些文件：
locustfile.py（已有）
simulate_brute_force.py（新增）
test_circuit_breaker.py（你刚写的熔断器）
debug_pool.py（Flask 调试接口）
security-hardening-manual.md（手册）
start.sh（启动脚本）