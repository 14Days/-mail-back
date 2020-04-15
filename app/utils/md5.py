import hashlib


class MD5:
    @classmethod
    def encode_md5(cls, temp: str) -> str:
        md5 = hashlib.md5()
        md5.update(temp.encode(encoding='utf-8'))

        return md5.hexdigest()
