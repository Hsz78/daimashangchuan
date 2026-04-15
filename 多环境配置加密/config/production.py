from .base import BaseConfig

class ProductionConfig(BaseConfig):
    
    DEBUG = False
    ENV = "production"

"""
生产环境，严禁开 DEBUG
环境名：production
"""