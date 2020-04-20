import datetime
from typing import List, Dict, Any
from app.daos import db, session_commit
from app.daos.model import Filter


class IPListData:
    def __init__(self, ip_id, address):
        self.ip_id = ip_id
        self.address = address


class IIP:
    def query_ip_by_address(self, address: str) -> Filter:
        raise NotImplementedError()

    def query_ip_by_id(self, ip_id: int) -> Filter:
        raise NotImplementedError()

    def add_ip(self, address: str) -> None:
        raise NotImplementedError()

    def delete_ip(self, ip: Filter) -> None:
        raise NotImplementedError()

    def get_ip_list(self, ip_id: int, address: str, page: int, limit: int) -> (List[Dict[str, Any]], int):
        raise NotImplementedError()


class DaoIP(IIP):
    def query_ip_by_address(self, address):
        return Filter.query. \
            filter_by(address=address). \
            filter_by(delete_at=None). \
            first()

    def query_ip_by_id(self, uid):
        return Filter.query. \
            filter_by(id=uid). \
            filter_by(delete_at=None). \
            first()

    def add_ip(self, address: str) -> None:
        ip = Filter(address=address)
        db.session.add(ip)
        session_commit()

    def delete_ip(self, ip: Filter) -> None:
        ip.delete_at = datetime.datetime.now()
        session_commit()

    def get_ip_list(self, ip_id: int, address: str, page: int, limit: int) -> (List[Dict[str, Any]], int):
        sql = Filter.query. \
            filter(Filter.delete_at.is_(None))

        temp = sql.limit(limit).offset(page * limit).all()
        count = sql.count()

        ip_list: List[Dict[str, Any]] = []
        for item in temp:
            ip_list.append(IPListData(item.id, item.address).__dict__)

        return ip_list, count
