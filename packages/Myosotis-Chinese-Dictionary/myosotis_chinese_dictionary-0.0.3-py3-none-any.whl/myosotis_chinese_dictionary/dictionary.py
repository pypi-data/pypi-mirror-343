from importlib import resources
import json
import os

dictionary_path = os.path.join(os.path.dirname(__file__), "dictionary.json")

dictionary = {}
with resources.files("myosotis_chinese_dictionary").joinpath("dictionary.json").open("r", encoding="utf-8") as f:
    dictionary = json.load(f)

def pinyin_list(cc):
    if len(cc) > 1:
        raise ValueError("The input string should contain exactly 1 character.")
    if cc in dictionary.keys():
        return dictionary[cc]
    return None

__all__ = ["pinyin_list"]