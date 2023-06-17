from rest_framework import status

## HTTP Code [200,201,400,403,409]
SUCCESS = "요청된 작업을 완료했습니다."
MISSING_PARAMS = "요청 데이터에 누락된 데이터가 있습니다."
SERVER_ERROR = "요청을 처리할 수 없습니다."
INVAILD_ERROR = "유효하지 않는 데이터입니다."
FORBIDEEN_ERROR = "유효하지 않는 접근입니다."
NOTFOUND_ERROR = "해당 요청을 찾을 수 없습니다."

__all__ = (
    "custom_response",
    "ErrorCollection",
)


class ErrorCollection(object):
    # def __init__(self, message, data):
    #     self.message = message
    #     self.data = data

    def as_md(self, res_dict):
        return "```\n%s\n```" % (res_dict,)


def custom_response(res_code, message: str = None, data=None) -> dict:
    # res_code = HTTP Code
    # message = "Response Message"
    # data = "Response Data"

    if message is not None:
        if res_code == 200 or res_code == 201:
            message = message

        elif res_code == 400:
            message = message

        elif res_code == 403:
            message = FORBIDEEN_ERROR

        elif res_code == 404:
            message = NOTFOUND_ERROR

    else:
        if res_code == 200 or res_code == 201:
            message = SUCCESS

        elif res_code == 400:
            message = MISSING_PARAMS

    result = {
        "message": message,
        "data": data,
    }

    return result
