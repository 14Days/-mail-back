from app.daos.server import IServer, DaoServer
from app.daos.model import Server


class ServerData:
    def __init__(self, server: Server):
        self.pop_port = server.pop_port
        self.pop_state = server.pop_on
        self.smtp_port = server.smtp_port
        self.smtp_state = server.smtp_on


class ManageServer:
    _server: IServer

    def __init__(self):
        self._server = DaoServer()

    def get_server_info(self):
        server = self._server.query_server()
        return ServerData(server)
