import yaml
import os
from DBot_SDK.utils import WatchDogThread

class Authority:
    _config_path = ''
    _watch_dog = None
    _authorities = {}

    @classmethod
    def load_config(cls, config_path, reload_flag=False):
        def flatten_list(nested_list):
            """
            将嵌套列表展开成一个列表
            """
            result = []
            for item in nested_list:
                if isinstance(item, list):
                    result.extend(flatten_list(item))
                else:
                    result.append(item)
            return result
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            cls._authorities = config.get('authorities', {})
            if not reload_flag:
                cls._config_path = config_path
                cls._watch_dog = WatchDogThread(config_path, cls.reload_config)
                cls._watch_dog.start()

    @classmethod
    def reload_config(cls):
        cls.load_config(config_path=cls._config_path, reload_flag=True)


    @classmethod
    def get_permission(cls, group_id, qq_id):
        if not cls._authorities:
            cls.load_config(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'authority.yaml'))
        if group_id == None:
            group_id = 0
        # 如果该群不在配置文件中，不响应
        if group_id not in cls._authorities:
            return None
        # 全局权限
        global_permission = cls._authorities[-1].get(qq_id, {})['permission_level']
        if global_permission is not None:
            return global_permission
        # 获取该 QQ 号在该群组中的权限
        permission = cls._authorities[group_id].get(qq_id, {})['permission_level']
        # 默认权限
        if permission is None:
            return cls._authorities[0][0]['permission_level']
        # 已配置权限
        else:
            return permission

    @classmethod
    def check_command_permission(cls, command, group_id, qq_id):
        permission_level = cls.get_permission(group_id, qq_id)
        if permission_level < 0:  # 最高权限
            return True
        elif permission_level == 0:  # 禁止使用
            return False
        else:
            from DBot_SDK.app import FuncDict
            permission_level_need = FuncDict.get_permission_level(command)
            return permission_level >= permission_level_need


