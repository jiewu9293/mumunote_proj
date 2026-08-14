import logging
from logging.handlers import RotatingFileHandler

from app.config.config import config
from settings import env


def set_log():
    config_class = config[env]

    # 设置日志的等级
    logging.basicConfig(level=config_class.LOG_LEVEL)
    # 创建日志记录器 ,指定日志的保存路径、每个日志文件的最大大小、保存的日志个数
    file_log_handler = RotatingFileHandler("log/mumunote.log",maxBytes=1024*1024*300,backupCount=10)
    # 创建日志记录的格式
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d %(message)s")
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

set_log()