import sys
import urllib.parse
import gzip
import zlib
import base64
import random
import brotli
from typing import Optional, Union


class ContentConcealing:
    def get_tool_name(self) -> str:
        return "None"

    def encode(self, pure_text: str) -> str:
        return pure_text

    def decode(self, encoded_text: str) -> str:
        return encoded_text

    @staticmethod
    def create_concealing_tool(tool_name: str):
        if tool_name == "url":
            return UrlConcealing()
        elif tool_name == "gzip":
            return GZipConcealing()
        elif tool_name == "br":
            return BrotliConcealing()
        elif tool_name == "def":
            return DeflateConcealing()
        elif tool_name == "b64":
            return Base64Concealing()
        elif tool_name == "b85a":
            return Base85AConcealing()
        elif tool_name == "b85b":
            return Base85BConcealing()
        elif tool_name == "b32":
            return Base32Concealing()
        elif tool_name == "b16":
            return Base16Concealing()
        else:
            print("Unknown tool!")

    @staticmethod
    def get_random_concealing_tool():
        random_tool_index = random.randrange(0, 9)
        print(random_tool_index)
        if random_tool_index == 0:
            return UrlConcealing()
        elif random_tool_index == 1:
            return GZipConcealing()
        elif random_tool_index == 2:
            return BrotliConcealing()
        elif random_tool_index == 3:
            return DeflateConcealing()
        elif random_tool_index == 4:
            return Base64Concealing()
        elif random_tool_index == 5:
            return Base85AConcealing()
        elif random_tool_index == 6:
            return Base85BConcealing()
        elif random_tool_index == 7:
            return Base32Concealing()
        elif random_tool_index == 8:
            return Base16Concealing()
        else:
            print("Unknown tool!")

    @staticmethod
    def create_random_concealing_array(unique=True, non_unique_length=20):
        concealing_list = list['ContentConcealing']()
        if unique:
            concealing_list.append(UrlConcealing())
            concealing_list.append(GZipConcealing())
            concealing_list.append(BrotliConcealing())
            concealing_list.append(DeflateConcealing())
            concealing_list.append(Base64Concealing())
            concealing_list.append(Base85AConcealing())
            concealing_list.append(Base85BConcealing())
            concealing_list.append(Base32Concealing())
            concealing_list.append(Base16Concealing())
        else:
            for index in range(0, non_unique_length):
                concealing_list.append(ContentConcealing.get_random_concealing_tool())
        return concealing_list

    @staticmethod
    def get_random_concealing_tool_from_array(concealing_array: list['ContentConcealing']):
        random_tool_index = random.randrange(0, len(concealing_array))
        return concealing_array[random_tool_index]

    @staticmethod
    def random_conceal_text(text: str,
                            concealing_array: Optional[list['ContentConcealing']] = None,
                            depth: int = 20) -> (str, str):
        applied_methods = ""
        if not concealing_array:
            concealing_array = ContentConcealing.create_random_concealing_array()
        for index in range(0, depth):
            conceal_method = ContentConcealing.get_random_concealing_tool_from_array(concealing_array)
            conceal_method_name = conceal_method.get_tool_name()
            text = conceal_method.encode(text)
            if applied_methods == "":
                applied_methods = conceal_method_name
            else:
                applied_methods = conceal_method_name + ";" + applied_methods
        return text, applied_methods

    @staticmethod
    def unconceal_text(concealed_text: str, applied_methods: str):
        for applied_method in applied_methods.split(";"):
            conceal_method = ContentConcealing.create_concealing_tool(applied_method)
            concealed_text = conceal_method.decode(concealed_text)
        return concealed_text


class UrlConcealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "url"

    def encode(self, pure_text: str) -> str:
        return urllib.parse.quote_plus(pure_text)

    def decode(self, encoded_text: str) -> str:
        return urllib.parse.unquote_plus(encoded_text)


class GZipConcealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "gzip"

    def encode(self, pure_text: Union[str, bytes]) -> str:
        if not type(pure_text) is bytes:
            pure_text = pure_text.encode()
        return urllib.parse.quote_from_bytes(gzip.compress(pure_text))

    def decode(self, encoded_text: str) -> str:
        return gzip.decompress(urllib.parse.unquote_to_bytes(encoded_text)).decode()


class BrotliConcealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "br"

    def encode(self, pure_text: str) -> str:
        if not type(pure_text) is bytes:
            pure_text = pure_text.encode()
        return urllib.parse.quote_from_bytes(brotli.compress(pure_text))

    def decode(self, encoded_text: str) -> bytes:
        return brotli.decompress(urllib.parse.unquote_to_bytes(encoded_text)).decode()


class DeflateConcealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "def"

    def encode(self, pure_text: str) -> str:
        if not type(pure_text) is bytes:
            pure_text = pure_text.encode()
        return urllib.parse.quote_from_bytes(zlib.compress(pure_text))

    def decode(self, encoded_text: str) -> str:
        return zlib.decompress(urllib.parse.unquote_to_bytes(encoded_text)).decode()


class Base64Concealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "b64"

    def encode(self, pure_text: str) -> str:
        if type(pure_text) is str:
            pure_text = pure_text.encode()
        return base64.b64encode(pure_text).decode()

    def decode(self, encoded_text: str) -> str:
        return str(base64.b64decode(encoded_text).decode())


class Base85BConcealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "b85b"

    def encode(self, pure_text: str) -> str:
        if type(pure_text) is str:
            pure_text = pure_text.encode()
        return base64.b85encode(pure_text).decode()

    def decode(self, encoded_text: str) -> str:
        return str(base64.b85decode(encoded_text).decode())


class Base85AConcealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "b85a"

    def encode(self, pure_text: str) -> str:
        if type(pure_text) is str:
            pure_text = pure_text.encode()
        return base64.a85encode(pure_text).decode()

    def decode(self, encoded_text: str) -> str:
        return str(base64.a85decode(encoded_text).decode())


class Base32Concealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "b32"

    def encode(self, pure_text: str) -> str:
        if type(pure_text) is str:
            pure_text = pure_text.encode()
        return base64.b32encode(pure_text).decode()

    def decode(self, encoded_text: str) -> str:
        return str(base64.b32decode(encoded_text).decode())


class Base16Concealing(ContentConcealing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_tool_name(self) -> str:
        return "b16"

    def encode(self, pure_text: str) -> str:
        if type(pure_text) is str:
            pure_text = pure_text.encode()
        return base64.b16encode(pure_text).decode()

    def decode(self, encoded_text: str) -> str:
        return str(base64.b16decode(encoded_text).decode())


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Error missing flag with name concealing or unconcealing!")
        exit(1)
        print(sys.argv[1])
    if sys.argv[1] == "-unconcealing":
        concealed_text = None
        key = None
        if sys.argv[2] == "-key":
            key = sys.argv[3]
            with sys.stdin as file:
                concealed_text = file.read()
        else:
            print("Error: Missing text and key flag!")
            exit(2)
        unconcealed_text = ContentConcealing.unconceal_text(concealed_text.strip(), applied_methods=key)
        print(unconcealed_text)
    elif sys.argv[1] == "-concealing":
        pass
    else:
        print("Error: Unknown option! Missing flag with name concealing or unconcealing!")
        exit(1)
