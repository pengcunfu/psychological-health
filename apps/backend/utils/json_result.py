from flask import jsonify


class JsonResult:
    @staticmethod
    def success(data=None, message='success', code=200):
        response = {
            'code': code,
            'message': message,
            'success': True
        }
        if data is not None:
            response['data'] = data
        return jsonify(response)

    @staticmethod
    def error(message='fail', code=500, data=None):
        response = {
            'code': code,
            'message': message,
            'success': False
        }
        if data is not None:
            response['data'] = data
        return jsonify(response)
