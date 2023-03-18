"""
@Time: 2023/3/1 14:19
@Project: CQUTWriter
@File: generateApp.py
@IDE: PyCharm
@Auther: BryanWang
@Description: 
"""
import json
import logging
import requests

logger = logging.getLogger("log")


class GenerateApp:
    """
    文章生成应用，包括两种：
    1. 标题+关键词
    2. 标题+关键词+摘要
    3. 标题+关键词+摘要+大纲
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
        初始化，包括调用模型，读取数据库内容，
        """

        # 待生成的文章
        self.article = ""
        self.title = ""
        self.keywords = ""
        self.abstract = ""
        self.outline = ""

        # 要加载的数据，如倒排索引，hash索引等

        logger.info("已初始化GenerateApp")

    def title_generate(self, title, keywords):
        """
        根据输入的标题和关键词进行生成
        :return:
        """

        # 由输入的标题和关键词进行摘要的抽取和大纲的匹配，用匹配出的大纲，进行文章的写作
        self.title = title
        self.keywords = keywords
        self.get_abstract(self.title, self.keywords)
        self.get_outline(self.title, self.keywords)

        self.article = self.send_request()

    def abstract_generate(self, title, keywords, abstract):
        """
        标题+关键词+摘要生成
        :return:
        """

        self.title = title
        self.keywords = keywords
        self.abstract = abstract
        self.get_outline(self.title, self.keywords)

        self.article = self.send_request()

    def outline_generate(self, title, keywords, abstract, outline):
        """
        标题+关键词+摘要（可能为空）+大纲
        :return:
        """

        self.title = title
        self.keywords = keywords
        self.abstract = abstract
        self.outline = outline

        if self.abstract == "":
            self.get_abstract(self.title, self.keywords)

        self.article = self.send_request()

    def get_abstract(self, title, keywords):
        """
        当用户选择检索摘要时，需要进行摘要的检索
        :return: 检索得到的摘要
        """

        # 读取前端传入的标题和关键词
        self.title = title
        self.keywords = keywords

        # 检索摘要
        try:
            url = "http://10.22.57.6:8080/extract_byKey?inputContent=" + self.keywords + "&topK=1"
            res = requests.get(url)
        except Exception as e:
            logger.error(e)
            res = '{"outputContent": [""]}'

        text = json.loads(res.text)
        self.abstract = text["outputContent"][0]

    def get_outline(self, title, keywords):
        """
        当用户选择检索大纲时
        :return: 检索得到的大纲
        """

        # 读取前端传入的标题和关键词
        self.title = title
        self.keywords = keywords

        # 检索大纲
        try:
            url = "http://10.22.57.6:8080/extract_byTopic?inputContent=" + self.title + "&topK=3"
            res = requests.get(url)
        except Exception as e:
            logger.error(e)
            res = '{"outputContent": [""]}'

        text = json.loads(res.text)
        self.outline = [each+"\n" for each in text["outputContent"]]

    def send_request(self):
        """
        根据已有的信息，去调用远程的生成服务
        :return:
        """

        article = [self.abstract+"\n"]
        for each in self.outline:
            try:
                url = "http://10.22.57.6:8080/generate_byTopic?inputContent1=" + each + "&inputContent2=" + self.keywords + "&type=0&k=1"
                res = requests.get(url)
            except Exception as e:
                logger.error(e)
                res = '{"outputContent": [""]}'

            article.append(json.loads(res.text)["outputContent"][0]+"\n")

        return article
