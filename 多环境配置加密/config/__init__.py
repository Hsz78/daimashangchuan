from .base import BaseConfig
from .development import DevelopmentConfig
from .testing import TestingConfig
from .production import ProductionConfig

# 环境名字 → 对应配置类
config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}