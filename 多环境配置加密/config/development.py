from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"

"""
from .base import BaseConfig从刚才那个父配置里继承过来，所有公共配置直接用。
class DevelopmentConfig(BaseConfig)这是开发环境专用配置。
DEBUG = True开发时打开调试模式，报错直接显示在网页上，方便改 bug。
ENV = "development"给环境起个名字，后面切换环境时靠它识别。
"""