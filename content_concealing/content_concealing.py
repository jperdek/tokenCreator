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


def test():
    content_concealing1: ContentConcealing = UrlConcealing()
    encoded_url = content_concealing1.encode("{This, is; text}")
    print("Url encoding")
    print(encoded_url)
    print(content_concealing1.decode(encoded_url))
    print("2x encoded")
    print(content_concealing1.encode(encoded_url))
    print("")
    print("")

    content_concealing2: ContentConcealing = GZipConcealing()
    encoded_gzip = content_concealing2.encode("{This, is; text}")
    print("Gzip encoding")
    print(encoded_gzip)
    print(content_concealing2.decode(encoded_gzip))
    print("2x encoded")
    print(content_concealing2.encode(encoded_gzip))
    print("")
    print("")

    content_concealing3: ContentConcealing = BrotliConcealing()
    encoded_brotli = content_concealing3.encode("{This, is; text}")
    print("Brotli encoding")
    print(encoded_brotli)
    print(content_concealing3.decode(encoded_brotli))
    print("2x encoded")
    print(content_concealing3.encode(encoded_brotli))
    print("")
    print("")

    content_concealing4: ContentConcealing = DeflateConcealing()
    encoded_deflate = content_concealing4.encode("{This, is; text}")
    print("Deflate encoding")
    print(encoded_deflate)
    print(content_concealing4.decode(encoded_deflate))
    print("2x encoded")
    print(content_concealing4.encode(encoded_deflate))
    print("")
    print("")

    content_concealing5: ContentConcealing = Base64Concealing()
    encoded_base64 = content_concealing5.encode("{This, is; text}")
    print("Bae64 encoding")
    print(encoded_base64)
    print(content_concealing5.decode(encoded_base64))
    print("2x encoded")
    a = content_concealing5.encode(encoded_base64)
    print(content_concealing5.encode(encoded_base64))
    print(content_concealing5.decode(content_concealing5.decode(a)))
    print("")
    print("")

    content_concealing6: ContentConcealing = Base85BConcealing()
    encoded_base85b = content_concealing6.encode("{This, is; text}")
    print("Base85 B encoding")
    print(encoded_base85b)
    print(content_concealing6.decode(encoded_base85b))
    print("2x encoded")
    a = content_concealing6.encode(encoded_base85b)
    print(content_concealing6.encode(encoded_base85b))
    print(content_concealing6.decode(content_concealing6.decode(a)))
    print("")
    print("")

    content_concealing7: ContentConcealing = Base85AConcealing()
    encoded_base85a = content_concealing7.encode("{This, is; text}")
    print("Base85 A encoding")
    print(encoded_base85a)
    print(content_concealing7.decode(encoded_base85a))
    print("2x encoded")
    a = content_concealing7.encode(encoded_base85a)
    print(content_concealing7.encode(encoded_base85a))
    print(content_concealing7.decode(content_concealing7.decode(a)))
    print("")
    print("")

    content_concealing8: ContentConcealing = Base32Concealing()
    encoded_base32 = content_concealing8.encode("{This, is; text}")
    print("Base32 encoding")
    print(encoded_base32)
    print(content_concealing8.decode(encoded_base32))
    print("2x encoded")
    a = content_concealing8.encode(encoded_base32)
    print(content_concealing8.encode(encoded_base32))
    print(content_concealing8.decode(content_concealing8.decode(a)))
    print("")
    print("")

    content_concealing9: ContentConcealing = Base16Concealing()
    encoded_base16 = content_concealing9.encode("{This, is; text}")
    print("Base16 encoding")
    print(encoded_base16)
    print(content_concealing9.decode(encoded_base16))
    print("2x encoded")
    a = content_concealing9.encode(encoded_base16)
    print(content_concealing9.encode(encoded_base16))
    print(content_concealing9.decode(content_concealing9.decode(a)))
    print("")
    print("")

    ContentConcealing.create_random_concealing_array()
    ContentConcealing.create_random_concealing_array(unique=False, non_unique_length=50)
    concealed_text, conceal_methods = ContentConcealing.random_conceal_text(
        "My text is unconcealed and needs to be hidden!")
    print("Concealed text:")
    print(concealed_text)
    print("")
    print("")

    print("Concealed methods:")
    print(conceal_methods)
    print("")
    print("")

    print("Text unconcealed:")
    unconcealed_text = ContentConcealing.unconceal_text(concealed_text, applied_methods=conceal_methods)
    print(unconcealed_text)


if __name__ == "__main__":
    test()
