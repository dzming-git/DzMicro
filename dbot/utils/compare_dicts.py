# compare_dict.py
def compare_dicts(dict1, dict2):
    """
    比较两个字典的不同之处，返回三个字典（增加的内容，删除的内容，修改的内容）
    """
    added = {}
    deleted = {}
    modified = {}

    # 查找增加的内容
    for key in dict2.keys() - dict1.keys():
        added[key] = dict2[key]

    # 查找删除的内容
    for key in dict1.keys() - dict2.keys():
        deleted[key] = dict1[key]

    # 查找修改的内容
    for key in dict1.keys() & dict2.keys():
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            # 递归处理嵌套字典
            sub_added, sub_deleted, sub_modified = compare_dicts(dict1[key], dict2[key])
            if sub_added:
                added[key] = sub_added
            if sub_deleted:
                deleted[key] = sub_deleted
            if sub_modified:
                modified[key] = sub_modified
        elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
            # 处理嵌套列表
            if dict1[key] != dict2[key]:
                modified[key] = {'old': dict1[key], 'new': dict2[key]}
        elif dict1[key] != dict2[key]:
            # 处理其他类型的变化
            if dict1[key] == '' and dict2[key] != '':
                added[key] = dict2[key]
            elif dict1[key] != '' and dict2[key] == '':
                deleted[key] = dict1[key]
            else:
                modified[key] = {'old': dict1[key], 'new': dict2[key]}

    return added, deleted, modified
