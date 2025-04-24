from yyAutoAiframework.client import BaseAIClient

"""
管理DialogManager 的工厂实现类
主要用于维护创建的dialogManager 的状态
"""
class DialogManagerFactory:
    # 定义dialogManage 的对象集合
    _dialog_managers = {}
    #定义是否可以初始化
    __is_can_initialize = False
    """
    不允许外部直接调用
    """
    def __init__(self, client: BaseAIClient):
        if DialogManagerFactory.__is_can_initialize :  # 内部使用标记，不允许外部程序直接实例化
            self._dm_map = {}
            self.client = client
        else:
            raise RuntimeError("Direct instantiation is not allowed. Use 'create_dm_factory' instead.")

    """
    获取DialogManager Factory 
    对于同一个client 只创建一个DialogManagerFactory
    """
    @staticmethod
    def create_dm_factory(client: BaseAIClient):
        if client in DialogManagerFactory._dialog_managers:
            return DialogManagerFactory._dialog_managers[client]
        else:
            DialogManagerFactory.__is_can_initialize = True
            dm_factory =  DialogManagerFactory(client)
            DialogManagerFactory._dialog_managers[client] = dm_factory
            DialogManagerFactory.__is_can_initialize = False
            return dm_factory


    """
    获取对话管理实例
    """
    def get_dialog_manager(self, session_id:str,system_prompt: str = None, assistant_prompt: str = None):
        from yyAutoAiframework.agi_common.DialogManager import DialogManager
        if session_id in self._dm_map:
            return self._dm_map[session_id]
        else:
            DialogManager.authorized_caller = "DialogManagerFactory"
            dm = DialogManager(self,session_id,system_prompt,assistant_prompt)
            self._dm_map[session_id] = dm
            DialogManager.authorized_caller = None
            return dm