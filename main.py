import logging
from app.app import create_app
from common import set_log
app = create_app()

if __name__ == '__main__':
    logging.info("我是info的日志")
    logging.debug("我是debug的日志")

    app.run()
