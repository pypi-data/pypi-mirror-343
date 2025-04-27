#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
⠀⠀⠀⠀⠰⢷⢿⠄
⠀⠀⠀⠀⠀⣼⣷⣄
⠀⠀⣤⣿⣇⣿⣿⣧⣿⡄
⢴⠾⠋⠀⠀⠻⣿⣷⣿⣿⡀
○ ⠀⢀⣿⣿⡿⢿⠈⣿
⠀⠀⠀⢠⣿⡿⠁⠀⡊⠀⠙
⠀⠀⠀⢿⣿⠀⠀⠹⣿
⠀⠀⠀⠀⠹⣷⡀⠀⣿⡄
⠀⠀⠀⠀⣀⣼⣿⠀⢈⣧.
"""



from openai import OpenAI as _OpenAI
from .recall_base import Recall



class RecallOfficial(Recall):

    __doc__ = """
    
    使用官方（OpenAI）api的召回类
    需要拥有发行商的base_url和api_key
    
    """

    def __init__(self, token, base_url="https://api.openai.com/v1", **kwargs):
        self.client = _OpenAI(api_key=token, base_url=base_url, **kwargs)

    def recall(self, system_prompt: str, recall_data: str, question: str, model: str, **kwargs):
        """
        通过系统提示词和问题及模型，召回对应的数据
        :param system_prompt:  系统提示词 为空则使用默认的
        :param recall_data:    召回数据 （转为md格式的字符串）
        :param question:       问题
        :param model:          要提问的模型
        :param kwargs:  同 chat.completions.create的其他参数
        :return:
        """
        messages = [{"role": "system", "content": system_prompt + recall_data}, {"role": "user", "content": question}]
        response = self.client.chat.completions.create(model=model, messages=messages, **kwargs)
        result = response.choices[0].message.content
        return result


