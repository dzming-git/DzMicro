import yaml
import os
from DBot_SDK.utils import WatchDogThread

class Authority:
    _config_path = ''
    _watch_dog = None
    _global_permission_first = False
    _permission_level = {}
    _authorities = {}

    @classmethod
    def load_config(cls, config_path, reload_flag=False):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            cls._authorities = config.get('AUTHORITIES', {})
            cls._permission_level = config.get('PERMISSION_LEVEL', {})
            cls._global_permission_first = config.get('GLOBAL_PERMISSION_FIRST', False)
            if not reload_flag:
                cls._config_path = config_path
                cls._watch_dog = WatchDogThread(config_path, cls.reload_config)
                cls._watch_dog.start()

    @classmethod
    def reload_config(cls):
        cls.load_config(config_path=cls._config_path, reload_flag=True)


    @classmethod
    def get_permission_level(cls, group_id, qq_id):
        permission_level = 0
        if not cls._authorities:
            cls.load_config(cls._config_path)
        if group_id == None:
            group_id = 'PRIVATE'  # 私聊当作特殊的群聊处理
        is_grooup_configured = group_id in cls._authorities
        is_global_permission = qq_id in cls._authorities.get('GLOBAL', {})
        # 该qq有全局权限
        if is_global_permission:
            # 全局权限优先 或 该群被配置
            if cls._global_permission_first or is_grooup_configured:
                permission_level = cls._authorities.get('GLOBAL', {}).get(qq_id, {}).get('PERMISSION', 'NONE')
            else:
                permission_level = 0
        # 该qq无全局权限
        else:
            # 获取该 QQ 号在该群组中的权限
            permission_level = cls._authorities.get(group_id, {}).get(qq_id, {}).get('PERMISSION', None)
            # 默认权限
            if permission_level is None:
                permission_level = cls._authorities.get(group_id, {}).get('DEFAULT', {}).get('PERMISSION', None)
        return permission_level

    @classmethod
    def check_command_permission(cls, command, group_id, qq_id):
        '''
        特殊权限：
        -3 只准内部调用，不对用户开放
        -2 最高权限，可以调用一切外部调用的指令
        -1 禁止使用一切指令
        '''
        permission_level = cls.get_permission_level(group_id, qq_id)
        from DBot_SDK.app import FuncDict
        permission_need = FuncDict.get_permission(command)
        permission_level_need = cls._permission_level.get(permission_need, None)
        # func_dict中权限配置错误
        if permission_level_need is None:
            print('func_dict中权限配置错误')
            return None
        # 只准内部调用，不对用户开放
        if permission_level_need == -3:
            return None
        # 最高权限
        if permission_level == -2:
            return True
        # 禁止权限
        if permission_level == -1:
            return False
        # 一般权限
        return permission_level >= permission_level_need


