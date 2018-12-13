"""
错误类型处理
"""
import json
from bottle import HTTPResponse
from sclog.logger import get_logger
from common import error_code

LOGGER = get_logger()


class CustomBottle(object):
    """
    Bottle框架自定义函数
    """
    @staticmethod
    def __format_response(data, code=200, msg=None):
        """
        统一格式化包装
        """
        if not msg:
            msg = CustomBottle.__error_msg(code)
        return {
            "message": msg,
            "code": code,
            "data": data
        }

    @staticmethod
    def __error_msg(code):
        """
        统一状态码处理
        """
        if code == 200:
            return "SUCCESS"
        return error_code.ERROR_TEXT.get(code, "FAILED")

    @staticmethod
    def custom_response(code=200, data=None, message=None):
        """
        统一返回值包装
        """
        if not isinstance(code, int):
            raise Exception("code必须为数字类型")
        return HTTPResponse(status=int(str(code)[0:3]), headers={"Content-Type": "application/json"},
                            body=CustomBottle.__format_response(data=data, code=code, msg=message))

    @staticmethod
    def post_validate(request):
        """
        post统一获取
        """
        try:
            body = json.loads(request.body.read())
        except Exception as error:
            LOGGER.error(error)
            return None
        return body
