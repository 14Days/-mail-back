from flask import jsonify


def success_warp(data):
    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': data
    })


def fail_warp(code, msg):
    return jsonify({
        'code': code,
        'msg': msg,
        'data': None
    })
