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

    def __init__(self, address=None, page=0, limit=10):
        self._address = address
        self._page = page
        self._limit = limit
        self._ip = DaoIP()

    def add_black_ip(self, address) -> None:
        raise NotImplementedError()

    def delete_black_ip(self, address) -> None:
        raise NotImplementedError()

    def get_ip_list(self) -> IPListData:
        raise NotImplementedError


class IPManage(IIPManage):
    _re_IP = re.compile(r'^((25[0-5]|2[0-4]\\d|[1]{1}\\d{1}\\d{1}|[1-9]{1}\\d{1}|\\d{1})($|(?!\\.$)\\.)){4}$')

    def add_black_ip(self, address) -> None:
        if self._re_IP.match(address) is None:
            raise AddressError('请检查ip地址')
        ip = self._ip.query_ip_by_address(address)
        if ip is not None:
            raise AddressExist('ip已存在')
        self.add_black_ip(address)
        return

    def delete_black_ip(self, address) -> None:
        ip = self._ip.query_ip_by_address(address)
        if ip is not None:
            raise AddressNotExist('ip不存在')
        self.delete_black_ip(address)
        return

    def get_ip_list(self) -> IPListData:
        current_app.logger.debug('address: %s, page: %s, limit: %s', self._address, self._page, self._limit)
        ip_list, count = self._ip.get_ip_list(self._address, self._page, self._limit)
        return IPListData(ip_list, count)
