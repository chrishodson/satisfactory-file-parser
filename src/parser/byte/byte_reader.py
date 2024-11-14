from src.parser.error.parser_error import CorruptSaveError
from src.parser.byte.alignment_enum import Alignment
from src.parser.byte.binary_readable_interface import BinaryReadable

class ByteReader(BinaryReadable):

    def __init__(self, file_buffer: bytearray, alignment: Alignment):
        self.alignment = alignment
        self.reset(file_buffer)

    def reset(self, new_file_buffer: bytearray):
        self.file_buffer = new_file_buffer
        self.buffer_view = memoryview(new_file_buffer)
        self.max_byte = len(new_file_buffer)
        self.current_byte = 0
        self.handled_byte = 0

    def skip_bytes(self, byte_length: int = 1):
        self.current_byte += byte_length

    def read_byte(self) -> int:
        return int(self.buffer_view[self.current_byte])

    def read_bytes(self, count: int) -> bytearray:
        bytes_array = bytearray(count)
        for i in range(count):
            bytes_array[i] = self.buffer_view[self.current_byte + i]
        self.current_byte += count
        return bytes_array

    def bytes_to_hex_representation(self, bytes_array: bytearray) -> list:
        return [f'{byte:02x}' for byte in bytes_array]

    def read_hex(self, byte_length: int, hex_separator: str = ' ') -> str:
        return hex_separator.join(self.bytes_to_hex_representation(self.read_bytes(byte_length)))

    def read_int8(self) -> int:
        data = int.from_bytes(self.buffer_view[self.current_byte:self.current_byte + 1], byteorder='little', signed=True)
        self.current_byte += 1
        return data

    def read_uint8(self) -> int:
        data = int.from_bytes(self.buffer_view[self.current_byte:self.current_byte + 1], byteorder='little', signed=False)
        self.current_byte += 1
        return data

    def read_int16(self) -> int:
        data = int.from_bytes(self.buffer_view[self.current_byte:self.current_byte + 2], byteorder='little', signed=True)
        self.current_byte += 2
        return data

    def read_uint16(self) -> int:
        data = int.from_bytes(self.buffer_view[self.current_byte:self.current_byte + 2], byteorder='little', signed=False)
        self.current_byte += 2
        return data

    def read_int32(self) -> int:
        data = int.from_bytes(self.buffer_view[self.current_byte:self.current_byte + 4], byteorder='little', signed=True)
        self.current_byte += 4
        return data

    def read_uint32(self) -> int:
        data = int.from_bytes(self.buffer_view[self.current_byte:self.current_byte + 4], byteorder='little', signed=False)
        self.current_byte += 4
        return data

    def read_long(self) -> int:
        data = int.from_bytes(self.buffer_view[self.current_byte:self.current_byte + 8], byteorder='little', signed=True)
        self.current_byte += 8
        return data

    def read_int64(self) -> int:
        return self.read_long()

    def read_uint64(self) -> int:
        data = int.from_bytes(self.buffer_view[self.current_byte:self.current_byte + 8], byteorder='little', signed=False)
        self.current_byte += 8
        return data

    def read_float32(self) -> float:
        data = struct.unpack('<f', self.buffer_view[self.current_byte:self.current_byte + 4])[0]
        self.current_byte += 4
        return data

    def read_double(self) -> float:
        data = struct.unpack('<d', self.buffer_view[self.current_byte:self.current_byte + 8])[0]
        self.current_byte += 8
        return data

    def read_string(self) -> str:
        str_length = self.read_int32()
        start_bytes = self.current_byte

        if str_length == 0:
            return ''

        if str_length > (len(self.buffer_view) - self.current_byte):
            error_message = f'Cannot read string of length {str_length} at position {self.current_byte} as it exceeds the end at {len(self.buffer_view)}'
            raise ValueError(error_message)

        if str_length < 0:
            string = ''.join([chr(self.read_uint16()) for _ in range(-str_length - 1)])
            self.current_byte += 2
            return string

        try:
            string = ''.join([chr(self.read_uint8()) for _ in range(str_length - 1)])
            self.current_byte += 1
            return string
        except Exception as error:
            raise CorruptSaveError(f'Cannot read UTF8 string of length {str_length} at position {self.current_byte}.')

    def get_buffer_position(self) -> int:
        return self.current_byte

    def get_buffer_slice(self, begin: int, end: int) -> bytearray:
        return self.buffer_view[begin:end]

    def get_buffer_progress(self) -> float:
        return self.current_byte / len(self.buffer_view)

    def get_buffer_length(self) -> int:
        return len(self.buffer_view)

    def get_buffer(self) -> bytearray:
        return self.buffer_view
