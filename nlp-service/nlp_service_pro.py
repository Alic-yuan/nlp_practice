# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author  jakey
# Date 2018-02-28 15:47

"""
nlpServiceApi启动文件
"""

import argparse
from bottle import run
from sclog.logger import get_logger


# yuan.zhang
from controllers.ner_pro import ner_pro_handler

PARSER = argparse.ArgumentParser()
LOGGER = get_logger()

if __name__ == "__main__":
    PARSER.add_argument("-port", "--port", type=int, default=5000, help="请输入端口, 默认为5000")
    ARGS = PARSER.parse_args()
    LOGGER.info("服务已经启动...")
    run(host='0.0.0.0', port=ARGS.port, workers=1, server="tornado")
