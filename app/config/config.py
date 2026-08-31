# 全局通用配置
class Config(object):
    db_url = "mysql+pymysql://root:20040620Deng@127.0.0.1:3306/mumushouji?charset=utf8mb4"
    page_count = 10
    article_header_image_path = "/images/article/header/"
    user_header_image_path = "/images/headers/"
# 测试环境
class TestConfig(Config):
    # db_url = ""
    if_echo=True
    LOG_LEVEL="DEBUG"

class ProductionConfig(Config):
    if_echo=False
    LOG_LEVEL = "INFO"

config = {
    "test":TestConfig,
    "prop":ProductionConfig
}