from .base import BaseConfig

class TestingConfig(BaseConfig):
    DEBUG = False
    ENV = "testing"

"""
测试环境
"""