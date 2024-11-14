from enum import Enum

class Alignment(Enum):
    BIG_ENDIAN = 0
    LITTLE_ENDIAN = 1

class ByteWriter:
    def __init__(self, alignment: Alignment, buffer_size: int = 500):
        self.alignment = alignment
        self.buffer_array = bytearray(buffer_size)
        self.current_byte = 0

    def skip_bytes(self, count: int = 1) -> None:
        self.extend_buffer_if_needed(count)
        self.current_byte += count

    def jump_to(self, pos: int) -> None:
        count = pos - self.get_buffer_position()
        self.skip_bytes(count)

    def write_byte(self, value: int) -> None:
        self.extend_buffer_if_needed(1)
        self.buffer_array[self.current_byte] = value
        self.current_byte += 1

    def write_bytes_array(self, bytes_array: list[int]) -> None:
        self.write_bytes(bytearray(bytes_array))

    def write_bytes(self, bytes_array: bytearray) -> None:
        self.extend_buffer_if_needed(len(bytes_array))
        for byte in bytes_array:
            self.buffer_array[self.current_byte] = byte
            self.current_byte += 1

    def write_int8(self, value: int) -> None:
        self.extend_buffer_if_needed(1)
        self.buffer_array[self.current_byte] = value
        self.current_byte += 1

    def write_uint8(self, value: int) -> None:
        self.write_byte(value)

    def write_int16(self, value: int) -> None:
        self.extend_buffer_if_needed(2)
        self.buffer_array[self.current_byte:self.current_byte + 2] = value.to_bytes(2, byteorder=self.alignment.name.lower(), signed=True)
        self.current_byte += 2

    def write_uint16(self, value: int) -> None:
        self.extend_buffer_if_needed(2)
        self.buffer_array[self.current_byte:self.current_byte + 2] = value.to_bytes(2, byteorder=self.alignment.name.lower(), signed=False)
        self.current_byte += 2

    def write_int32(self, value: int) -> None:
        self.extend_buffer_if_needed(4)
        self.buffer_array[self.current_byte:self.current_byte + 4] = value.to_bytes(4, byteorder=self.alignment.name.lower(), signed=True)
        self.current_byte += 4

    def write_uint32(self, value: int) -> None:
        self.extend_buffer_if_needed(4)
        self.buffer_array[self.current_byte:self.current_byte + 4] = value.to_bytes(4, byteorder=self.alignment.name.lower(), signed=False)
        self.current_byte += 4

    def write_int64(self, value: int) -> None:
        self.extend_buffer_if_needed(8)
        self.buffer_array[self.current_byte:self.current_byte + 8] = value.to_bytes(8, byteorder=self.alignment.name.lower(), signed=True)
        self.current_byte += 8

    def write_uint64(self, value: int) -> None:
        self.extend_buffer_if_needed(8)
        self.buffer_array[self.current_byte:self.current_byte + 8] = value.to_bytes(8, byteorder=self.alignment.name.lower(), signed=False)
        self.current_byte += 8

    def write_float32(self, value: float) -> None:
        self.extend_buffer_if_needed(4)
        self.buffer_array[self.current_byte:self.current_byte + 4] = bytearray(struct.pack('<f' if self.alignment == Alignment.LITTLE_ENDIAN else '>f', value))
        self.current_byte += 4

    def write_double(self, value: float) -> None:
        self.extend_buffer_if_needed(8)
        self.buffer_array[self.current_byte:self.current_byte + 8] = bytearray(struct.pack('<d' if self.alignment == Alignment.LITTLE_ENDIAN else '>d', value))
        self.current_byte += 8

    def write_string(self, value: str) -> None:
        if len(value) == 0:
            self.write_int32(0)
            return

        if self.is_ascii_compatible(value):
            self.write_int32(len(value) + 1)
            for char in value:
                self.write_byte(ord(char))
            self.write_uint8(0)
        else:
            self.write_int32(-len(value) - 1)
            for char in value:
                self.write_uint16(ord(char))
            self.write_uint16(0)

    @staticmethod
    def is_ascii_compatible(value: str) -> bool:
        return all(ord(char) < 128 for char in value)

    def get_buffer_position(self) -> int:
        return self.current_byte

    def get_buffer_slice(self, start: int, end: int = None) -> bytearray:
        return self.buffer_array[start:end]

    def get_buffer_length(self) -> int:
        return len(self.buffer_array)

    def get_buffer_progress(self) -> float:
        return self.current_byte / len(self.buffer_array)

    def write_binary_size_from_position(self, len_indicator_pos: int, start: int) -> None:
        after = self.get_buffer_position()
        written_bytes = after - start
        self.jump_to(len_indicator_pos)
        self.write_int32(written_bytes)
        self.jump_to(after)

    def extend_buffer_if_needed(self, count_needed_bytes: int, factor: float = 1.5) -> None:
        if self.current_byte + count_needed_bytes > len(self.buffer_array):
            new_size = int(factor * len(self.buffer_array))
            self.buffer_array.extend(bytearray(new_size - len(self.buffer_array)))

    def truncate_buffer(self) -> None:
        self.buffer_array = self.buffer_array[:self.current_byte]

    def end_writing(self) -> bytearray:
        self.truncate_buffer()
        return self.buffer_array

    @staticmethod
    def to_int32(num: int) -> bytearray:
        return bytearray([
            (num & 0xff000000) >> 24,
            (num & 0x00ff0000) >> 16,
            (num & 0x0000ff00) >> 8,
            (num & 0x000000ff)
        ])

    @staticmethod
    def append_buffer(buffer1: bytearray, buffer2: bytearray) -> bytearray:
        return buffer1 + buffer2
