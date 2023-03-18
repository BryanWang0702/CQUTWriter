"""
@Time: 2023/3/2 10:28
@Project: CQUTWriter
@File: homeApp.py
@IDE: PyCharm
@Auther: BryanWang
@Description: 
"""
import json
import logging
import requests

logger = logging.getLogger("log")


class HomeApp:
    """
    主页的一些相关应用
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
        初始化一些数据
        """

        logger.info("已初始化HomeApp")

    def get_text(self, title, sentence):
        """
        根据一个标题和开头句，请求远端服务器的生成服务，得到一段生成的文本
        :param title:
        :param sentence:
        :return:
        """

        try:
            url = "http://10.22.57.6:8080/generate_bySentence?inputContent1=" + title + "&inputContent2=" + sentence + "&k=1"
            res = requests.get(url)
        except Exception as e:
            logger.error(e)
            res = '{"outputContent": [""]}'

        text = json.loads(res.text)
        return text["outputContent"][0]
