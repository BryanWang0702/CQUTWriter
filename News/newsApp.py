import json
import logging
import threading
import time

import requests
from bs4 import BeautifulSoup


class NewsApp:
    """
        使用爬虫爬取各新闻网站的热榜
    """

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        :param args:
        :param kwargs:
        """

        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        """
        初始化
        """

        self.logger = logging.getLogger('log')
        # 各平台的热榜数据，存放在redis中
        self.people = []  # 人民网
        self.weibo = []  # 微博
        self.zhihu = []  # 知乎
        self.baidu = []  # 百度
        self.toutiao = []  # 头条

        # 将所有的新闻全部存成一个字典
        self.news = {
            "people": [],
            "toutiao": [],
            "weibo": [],
            "baidu": [],
            "zhihu": []
        }

        # 创建线程在后台运行
        self.thread = threading.Thread(target=self.update_news, name="time_crawler")
        self.thread.start()

    def update_news(self):
        """
        更新热点新闻，即将所有的平台爬虫重新爬取一次
        :return:
        """

        while True:
            try:
                self.weibo_crawler()
                self.zhihu_crawler()
                self.people_crawler()
                self.toutiao_crawler()
                self.baidu_crawler()

                self.news["people"] = self.people
                self.news["toutiao"] = self.toutiao
                self.news["weibo"] = self.weibo
                self.news["zhihu"] = self.zhihu
                self.news["baidu"] = self.baidu

                self.logger.info("更新一次爬虫")
            except Exception as e:
                self.logger.error(e.args)
                self.thread.start()
            # 每小时更新一次
            time.sleep(60 * 60)

    def people_crawler(self):
        """
        人民网新闻爬虫，url为 http://www.people.com.cn/GB/59476/index.html
        在处理数据的时候需要转码
        :return:
        """

        url = "http://www.people.com.cn/GB/59476/index.html"

        try:
            res = requests.get(url)

            # 人民网的新闻是GB2312编码的
            soup = BeautifulSoup(res.text.encode("latin1").decode("GB2312"))

            news_tags = []

            # 顶部的头条新闻
            head_td = soup.find("td", class_="indexfont13")
            news_tags += ([each for each in head_td.find_all("a")])

            # 中间的要点新闻
            td_ = soup.find("td", class_="p6")
            news_tags += ([each for each in td_.find_all("a")])

            self.people = []
            # 将信息从a标签中提取出来
            for i in range(len(news_tags)):
                news = news_tags[i]
                self.people.append((news.text, news["href"]))

            # 有时候会爬取到空的新闻，将空的去除掉
            self.people = [news for news in self.people if news[0]]
            self.people = self.people[:20]

        except Exception as e:
            self.logger.error(e)

    def toutiao_crawler(self):
        """
        头条的热榜爬取，url https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc
        置顶的那条新闻信息不全，不进行爬取
        :return:
        """

        try:
            url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
            res = requests.get(url)
            json_ = json.loads(res.text)

            # 热点新闻
            news_tags = json_['data']

            self.toutiao = []

            for i in range(len(news_tags)):
                news = news_tags[i]
                self.toutiao.append((news['Title'], "https://www.toutiao.com/trending/" + news['ClusterIdStr']))

            # 有时候会爬取到空的新闻，将空的去除掉
            self.toutiao = [news for news in self.toutiao if news]
            self.toutiao = self.toutiao[:20]

        except Exception as e:
            self.logger.error(e)

    def weibo_crawler(self):
        """
        微博爬虫，爬取微博热搜榜，url为 https://weibo.com/ajax/statuses/hot_band
        目前看来没有什么反爬策略，将Json数据解析成字典后提取信息即可
        """

        # 爬取hot_band的信息并解析成dict
        url = 'https://weibo.com/ajax/statuses/hot_band'

        # 如果爬取失败则保持列表中的数据
        try:
            res = requests.get(url=url)
            hot_band = json.loads(res.text)['data']['band_list'][:50]

            # 读取其中有用的信息，主要包括热搜的内容和热度以及类别
            self.weibo = []
            for i in range(len(hot_band)):
                news = hot_band[i]
                try:
                    self.weibo.append((news['word'], 'https://s.weibo.com/weibo?q=' + news['word']))
                except KeyError as e:
                    self.logger.error(e.args)
                    continue

            # 有时候会爬取到空的新闻，将空的去除掉
            self.weibo = [news for news in self.weibo if news]
            self.weibo = self.weibo[:20]

        except Exception as e:
            self.logger.error(e.args)
            return

    def baidu_crawler(self):
        """
        爬取百度热搜，url https://top.baidu.com/board?tab=realtime
        包括标题、链接、热度
        :return:
        """

        try:
            url = "https://top.baidu.com/board?tab=realtime"
            res = requests.get(url)
            soup = BeautifulSoup(res.text)

            news_tags = soup.find_all("div", class_="category-wrap_iQLoo")[1:]

            self.baidu = []
            for i in range(len(news_tags)):
                news = news_tags[i]
                title = news.find("div", class_="c-single-text-ellipsis").text.strip()
                href = "https://www.baidu.com/s?wd=" + title

                self.baidu.append((title, href))

            # 有时候会爬取到空的新闻，将空的去除掉
            self.baidu = [news for news in self.baidu if news]
            self.baidu = self.baidu[:20]
        except Exception as e:
            self.logger.error(e)

    def zhihu_crawler(self):
        """
        爬取知乎的热榜，url为 https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50
        其中limit可以改，在此只爬取前50条后再截取前20条
        目前似乎没有反爬策略
        :return:
        """

        try:
            res = requests.get(url='https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50')
            hot_news = json.loads(res.text)['data']

            self.zhihu = []
            for i in range(len(hot_news)):
                news = hot_news[i]
                news = news['target']
                title = news['title']

                # 知乎对链接进行了处理
                # 爬取得到：https://api.zhihu.com/questions/581790596 返回json数据
                # 实际访问格式 https://zhihu.com/question/581790596
                # 进行修改
                url = news['url']
                url = url.replace('api.', '')
                url = url.replace('questions', 'question')

                self.zhihu.append((title, url))

            # 有时候会爬取到空的新闻，将空的去除掉
            self.zhihu = [news for news in self.zhihu if news]
            self.zhihu = self.zhihu[:20]

        except Exception as e:
            self.logger.error(e.args)
