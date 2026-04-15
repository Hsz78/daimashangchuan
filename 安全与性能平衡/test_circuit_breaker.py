import time 

class CircuitBreaker:
    def __init__(self, name, failure_threshold=3, recovery_timeout=5):
        self.name = name
        self.failure_threshold = failure_threshold  # 失败几次熔断
        self.recovery_timeout = recovery_timeout    # 冷却几秒
        self.state = "CLOSED"                      # 当前状态：关闭/开启/半开
        self.failure_count = 0                     # 失败次数
        self.last_failure_time = 0                 # 最后失败时间

    def call(self, func):
        # ======================
        # 状态1：熔断器开启（OPEN）
        # ======================
        if self.state == "OPEN":
            # 冷却时间到了 → 进入半开
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("熔断器已开启，拒绝请求")

        # ======================
        # 执行业务逻辑
        # ======================
        try:
            result = func()
            # 成功 → 重置错误次数，关闭熔断器
            self.failure_count = 0
            self.state = "CLOSED"
            return result

        except Exception as e:
            # 失败 → 计数 + 记录时间
            self.failure_count += 1
            self.last_failure_time = time.time()

            # 失败次数达标 → 熔断
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise e

# ======================
# 测试代码
# ======================
breaker = CircuitBreaker("db")

def bad_db():
    raise Exception("数据库挂了")

def good_db():
    return "ok"

print("=== 连续失败，触发熔断 ===")
for _ in range(5):
    try:
        breaker.call(bad_db)
    except Exception as e:
        print("状态:", breaker.state, "错误:", e)

print("\n=== 等待 6 秒冷却 ===")
time.sleep(6)

print("=== 尝试恢复 ===")
try:
    print(breaker.call(good_db))
    print("状态:", breaker.state)
except Exception as e:
    print(e)