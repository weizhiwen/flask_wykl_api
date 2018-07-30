from operator import itemgetter
from collections import OrderedDict

from db import select, select_one

# 读出所要的数据并形成矩阵
def get_data(good_id):
    sql = 'SELECT u_g.userId, u_g.goodId, g.good_img, g.title, g.eva_num ' \
            'FROM user_good u_g, goods g WHERE userId in (SELECT userId FROM user_good WHERE goodId = %d) ' \
                'AND u_g.goodId = g.good_id' %good_id
    result = select(sql)
    # print(result)
    data = {} # 数据矩阵
    for row in result:
        if row[0] not in data:
            data[row[0]] = []
        data[row[0]].append({'good_id':row[1],'good_img': row[2],'title': row[3],'eva_num': row[4]})
    # print(data)
    return data

# 购买过此商品的用户还购买过推荐算法
def recommend1(good_id, count):
    data = get_data(good_id)
    goods_count = {} # 商品出现的频次集合
    goods_data = [] # 商品信息数组
    for user in data.keys():
        for good in data[user]:
            if good['good_id'] == good_id:
                continue
            if good['good_id'] not in goods_count:
                goods_count.setdefault(good['good_id'], 0)
            goods_count[good['good_id']] += 1
            if good['good_id'] not in goods_data:
                goods_data.append(good)
    # print('商品出现的频次', goods_count)
    if count < len(goods_count):
        goods_count_sort = sorted(goods_count.items(), key=itemgetter(1), reverse=True)[:count]
    else:
        goods_count_sort = goods_count
    print('商品出现的频次排序', goods_count_sort)
    count_sort = []
    for good_id in goods_count_sort:
        count_sort.append(good_id[0])
    # print('所要推荐的商品的序号', count_sort)
    # print('商品信息数据', goods_data, end='\n')
    # print('要推荐的商品信息')
    recommend_goods = []
    for id in count_sort:
        for good in goods_data:
            if id == good['good_id'] and good not in recommend_goods:
                # print('item', good)
                recommend_goods.append(good)
    return recommend_goods

if __name__ == '__main__':
    # get_data(1)
    for good in recommend1(1, 6):
        print(good)