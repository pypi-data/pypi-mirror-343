from urllib.parse import unquote

from pydantic import EncodedStr, EncoderProtocol
from typing_extensions import Annotated


class MyEncoder(EncoderProtocol):
    @classmethod
    def decode(cls, data: bytes) -> bytes:
        return str.encode(unquote(data))


URLEncodedStr = Annotated[str, EncodedStr(encoder=MyEncoder)]
