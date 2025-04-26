import struct
from io import BytesIO
from typing import Any, cast


class T:
    CHAR = "c"
    SIGNED_CHAR = "b"
    UNSIGNED_CHAR = "B"
    BOOL = "?"
    SHORT = "h"
    UNSIGNED_SHORT = "H"
    INT = "i"
    UNSIGNED_INT = "I"
    LONG = "l"
    UNSIGNED_LONG = "L"
    LONG_LONG = "q"
    UNSIGNED_LONG_LONG = "Q"
    FLOAT = "f"
    DOUBLE = "d"
    STRING = "s"
    VOID_PTR = "P"

    PY_STRUCT = "%STRUCT%"
    PY_STRUCT_LIST = "%STRUCT_LIST%"


def TP(*types):
    return " ".join(types)


class EasyStruct:
    """
    一个结构体, 用于快速创建C结构

    A struct for create C struct
    """

    def __init__(self):
        self.attr_now = False
        self.members = []

    def get_ref(self, type_: str, value: Any = 0):
        self.attr_now = True
        self.members.append((None, type_))
        return value

    def __setattr__(self, key, value):
        if key == "attr_now":
            return super().__setattr__(key, value)
        if self.attr_now:
            self.members[-1] = (key, self.members[-1][1])
            self.attr_now = False
        return super().__setattr__(key, value)

    @property
    def binary(self):
        bits = b""
        for key, type_ in self.members:
            value = getattr(self, key) if key else 0
            if isinstance(value, EasyStruct):
                content_bits = value.binary
            elif isinstance(value, list) and isinstance(value[0], EasyStruct):
                content_bits = b''.join(x.binary for x in value)
            elif isinstance(type_, str):
                if type_ == T.STRING:
                    content_bits = value
                else:
                    content_bits = struct.pack(type_, value)
            else:
                raise NotImplementedError()
            bits += content_bits
        return bits


class CurFile(EasyStruct):
    def __init__(self):
        super().__init__()
        self.file_head: CurHead = self.get_ref(T.PY_STRUCT, CurHead())
        self.entries: list[CurEntry] = self.get_ref(T.PY_STRUCT_LIST, [])
        self.bitmaps: list[Bitmap] = self.get_ref(T.PY_STRUCT_LIST, [])

    @property
    def binary(self):
        file_head = cast(CurHead, self.file_head)
        file_head.count = len(self.entries)

        now_offset = len(self.entries) * 16 + 6
        for entry in self.entries:
            entry.bitmap_offset = now_offset
            now_offset += entry.bitmap_size
        entry_bits = b''.join(x.binary for x in self.entries)

        return file_head.binary + entry_bits + b''.join(x.binary for x in self.bitmaps)


class CurHead(EasyStruct):
    def __init__(self):
        super().__init__()
        self.get_ref(T.UNSIGNED_SHORT)
        self.type: int = self.get_ref(T.UNSIGNED_SHORT, 2)
        self.count: int = self.get_ref(T.UNSIGNED_SHORT)


class CurEntry(EasyStruct):  # 16 Bytes
    def __init__(self):
        super().__init__()
        self.width = self.get_ref(T.UNSIGNED_CHAR)
        self.height = self.get_ref(T.UNSIGNED_CHAR)
        self.planes = self.get_ref(T.UNSIGNED_CHAR)
        self.get_ref(T.UNSIGNED_CHAR)  # none used
        self.x_hotspot = self.get_ref(T.UNSIGNED_SHORT)
        self.y_hotspot = self.get_ref(T.UNSIGNED_SHORT)
        self.bitmap_size = self.get_ref(T.UNSIGNED_INT)  # 指向的Bitmap的大小 - Bitmap Size
        self.bitmap_offset = self.get_ref(T.UNSIGNED_INT)  # 指向的Bitmap相对于文件头的偏移量 - Bitmap Offset


class BitmapHeader(EasyStruct):  # 40 Bytes
    def __init__(self):
        super().__init__()
        self.head_length = self.get_ref(T.UNSIGNED_INT, 40)
        self.width = self.get_ref(T.UNSIGNED_INT)
        self.height = self.get_ref(T.UNSIGNED_INT)
        self.planes = self.get_ref(T.UNSIGNED_SHORT, 1)
        self.pixel_bits = self.get_ref(T.UNSIGNED_SHORT, 32)  # RGBA
        self.compress_type = self.get_ref(T.UNSIGNED_INT, 0)  # 0: 无压缩 - 0: uncompressed
        self.image_data_length = self.get_ref(T.UNSIGNED_INT, 0)

        self.none_used = self.get_ref(T.STRING, b"")  # 未使用 - none used (16bit)
        self.none_used = b"\x00" * 16


class Pixel(EasyStruct):
    def __init__(self, r: int, g: int, b: int, a: int):
        super().__init__()
        self.b = self.get_ref(T.UNSIGNED_CHAR, b)
        self.g = self.get_ref(T.UNSIGNED_CHAR, g)
        self.r = self.get_ref(T.UNSIGNED_CHAR, r)
        self.a = self.get_ref(T.UNSIGNED_CHAR, a)  # FF是完全不透明, 00是完全透明 - Alpha


class XORBitmap(EasyStruct):
    def __init__(self):
        super().__init__()
        self.width = 0  # 仅用于计算 - Only for Calculate
        self.height = 0  # 仅用于计算 - Only for Calculate
        self.pixels: list[Pixel] = self.get_ref(T.PY_STRUCT_LIST, [])

    @property
    def binary(self):
        bits = super().binary
        return reverse_bitmap_lines(bits, self.width, self.height)


class ANDBitmap(EasyStruct):
    def __init__(self):
        super().__init__()
        # 单色图 (0: 不透明, 1: 透明) - Binary Bitmap (1: transparent, 0: not transparent)
        self.pixel_data = self.get_ref(T.STRING)


class Bitmap(EasyStruct):
    def __init__(self):
        super().__init__()
        self.header: BitmapHeader = self.get_ref(T.PY_STRUCT, BitmapHeader())
        self.xor_bitmap: XORBitmap = self.get_ref(T.PY_STRUCT, XORBitmap())  # 存储颜色 - Store Color
        self.and_bitmap: ANDBitmap = self.get_ref(T.PY_STRUCT, ANDBitmap())  # 存储透明相关像素 - Alpha like transparent


def reverse_bitmap_lines(bitmap_data: bytes, width: int, height: int, bit: int = 4) -> bytes:
    data_array = bytearray(bitmap_data)
    lines = []
    for i in range(height):
        lines.append(data_array[i * width * bit: (i + 1) * width * bit])
    lines.reverse()
    return bytes().join(lines)


def binary_list_to_bytes(binary_list):
    byte_values = bytearray()
    for i in range(0, len(binary_list), 8):
        bits = binary_list[i:i + 8]
        byte_val = 0
        for bit in bits:
            byte_val = (byte_val << 1) | bit
        byte_values.append(byte_val)
    return bytes(byte_values)


class Cursor:
    """
    一个鼠标指针文件, 可包含多个指针

    A mouse pointer file, can contain multiple pointers.

    参考 (Ref):

    https://blog.csdn.net/chenyujing1234/article/details/8747328

    https://www.daubnet.com/en/file-format-cur
    """

    def __init__(self):
        self.cur_file = CurFile()

    def add_cursor(self, width: int, height: int, x_hotspot: int, y_hotspot: int, bitmap_data: bytes):
        """
        添加鼠标指针进入文件
        Add a cursor into file
        :param width: 指针宽度 (bitmap width)
        :param height: 指针高度 (bitmap height)
        :param x_hotspot: 指针x热点 (cursor hotspot x)
        :param y_hotspot: 指针y热点 (cursor hotspot y)
        :param bitmap_data: 位图数据 (必须为RGBA) (Bitmap raw data (Must be RGBA mode))
        :return: 无
        """
        # 初始化位图对象 - Init Bitmap
        bitmap = Bitmap()
        bitmap_header = bitmap.header
        bitmap_header.width = width
        bitmap_header.height = height * 2
        bitmap_header.image_data_length = (width * height * 4) + (width * height // 8)

        # 初始化 XOR 位图 (存储颜色) - Init XOR Bitmap (Store color)
        xor_bitmap = bitmap.xor_bitmap
        xor_bitmap.width = width
        xor_bitmap.height = height
        data_array = bytearray(bitmap_data)
        for i in range(width * height):
            pixel = Pixel(data_array[i * 4], data_array[i * 4 + 1], data_array[i * 4 + 2], data_array[i * 4 + 3])
            xor_bitmap.pixels.append(pixel)

        # 初始化 AND 位图 (存储透明度相关) - Init AND Bitmap (Store alpha like transparent)
        and_bitmap = cast(ANDBitmap, bitmap.and_bitmap)
        binary_list = [0 if pixel.a else 1 for pixel in xor_bitmap.pixels]
        line_list = [binary_list[i * width:i * width + width] for i in range(height)]
        line_list.reverse()
        binary_list = []
        for line in line_list:
            binary_list.extend(line)
        and_bitmap.pixel_data = binary_list_to_bytes(binary_list)

        # 初始化 CUR 入口 - Init CUR Entry
        entry = CurEntry()
        entry.width = width
        entry.height = height
        entry.x_hotspot = x_hotspot
        entry.y_hotspot = y_hotspot
        entry.bitmap_size = 40 + bitmap_header.image_data_length
        # entry.offset -> 稍后封装文件时再计算 - offset will be calculated when saving file

        self.cur_file.entries.append(entry)
        self.cur_file.bitmaps.append(bitmap)

    def save_file(self, file: BytesIO | str):
        """
        保存Cur文件到路径或IO

        Save Cur file to path or IO

        :param file: 文件路径或者BytesIO - File path or BytesIO
        :return: None
        """
        file_binary = self.cur_file.binary
        if isinstance(file, BytesIO):
            file.write(file_binary)
        else:
            with open(file, 'wb') as f:
                f.write(file_binary)