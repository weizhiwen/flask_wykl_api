import json
from operator import itemgetter

from db import select,select_one
from jieba import posseg, analyse


# 读出所要的数据并形成矩阵
def get_data(current_page):
    start = ((current_page-1)*24)+1
    end = start + 24
    sql = 'SELECT id, img, title, eva_num FROM goods WHERE id NOT IN ' \
          '(SELECT id FROM goods WHERE id >= %d AND id < %d)' %(start, end)
    result = select(sql)
    return result

# 根据商品的相似度推荐
def recommend3(current_page, goods_num):
    sql = 'SELECT words FROM word WHERE id = %d' %current_page
    result_words = select_one(sql)[0]

    result = get_data(current_page)
    other_goods_info = {} # 详细信息的其他商品矩阵
    other_goods = {} # 便于分析的其他商品矩阵
    for row in result:
        if row[0] not in result:
            other_goods_info.setdefault(row[0],[])
            other_goods.setdefault(row[0],[])
        other_goods_info[row[0]] = {'id':row[0],'img': row[1],'title': row[2],'eva_num': row[3]}
        other_goods[row[0]].append(row[2])
    stop_words = []
    # 获取停用词
    with open('stop_words.txt', 'r', encoding='utf-8') as obj:
        stop_words = obj.readlines()

    other_goods_words = {}
    for i, (id, oword) in enumerate(other_goods.items()):
        # print(id, ':', oword[0])
        keys = []
        owords = posseg.cut(oword[0])
        for owds in owords:
            if owds.flag.startswith('n') and owds.word not in stop_words:
                keys.append(owds.word)
        if id not in other_goods_words:
            other_goods_words.setdefault(id, [])
        other_goods_words[id] = analyse.extract_tags(str(keys), topK=4)
    # print('other_goods_words', other_goods_words)
    result_words = json.loads(result_words.replace('\'', '\"'))
    # print('result_words', result_words)
    recommend_sort = {}
    for id, word in other_goods_words.items():
        if id not in recommend_sort:
            recommend_sort.setdefault(id, 0)
        # print('test')
        # print(set(word))
        # print(set(result_words))
        recommend_sort[id] = len(set(word) & set(result_words)) / len(result_words)
    recommend_sort = sorted(recommend_sort.items(), key=itemgetter(1), reverse=True)[:goods_num]
    count_sort = [] # 要推荐的商品编号集合
    for row in recommend_sort:
        if row[0] not in count_sort:
            count_sort.append(row[0])
    print('推荐序号', count_sort)
    recommend_goods = []  # 要推荐的详细商品
    # print('推荐详细商品')
    for id in count_sort:
        for key, value in other_goods_info.items():
            if id == key and key not in recommend_goods:
                recommend_goods.append(value)
    return recommend_goods

if __name__ == '__main__':
    recommend3(2,5)