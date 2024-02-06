#!/usr/bin/env python3
# *_*coding=utf-8
"""
@author : Francis.zz
@date   : 2023-11-15 16:52
@desc   : get_tokens.py
"""

import unicodedata


def is_cjk_character(ch: str) -> bool:
    """
    Check if the character is CJK character.
    """
    code = ord(ch)
    return 0x4E00 <= code <= 0x9FFF


def is_space(ch: str) -> bool:
    """
    Check if the character is space.
    """
    return ch in {" ", "\n", "\r", "\t"} or unicodedata.category(ch) == "Zs"


def is_punctuation(ch: str) -> bool:
    """
    Check if the character is punctuation.
    """
    code = ord(ch)
    return (
            33 <= code <= 47
            or 58 <= code <= 64
            or 91 <= code <= 96
            or 123 <= code <= 126
            or unicodedata.category(ch).startswith("P")
    )


def local_count_tokens(text: str, model: str = "ERNIE-Bot") -> int:
    """
    计算千帆文本tokens数

    :param text:
    :param model:
    :return:
    """
    han_count = 0
    text_only_word = ""
    for ch in text:
        if is_cjk_character(ch):
            han_count += 1
            text_only_word += " "
        elif is_punctuation(ch) or is_space(ch):
            text_only_word += " "
        else:
            text_only_word += ch
    word_count = len(list(filter(lambda x: x != "", text_only_word.split(" "))))
    return han_count + int(word_count * 1.3)


if __name__ == '__main__':
    text = "123,,,,,,"
    print(f'千帆tokens：{local_count_tokens(text)}')
