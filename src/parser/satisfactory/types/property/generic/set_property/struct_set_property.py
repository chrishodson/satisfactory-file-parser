from src.parser.byte.binary_readable_interface import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.error.parser_error import UnimplementedError
from src.parser.satisfactory.types.structs.GUID import GUID
from src.parser.satisfactory.types.structs.vec3 import vec3
from src.parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty

def is_struct_set_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'StructSetProperty'

class StructSetProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list, ueType: str = 'StructSetProperty', index: int = 0):
        super().__init__(type='StructSetProperty', ueType=ueType, guidInfo=None, index=index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def Parse(reader: BinaryReadable, elementCount: int, subtype: str, ueType: str, index: int = 0, propertyName: str = '') -> 'StructSetProperty':
        values = []
        if propertyName == 'mRemovalLocations':
            values = [vec3.ParseF(reader) for _ in range(elementCount)]
        elif propertyName in ['mDestroyedPickups', 'mLootedDropPods']:
            values = [GUID.read(reader) for _ in range(elementCount)]
        else:
            raise UnimplementedError(f'Not Implemented SetProperty of StructProperty for property type {propertyName}.')

        return StructSetProperty(subtype=subtype, values=values, ueType=ueType, index=index)

    @staticmethod
    def Serialize(writer: ByteWriter, property: 'StructSetProperty') -> None:
        if property.name == 'mRemovalLocations':
            print('serializing mRemovalLocations, this is still under investigation.')
            for value in property.values:
                vec3.SerializeF(writer, value)
        elif property.name in ['mDestroyedPickups', 'mLootedDropPods']:
            for value in property.values:
                GUID.write(writer, value)
        else:
            raise UnimplementedError(f'Not Implemented serializing SetProperty of StructProperty for property {property.name}.')
