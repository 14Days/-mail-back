from app.daos import session_commit
from app.daos.model import Server


class IServer:
    def query_server(self) -> Server:
        raise NotImplementedError()

    def modify_smtp_state(self, state):
        raise NotImplementedError()

    def modify_pop_state(self, state):
        raise NotImplementedError()

    def modify_smtp_port(self, port):
        raise NotImplementedError()

    def modify_pop_port(self, port):
        raise NotImplementedError()


class DaoServer(IServer):
    def query_server(self):
        return Server.query. \
            filter_by(id=1). \
            first()

    def modify_smtp_state(self, state):
        server = self.query_server()
        server.smtp_on = state
        session_commit()

    def modify_pop_state(self, state):
        server = self.query_server()
        server.pop_on = state
        session_commit()

    def modify_smtp_port(self, port):
        server = self.query_server()
        server.smtp_port = port
        session_commit()

    def modify_pop_port(self, port):
        server = self.query_server()
        server.pop_port = port
        session_commit()
