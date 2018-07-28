from math import ceil

from flask import Flask
from db import get_db, select, select_one
from status_code import *
app = Flask(__name__)


@app.route('/')
def index():
    return status_response(STATUS_CODE_200)


# 获取所有商品列表 API，/goods
# return total_pages, current_page
# @app.route('/goods')
# def goods_list():
#     sql = "SELECT good_id, good_img, now_price, pefer_price, title, eva_num, goods_prma FROM goods"
#     result = select(sql)
#     data = []
#     for row in result:
#         data.append({'good_id': row[0], 'good_img': row[1], 'now_price': row[2], 'pefer_price': row[3], 'title': row[4], 'eva_num': row[5], 'goods_prma': row[6]})
#     return data_response(STATUS_CODE_200, data)

# 按页获取商品列表 API，/goods/<int:page>/<int:offset>
# 说明：前台发送 GET 请求，传入需要显示页面的页数 page，页数从 1 开始，以及每页想显示的条数 offset
# return data, total_pages, current_page, total_items
@app.route('/goods/<int:page>/<int:offset>')
def goods_list_page(page, offset):
    sql = "SELECT COUNT(good_id) FROM goods"
    result = select_one(sql)
    total_items = result[0] # 总条数
    total_page = int(ceil(total_items / offset)) # 总页数
    start = (page - 1) * offset
    sql = "SELECT good_id, good_img, now_price, pefer_price, title, eva_num, goods_prma FROM goods LIMIT %d, %d" %(start, offset)
    result = select(sql)
    data = []
    for row in result:
        data.append({'good_id': row[0], 'good_img': row[1], 'now_price': row[2], 'pefer_price': row[3], 'title': row[4], 'eva_num': row[5], 'goods_prma': row[6]})
    return data_with_page_response(STATUS_CODE_200, data, current_page=page, total_pages=total_page, total_items=total_items)


# 获取某个单独的 API，/goods/<int:id>
@app.route('/goods/<int:id>')
def get_good_by_id(id):
    sql = "SELECT good_id, good_img, brand, now_price, pefer_price, title, taxation, explains, service, eva_score, eva_num, sun_num, goods_prma FROM goods WHERE good_id = %d" %id
    row = select_one(sql)
    data = []
    data.append({'good_id': row[0], 'good_img': row[1], 'brand': row[2], 'now_price': row[3], 'pefer_price': row[4], 'title': row[5], 'taxation': row[6], 'explains': row[7], 'service': row[8], 'eva_score': row[9], 'eva_num': row[10], 'sun_num': row[11], 'goods_prma': row[12]})
    return data_response(STATUS_CODE_200, data)

if __name__ == '__main__':
    app.run()
