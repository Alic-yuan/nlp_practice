# -*- coding:utf-8 -*-
'''
@Author: yuan
@Date: 2018-07-27 17:27:45
'''

import sys

from bottle import request, route

from bussiness.ner_pro_entry import extract_api

from common import error_code
from common.error_handler import CustomBottle
from sclog.logger import get_logger

LOGGER = get_logger()

@route("/api/nlp/pro", method="POST")
def ner_pro_handler():
    """
    机构名简称抽取接口
    """
    body = CustomBottle.post_validate(request)
    if not body:
        return CustomBottle.custom_response(code=error_code.ERROR_PARAMETER)

    try:
        content = body.get("content", None)
        assert content, ValueError("参数为空")
    except Exception as error:
        LOGGER.error(error)
        return CustomBottle.custom_response(code=error_code.ERROR_PARAMETER, message=str(error))
    try:
        res = extract_api(content)
        if not res:
            return CustomBottle.custom_response(code=error_code.ERROR_RESOLVE)
        return CustomBottle.custom_response(data=res)
    except Exception as error:
        import traceback
        traceback.print_exc()
        LOGGER.error(error)
        return CustomBottle.custom_response(code=error_code.ERROR_INNER_SERVICE, message=str(error))
