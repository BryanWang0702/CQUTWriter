"""
@Time: 2023/3/1 15:26
@Project: CQUTWriter
@File: summarizeApp.py
@IDE: PyCharm
@Auther: BryanWang
@Description: 
"""

from django.http import JsonResponse
from django.shortcuts import render
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import logging

logger = logging.getLogger("log")


class SummarizeApp:
    """
    摘要类，包括摘要页面的一系列操作，如跳转到摘要页，摘要和关键词的生成
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
        摘要类的初始化方法，主要是用于加载所需要的库，后续调用方法时不用再加载
        """

        # 初始化TextRank4Keyword
        self.tr4w = TextRank4Keyword()

        # 初始化TextRank4Sentence
        self.tr4s = TextRank4Sentence()

        logger.info("已初始化SummarizeApp")

    def abstract_keywords_generation(self, inputContent):
        """
        根据前端传入的文本数据，抽取出摘要和关键词并返回
        :param inputContent:
        :return: Json数据，包括摘要和关键词
        """

        # 抽取摘要和关键词
        abstract = self.sentences_extraction(inputContent)
        keywords = self.keywords_extraction(inputContent)

        return abstract, keywords

    def sentences_extraction(self, text):
        """
        根据文本抽取出摘要
        :param text: 待摘要文本
        :return: 摘要，各摘要之间用 "\n"隔开
        """

        # 利用tr4s进行摘要抽取
        self.tr4s.analyze(text=text, lower=True)

        # 将关键句提取出来
        sentences = "\n".join(
            each for each in [item.sentence for item in self.tr4s.get_key_sentences(num=3, sentence_min_len=5)])

        return sentences

    def keywords_extraction(self, text):
        """
        根据文本抽取出关键词
        :param text:
        :return: 关键词，用 "，" 隔开
        """

        # 利用tr4w抽取关键词
        self.tr4w.analyze(text=text, lower=True, window=5)

        # 将关键词提取出来
        keywords = "，".join(each for each in [item.word for item in self.tr4w.get_keywords(num=10, word_min_len=2)])

        return keywords
