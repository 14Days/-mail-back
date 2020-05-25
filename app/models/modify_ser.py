from typing import Dict, Any
from app.daos.server import IServer, DaoServer
from app.models.errors import PropertyNotExist, StateNotExist, PortOutOfRange


class ModifySer:
    _data: Dict[str, Any]
    _dao_ser: DaoServer

    def __init__(self, data):
        self._data = data
        self._dao_ser = DaoServer()
        self._handle_dict()
        pass

    def _handle_dict(self):
        for key, val in self._data.items():
            method = getattr(self, f'handle_{key}', None)
            if method is None:
                raise PropertyNotExist(f'{key} 属性不存在')
            method(val)

    def handle_pop_state(self, pop_state):
        if pop_state != 0 and pop_state != 1:
            raise StateNotExist("pop服务无此状态")
        self._dao_ser.modify_pop_state(pop_state)

    def handle_pop_port(self, pop_port):
        if pop_port < 1 or pop_port > 65535:
            raise PortOutOfRange("不在正常端口范围")
        self._dao_ser.modify_pop_port(pop_port)

    def handle_smtp_state(self, smtp_state):
        if smtp_state != 0 and smtp_state != 1:
            raise StateNotExist("smtp服务无此状态")
        self._dao_ser.modify_smtp_state(smtp_state)

    def handle_smtp_port(self, smtp_port):
        if smtp_port < 1 or smtp_port > 65535:
            raise PortOutOfRange("不在正常端口范围")
        self._dao_ser.modify_smtp_port(smtp_port)


def manage_server(data) -> ModifySer.__class__:
    return ModifySer(data)
