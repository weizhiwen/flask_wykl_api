# 网易考拉爬虫项目 API 文档
## 商品相关接口
| 序号 |                           接口路由                           |                 接口功能                  |
| :--: | :----------------------------------------------------------: | :---------------------------------------: |
|  1   |            [/api/goods/\<int:page\>/\<int:offset\>](./分页查询商品.md)           |           分页查询商品部分信息            |
|  2   |                    [/api/goods/\<int:id\>](./查询商品详情.md)                |             查询商品详情信息              |
|  3   |                    [/api/search/\<string:keyword\>/\<int:goods_num\>](./搜索商品.md)                |             根据关键字搜索商品              |
|  4   |     [/api/goods/recommend1/\<int:good_id\>/\<int:count\>](./购买过此商品的用户还购买过推荐.md)      | 商品推荐算法1，购买过此商品的用户还购买过 |
|  5   | [/api/goods/recommend2/\<int:user_id\>/\<int:user_num\>/\<int:recommend_num\>](./用户购买过的商品余弦相似度推荐.md) |  商品推荐算法2，用户购买过商品的余弦相似度推荐商品   |
|  6   | [/api/goods/recommend3/\<int:current_page\>/\<int:recommend_num\>](./商品的相似度推荐.md) | 商品推荐算法3，一页商品的相似度推荐商品 |