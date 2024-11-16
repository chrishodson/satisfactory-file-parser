from src.parser.satisfactory.types.structs.guid_info import GUIDInfo
from src.parser.satisfactory.types.structs.soft_object_reference import SoftObjectReference
from .abstract_base_property import AbstractBaseProperty

def is_soft_object_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'SoftObjectProperty'

class SoftObjectProperty(AbstractBaseProperty):

    def __init__(self, value: SoftObjectReference, ue_type: str = 'SoftObjectProperty', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__('SoftObjectProperty', ue_type, guid_info, index)
        self.value = value

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int = 0) -> 'SoftObjectProperty':
        guid_info = GUIDInfo.read(reader)
        value = SoftObjectReference.read(reader)
        return SoftObjectProperty(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: BinaryReadable) -> SoftObjectReference:
        return SoftObjectReference.read(reader)

    @staticmethod
    def calc_overhead(property: 'SoftObjectProperty') -> int:
        return 1

    @staticmethod
    def serialize(writer: ByteWriter, property: 'SoftObjectProperty') -> None:
        GUIDInfo.write(writer, property.guid_info)
        SoftObjectReference.write(writer, property.value)

    @staticmethod
    def serialize_value(writer: ByteWriter, value: SoftObjectReference) -> None:
        SoftObjectReference.write(writer, value)
