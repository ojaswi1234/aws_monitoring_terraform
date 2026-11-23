import os

class BaseConfig:
    APP_NAME = "DevOps Self-Healing System"
    VERSION = "1.0.0"
    SERVICE_NAME = "python-backend"
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"

class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    ENV = "testing"

class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

def get_config():
    env = os.environ.get("FLASK_ENV", "production").lower()
    return CONFIG_MAP.get(env, ProductionConfig)
