from flask import jsonify

# 状态码列表
STATUS_CODE_200 = {'code': 200, 'message': 'OK all right.'}
STATUS_CODE_201 = {'code': 201, 'message': 'All created.'}
STATUS_CODE_204 = {'code': 204, 'message': 'All deleted.'}
STATUS_CODE_400 = {'code': 400, 'message': 'Bad request.'}
STATUS_CODE_403 = {'code': 403, 'message': 'You can not do this.'}
STATUS_CODE_404 = {'code': 404, 'message': 'No result matched.'}

# 带数据的响应
def data_response(status_code, data):
    return jsonify({'status': status_code, 'data': data})

# 带分页数据的响应
def data_with_page_response(status_code, data, current_page, total_pages, total_items):
    return jsonify({'status': status_code, 'data': data, 'current_page':current_page, 'total_pages': total_pages, 'total_items':total_items})

# 只有状态码的响应
def status_response(status_code):
    return jsonify({'status': status_code})