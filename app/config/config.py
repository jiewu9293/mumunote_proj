# 全局通用配置
class Config(object):
    db_url = "mysql+pymysql://admin1:123@192.168.1.129:3306/mumushouji"
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