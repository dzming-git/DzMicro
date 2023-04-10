import yaml
from dzmicro.utils import WatchDogThread
from typing import List, Union

class Authority:
    def __init__(self, uuid: str, is_platform: bool = False) -> None:
        self.uuid = uuid
        self.is_platform = is_platform
        self._config_path = ''
        self._watch_dog = None
        self._global_permission_first = False
        self._permission_level = {}
        self._authorities = {}
    
    def set_server_unique_info(self) -> None:
        from dzmicro.utils import singleton_server_manager
        self.server_unique_info = singleton_server_manager.get_server_unique_info(self.uuid)

    def load_config(self, config_path: str, reload_flag: bool = False) -> None:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self._authorities = config.get('AUTHORITIES', {})
            self._permission_level = config.get('PERMISSION_LEVEL', {})
            self._global_permission_first = config.get('GLOBAL_PERMISSION_FIRST', False)
            if not reload_flag:
                self._config_path = config_path
                self._watch_dog = WatchDogThread(config_path, self.reload_config)
                self._watch_dog.start()

    def reload_config(self) -> None:
        self.load_config(config_path=self._config_path, reload_flag=True)


    def get_permission_level(self, source_id: List[any]) -> int:
        source_id = [str(x_id) for x_id in source_id]
        # 回溯方法调取权限
        search_path_stack = []
        authorities = self._authorities
        id_index = 0
        max_index = len(source_id)
        recall_times = 0
        permission_level = None
        while True:
            x_id = source_id[id_index]
            if 'GLOBAL' in authorities and recall_times <= 0:
                if not self._global_permission_first and x_id not in authorities:
                    # 如果x_id没查询到，并且global优先为设定，则不使用global权限
                    # global优先未设定时，只有参与配置的id可以使用global权限
                    break
                search_path_stack.append([id_index, authorities, recall_times])  # 记录回溯节点
                authorities = authorities.get('GLOBAL')
            elif x_id in authorities and recall_times <= 1:
                search_path_stack.append([id_index, authorities, recall_times])  # 记录回溯节点
                authorities = authorities.get(x_id)
            elif 'DEFAULT' in authorities and recall_times <= 2:
                search_path_stack.append([id_index, authorities, recall_times])  # 记录回溯节点
                authorities = authorities.get('DEFAULT')
            elif search_path_stack:
                # 找不到权限信息，回溯
                id_index, authorities, recall_times = search_path_stack.pop()
                recall_times += 1
                continue
            id_index += 1
            recall_times = 0
            if id_index >= max_index or 'PERMISSION' in authorities:
                permission_level = authorities.get('PERMISSION', None)
                break
        return permission_level

    def get_permission_by_level(self, level: int) -> Union[str, None]:
        for permission, l in self._permission_level.items():
            if l == level:
                return permission
        return None

    def check_command_permission(self, command: str, source_id: List[any]) -> Union[bool, None]:
        '''
        特殊权限：
        -3 只准内部调用，不对用户开放
        -2 最高权限，可以调用一切外部调用的指令
        -1 禁止使用一切指令
        '''
        permission_level = self.get_permission_level(source_id)
        func_dict = self.server_unique_info .func_dict
        permission_need = func_dict.get_permission(command)
        permission_level_need = self._permission_level.get(permission_need, None)
        # func_dict中权限配置错误
        if permission_level_need is None:
            print('func_dict中权限配置错误')
            return None
        # 只准内部调用，不对用户开放
        if permission_level_need == -3:
            return None
        # 该群没有被配置
        if permission_level is None:
            return None
        # 最高权限
        if permission_level == -2:
            return True
        # 禁止权限
        if permission_level == -1:
            return False
        # 一般权限
        return permission_level >= permission_level_need
