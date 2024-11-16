from .binary_operable_interface import BinaryOperable

class BinaryWritable(BinaryOperable):

    def skip_bytes(self, count: int = 1) -> None:
        pass

    def jump_to(self, position: int) -> None:
        pass

    def write_byte(self, value: int) -> None:
        pass

    def write_bytes(self, bytes: bytearray) -> None:
        pass

    def write_bytes_array(self, bytes: list[int]) -> None:
        pass

    def write_int8(self, value: int) -> None:
        pass

    def write_uint8(self, value: int) -> None:
        pass

    def write_int16(self, value: int) -> None:
        pass

    def write_uint16(self, value: int) -> None:
        pass

    def write_int32(self, value: int) -> None:
        pass

    def write_uint32(self, value: int) -> None:
        pass

    def write_int64(self, value: int) -> None:
        pass

    def write_uint64(self, value: int) -> None:
        pass

    def write_float32(self, value: float) -> None:
        pass

    def write_double(self, value: float) -> None:
        pass

    def write_string(self, value: str) -> None:
        pass

    def get_buffer_progress(self) -> float:
        pass
