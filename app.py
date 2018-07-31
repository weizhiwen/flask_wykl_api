import os
from math import ceil
from flask import Flask, send_file as _send_file
from db import select, select_one
from status_code import *
from recommend1 import recommend1
from recommend2 import recommend2
from recommend3 import recommend3
app = Flask(__name__)

# beken code
def get_folder(folder):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        folder)

def send_file(filename):
    return _send_file(os.path.join('webroot', filename))

# 返回页面
@app.route('/detail/<int:id>')
def detail(id):
    return send_file('detail.html')

@app.route('/')
def index():
    return send_file('index.html')

# 按页获取商品列表 API，/api/goods/<int:page>/<int:offset>
# 说明：前台发送 GET 请求，传入需要显示页面的页数 page，页数从 1 开始，以及每页想显示的条数 offset
# return data, total_pages, current_page, total_items
@app.route('/api/goods/<int:page>/<int:offset>')
def goods_list_page(page, offset):
    sql = "SELECT COUNT(id) FROM goods"
    result = select_one(sql)
    total_items = result[0] # 总条数
    total_page = int(ceil(total_items / offset)) # 总页数
    data = []
    if page > 0 or page <= total_page:
        start = (page - 1) * offset
        sql = "SELECT id, img, origin_country, brand, tag, title, cell_price, pefer_price, activity, explains, eva_num FROM goods LIMIT %d, %d" %(start, offset)
        result = select(sql)
        for row in result:
            data.append({'id': row[0], 'img': row[1], 'origin_country': row[2], 'brand': row[3], 'tag': row[4], 'title': row[5], 'cell_price':row[6], 'pefer_price':row[7], 'activity':row[8], 'explains':row[9], 'eva_num':row[10]})
    return data_with_page_response(STATUS_CODE_200, data, current_page=page, total_pages=total_page, total_items=total_items)


# 获取某个商品的 API，/api/goods/<int:id>
@app.route('/api/goods/<int:id>')
def get_good_by_id(id):
    sql = "SELECT id, img, origin_country, brand, tag, title, cell_price, pefer_price, activity, service, explains, eva_score, eva_num, sun_num FROM goods WHERE id = %d" %id
    row = select_one(sql)
    data = [{'id': row[0], 'img': row[1], 'origin_country': row[2], 'brand': row[3], 'tag':row[4], 'title': row[5], 'cell_price': row[6], 'pefer_price': row[7], 'activity': row[8], 'service': row[9], 'explains': row[10], 'eva_score': row[11], 'eva_num': row[12], 'sun_num': row[13]}]
    return data_response(STATUS_CODE_200, data)


# 获取购买过此商品的用户还购买过推荐商品的 API，/api/goods/recommend1/<int:good_id>/<int:count>
@app.route('/api/goods/recommend1/<int:good_id>/<int:count>')
def get_recommend1_goods(good_id, count):
    # print('传过来的值为 recommend_id：' + str(recommend_id) + 'good_id：' + str(good_id) + 'count：' + str(count))
    data = recommend1(good_id, count)
    return data_response(STATUS_CODE_200, data)


# 根据用户购买过商品的余弦相似度推荐商品的 API，/api/goods/recommend2/<int:user_id>/<int:user_num>/<int:recommend_num>
@app.route('/api/goods/recommend2/<int:user_id>/<int:user_num>/<int:recommend_num>')
def get_recommend2_goods(user_id, user_num, recommend_num):
    # print('传过来的值为 user_id：' + str(user_id) + 'good_id：' + str(user_num) + 'count：' + str(recommend_num))
    data = recommend2(user_id, user_num, recommend_num)
    return data_response(STATUS_CODE_200, data)


# 根据商品的标题分词推荐关联高的商品的 API
@app.route('/api/goods/recommend3/<int:current_page>/<int:recommend_num>')
def get_recommend3_goods(current_page, recommend_num):
    # print('传过来的值为 current_page：', str(current_page) + ',goods_num:', str(goods_num))
    data = recommend3(current_page, recommend_num)
    return data_response(STATUS_CODE_200, data)


if __name__ == '__main__':
    app.run()
