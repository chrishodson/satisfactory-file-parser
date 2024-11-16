from .alignment_enum import Alignment

class BinaryOperable:
    def __init__(self, alignment: Alignment):
        self.alignment = alignment

    def get_buffer_position(self) -> int:
        raise NotImplementedError

    def get_buffer_length(self) -> int:
        raise NotImplementedError
