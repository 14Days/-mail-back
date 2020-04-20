from flask import current_app, g
import re
from app.daos.ip import IIP, DaoIP
from app.daos.model import Filter
from app.models.errors import AddressError, AddressExist, AddressNotExist


class IPListData:
    def __init__(self, res, count):
        self.res = res
        self.count = count


class IIPManage:
    _ip: IIP
    _page: int
    _limit: int

    def __init__(self, ip_id=1, address=None, page=0, limit=10):
        self._ip_id = ip_id
        self._address = address
        self._page = page
        self._limit = limit
        self._ip = DaoIP()

    def add_ip(self, address) -> None:
        raise NotImplementedError()

    def delete_ip(self, ip_id) -> None:
        raise NotImplementedError()

    def get_ip_list(self) -> IPListData:
        raise NotImplementedError


class IPManage(IIPManage):
    _re_IP = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')

    def add_ip(self, address) -> None:
        if self._re_IP.match(address) is None:
            raise AddressError('请检查ip地址')
        ip = self._ip.query_ip_by_address(address)
        if ip is not None:
            raise AddressExist('ip已存在')
        self._ip.add_ip(address)
        return

    def delete_ip(self, ip_id) -> None:
        ip = self._ip.query_ip_by_id(ip_id)
        if ip is None:
            raise AddressNotExist('ip不存在')
        self._ip.delete_ip(ip)
        return

    def get_ip_list(self) -> IPListData:
        current_app.logger.debug('address: %s, page: %s, limit: %s', self._address, self._page, self._limit)
        ip_list, count = self._ip.get_ip_list(self._ip_id, self._address, self._page, self._limit)
        return IPListData(ip_list, count)
