from flask import jsonify


class Warp:
    @classmethod
    def success_warp(cls, data):
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': data
        })

    @classmethod
    def fail_warp(cls, code, msg):
        return jsonify({
            'code': code,
            'msg': msg,
            'data': None
        })
