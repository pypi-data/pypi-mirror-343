from lavender_pinyin import *


def name_taboo(content):
    cc_list = list(content)
    l = len(cc_list)
    for i in range(l):
        pinyins = pinyin_list(cc_list[i])
        if not pinyins:
            continue
        if "xi" in pinyins or "jin" in pinyins or "ping" in pinyins:
            cc_list[i] = "*"
    return "".join(cc_list)


__all__ = ["name_taboo"]
