# urlencoding_message.py
import re
import urllib

def urlencoding_message(message):
    # split the string using the pattern
    cqcode_first = message.startswith("[CQ:")
    cqcodes = re.findall(r"\[CQ:[^\]]*\]", message)
    others = re.split(r"\[CQ:[^\]]*\]", message)
    # remove empty strings from others list
    others = [urllib.parse.quote(x) for x in others if x]
    # others = [x for x in others if x]

    # construct the list to concatenate the strings back together
    new_list = []
    cqcodes_index = 0
    cqcodes_len = len(cqcodes)
    others_index = 0
    others_len = len(others)

    if cqcode_first:
        new_list.append(cqcodes[cqcodes_index])
        cqcodes_index += 1
    while others_index < others_len or cqcodes_index < cqcodes_len:
        if others_index < others_len:
            new_list.append(others[others_index])
            others_index += 1
        if cqcodes_index < cqcodes_len:
            new_list.append(cqcodes[cqcodes_index])
            cqcodes_index += 1

    # concatenate the strings back together
    new_string = "".join(new_list)
    return new_string
