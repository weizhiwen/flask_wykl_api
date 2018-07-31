import random
from db import get_db
userIds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
db = get_db()
for userId in userIds:
    goodsIds = set()
    for i in range(100):
        goodsIds.add(random.randint(1,100))
    for goodId in goodsIds:
        sql = 'INSERT INTO user_goods(userId, goodsId) VALUES(%d, %d)'%(userId,goodId)
        cursor = db.cursor()
        cursor.execute(sql)
    db.commit()