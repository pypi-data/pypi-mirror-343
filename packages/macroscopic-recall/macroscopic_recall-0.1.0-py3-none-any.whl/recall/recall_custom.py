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

from .recall_base import Recall


class RecallCustom(Recall):

    __doc__ = """

    使用用户自己定制的召回类

    """

    def __init__(self, recall_function):
        self.recall_function = recall_function

    def recall(self, *args, **kwargs):
        """
        使用用户自定义的召回方法，返回方法的返回值
        """
        result = self.recall_function(*args, **kwargs)
        return result



