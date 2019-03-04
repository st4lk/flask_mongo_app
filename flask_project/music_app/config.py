import os

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 27017)
DB_NAME = os.environ.get('DB_NAME', 'flask_project')


class BaseConfig:
    MONGO_URI = f'mongodb://{DB_HOST}:{DB_PORT}/{DB_NAME}'


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    MONGO_URI = f'mongodb://{DB_HOST}:{DB_PORT}/test_{DB_NAME}'


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
}
