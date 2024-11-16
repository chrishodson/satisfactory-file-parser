from parser.satisfactory.types.structs.guid_info import GUIDInfo
from parser.satisfactory.types.structs.object_reference import ObjectReference
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty

def is_object_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'ObjectProperty'

class ObjectProperty(AbstractBaseProperty):

    def __init__(self, value: ObjectReference, ue_type: str = 'ObjectProperty', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__('ObjectProperty', ue_type, guid_info, index)
        self.value = value

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int = 0) -> 'ObjectProperty':
        guid_info = GUIDInfo.read(reader)
        value = ObjectProperty.read_value(reader)
        return ObjectProperty(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: BinaryReadable) -> ObjectReference:
        return ObjectReference.read(reader)

    @staticmethod
    def calc_overhead(property: 'ObjectProperty') -> int:
        return 1

    @staticmethod
    def serialize(writer: ByteWriter, property: 'ObjectProperty') -> None:
        GUIDInfo.write(writer, property.guid_info)
        ObjectProperty.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer: ByteWriter, value: ObjectReference) -> None:
        ObjectReference.write(writer, value)
