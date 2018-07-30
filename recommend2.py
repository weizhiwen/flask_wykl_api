import math
from operator import itemgetter

from db import select

# 读出所要的数据并形成矩阵
def get_data():
    sql = 'SELECT u_g.userId, u_g.goodId, g.good_img, g.title, g.eva_num FROM user_good u_g,	goods g WHERE	u_g.goodId = g.good_id'
    result = select(sql)
    # print('查询结果为')
    # for row in result:
    #     print(row)
    # data = {} # 数据矩阵
    # for row in result:
    #     if row[0] not in data:
    #         data[row[0]] = []
    #     data[row[0]].append({'good_id':row[1],'good_img': row[2],'title': row[3],'eva_num': row[4]})
    # print('查询结果为')
    # for key,value in data.items():
    #     print(key,":",value)
    return result

# 根据用户购买商品的余弦相似度推荐算法
def recommend2(user_id, user_num, recommend_num):
    result = get_data()
    # print('查询结果为')
    # for row in result:
    #     print(row)
    user_goods_info = {}  # 带有详细信息的数据矩阵
    user_goods_matrix = {} # 只有用户编号和商品编号的数据矩阵，便于算法使用
    for row in result:
        if row[0] not in user_goods_matrix:
            user_goods_info.setdefault(row[0],[])
            user_goods_matrix.setdefault(row[0], [])
        user_goods_info[row[0]].append({'good_id':row[1],'good_img': row[2],'title': row[3],'eva_num': row[4]})
        user_goods_matrix[row[0]].append(row[1])
    # print('带有详细信息的数据矩阵')
    # for key, varlue in user_goods_info.items():
    #     print(key, ':', varlue)
    # print('只有用户编号和商品编号的数据矩阵')
    # for key, varlue in user_goods_matrix.items():
    #     print(key, ':', varlue)

    good_user_matrix = {} # 商品用户举证
    # 将用户商品矩阵 user_goods_matrix 转换为商品用户矩阵 good_user_matrix
    for user, goods in user_goods_matrix.items():
        for good in goods:
            if good not in good_user_matrix:
                good_user_matrix.setdefault(good, set())
            good_user_matrix[good].add(user)
    # print('商品用户矩阵')
    # for key, value in good_user_matrix.items():
    #     print(key, ':', value)

    user_inner_matrix = {} # 用户之间相同商品数量矩阵
    # 统计用户之间购买过相同商品的数量
    for users in good_user_matrix.values():
        for user1 in users:
            for user2 in users:
                if user1 == user2:
                    continue
                if user1 not in user_inner_matrix:
                    user_inner_matrix.setdefault(user1, {})
                if user2 not in user_inner_matrix[user1]:
                    user_inner_matrix[user1][user2] = 0
                user_inner_matrix[user1][user2] += 1
    # print('用户之间购买过相同商品矩阵')
    # for key, value in user_inner_matrix.items():
    #     print(key, ':', value)

    user_similar_matrix = {} # 用户之间相似度矩阵
    # 计算用户之间的相似度
    for user1, inner in user_inner_matrix.items():
        for user2, num in inner.items():
            if user1 not in user_similar_matrix:
                user_similar_matrix.setdefault(user1, {})
            if user2 not in user_similar_matrix[user1]:
                user_similar_matrix[user1][user2] = 0
            user_similar_matrix[user1][user2] = num / math.sqrt(len(user_goods_matrix[user1]) * len(user_goods_matrix[user2]))
    # print('用户之间相似度矩阵')
    # for key, value in user_similar_matrix.items():
    #     print(key, ':', value)

    user_goods = user_goods_matrix[user_id] # 目标用户的商品集合
    user_similar_matrix = sorted(user_similar_matrix[user_id].items(), key=itemgetter(1), reverse=True)[:user_num] # 和目标用户的相似用户相似度排序
    # print('目标用户的商品集合', user_goods)
    good_ids = {} # 要推荐的商品的序号及相似度
    for user, similar in user_similar_matrix:
        # print(user, ':', similar)
        for goods in user_goods_matrix[user]:
            if goods in user_goods:
                continue
            if goods not in good_ids:
                good_ids.setdefault(goods, 0)
            good_ids[goods] += similar
    # print('排序前的商品的序号及相似度', good_ids)
    good_ids = sorted(good_ids.items(), key=itemgetter(1), reverse=True)[:recommend_num]
    # print('排序后的商品的序号及相似度', good_ids)
    count_sort = [] # 要推荐的商品的序号
    for id in good_ids:
        count_sort.append(id[0])
    print('推荐的商品的序号', count_sort)

    goods_data = []  # 商品信息数组
    for user in user_goods_info.keys():
        # print(user)
        for good in user_goods_info[user]:
            # print(good)
            if good not in goods_data:
                goods_data.append(good)
    # for good in goods_data:
    #     print(good)
    recommend_goods = [] # 要推荐的详细商品
    # print('推荐详细商品')
    for id in count_sort:
        for good in goods_data:
            # print('item', good)
            if id == good['good_id'] and good not in recommend_goods:
                recommend_goods.append(good)

    # print('推荐商品')
    # for good in recommend_goods:
    #     print(good)
    return recommend_goods

if __name__ == '__main__':
    # get_data()
    print(recommend2(2, 2, 4))