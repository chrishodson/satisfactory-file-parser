from ...byte.binary_readable_interface import BinaryReadable
from ...byte.byte_writer import ByteWriter

def is_conveyor_special_properties(obj: any) -> bool:
    return obj['type'] == 'ConveyorSpecialProperties'

class ConveyorSpecialProperties:
    def __init__(self):
        self.type = 'ConveyorSpecialProperties'

    @staticmethod
    def parse(reader: BinaryReadable) -> 'ConveyorSpecialProperties':
        reader.read_int32()  # 0
        return ConveyorSpecialProperties()

    @staticmethod
    def serialize(writer: ByteWriter, property: 'ConveyorSpecialProperties') -> None:
        writer.write_int32(0)
