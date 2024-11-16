from ..byte.binary_readable_interface import BinaryReadable
from ..byte.byte_writer import ByteWriter

def is_empty_special_properties(obj: any) -> bool:
    return obj.type == 'EmptySpecialProperties'

class EmptySpecialProperties:
    def __init__(self):
        self.type = 'EmptySpecialProperties'

    @staticmethod
    def parse(reader: BinaryReadable) -> 'EmptySpecialProperties':
        return EmptySpecialProperties()

    @staticmethod
    def serialize(writer: ByteWriter, property: 'EmptySpecialProperties') -> None:
        pass
