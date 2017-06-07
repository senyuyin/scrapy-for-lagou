# scrapy-for-lagou
拉勾网 职位抓取

# 功能:
1.适用于Python3，抓取拉勾网json数据，可根据所在城市及工种做出调整

2.将数据保存在本机MongoDB内

# 注意事项：
由于拉勾网可能封ip，可将DOWNLOAD_DELAY设置的长一点

或者在Middlewares中启动ProxyMiddleware

本文采用的是崔庆才的proxyfilter接口，Github地址为https://github.com/Germey/ProxyFilter

clone好后，在命令行内输入：python3 run.py

再进行scrapy抓取

# 后续更新

加入 scrapy-redis分布式爬取拉勾网
