from importlib import resources
import json
import os

style_names = [
    "normal",
    "tone",
    "tone2",
    "tone3",
    "finals",
    "finals_tone",
    "finals_tone2",
    "finals_tone3",
    "initials",
    "bopomofo",
    "bopomofo_first",
]
k = len(style_names)

dictionaries = {}
for i in range(k):
    style_name = style_names[i]
    dictionary_path = os.path.join(os.path.dirname(__file__), "dictionaries", style_name, "dictionary.json")
    dictionary = {}
    with resources.files("myosotis_chinese_dictionary").joinpath("dictionaries", style_name, "dictionary.json").open(
        "r", encoding="utf-8"
    ) as f:
        dictionaries[style_name] = json.load(f)


def pinyin_list(cc, style_name = "normal"):
    if style_name not in style_names:
        raise ValueError("Unsupported style name.")
    if len(cc) > 1:
        raise ValueError("The input string should contain exactly 1 character.")
    if cc in dictionaries[style_name].keys():
        return dictionaries[style_name][cc]
    return None

__all__ = ["pinyin_list"]
