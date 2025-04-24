import json
import os

dictionary_path = os.path.join(os.path.dirname(__file__), "dictionary.json")

dictionary = {}
with open(dictionary_path, "r") as f:
    dictionary = json.loads(f.read())

def pinyin_list(cc):
    if len(cc) > 1:
        raise ValueError("The input string should contain exactly 1 character.")
    if cc in dictionary.keys():
        return dictionary[cc]
    return None

__all__ = ["pinyin_list"]