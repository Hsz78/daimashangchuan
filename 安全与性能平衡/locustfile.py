# Locust 压测脚本（修正版，只压你真实存在的接口）
from locust import HttpUser, task, between

class NormalUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"  # 你的服务地址

    # 启动时只访问健康接口
    def on_start(self):
        self.client.get("/debug/db-pool")

    @task(3)  # 主要压这个接口（你真实存在的）
    def view_pool(self):
        self.client.get("/debug/db-pool")