from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from src.parser.satisfactory.types.property.generic.int32_property import Int32Property

def is_int32_set_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'IntSetProperty'

class Int32SetProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[int], ue_type: str = 'IntSetProperty', index: int = 0):
        super().__init__(type='IntSetProperty', ue_type=ue_type, index=index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader: BinaryReadable, element_count: int, subtype: str, ue_type: str, index: int = 0) -> 'Int32SetProperty':
        values = [Int32Property.read_value(reader) for _ in range(element_count)]
        return Int32SetProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer: ByteWriter, property: 'Int32SetProperty') -> None:
        for value in property.values:
            Int32Property.serialize_value(writer, value)
