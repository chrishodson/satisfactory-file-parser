from .binary_operable_interface import BinaryOperable

class BinaryReadable(BinaryOperable):

    def skip_bytes(self, count: int = 1) -> None:
        pass

    def read_bytes(self, count: int) -> bytearray:
        pass

    def read_byte(self) -> int:
        pass

    def read_hex(self, count: int) -> str:
        pass

    def read_int8(self) -> int:
        pass

    def read_uint8(self) -> int:
        pass

    def read_int16(self) -> int:
        pass

    def read_uint16(self) -> int:
        pass

    def read_int32(self) -> int:
        pass

    def read_uint32(self) -> int:
        pass

    def read_int64(self) -> int:
        pass

    def read_uint64(self) -> int:
        pass

    def read_float32(self) -> float:
        pass

    def read_double(self) -> float:
        pass

    def read_string(self) -> str:
        pass

    def get_buffer_progress(self) -> float:
        pass
