from parser.byte.binary_readable_interface import BinaryReadable
from parser.byte.byte_writer import ByteWriter
from parser.satisfactory.types.structs.dynamic_struct_property_value import DynamicStructPropertyValue
from parser.satisfactory.types.structs.object_reference import ObjectReference
from .abstract_base_property import AbstractBaseProperty
from .byte_property import ByteProperty
from .enum_property import EnumProperty
from .int32_property import Int32Property
from .int64_property import Int64Property
from .object_property import ObjectProperty
from .str_property import StrProperty
from .struct_property import GENERIC_STRUCT_PROPERTY_VALUE


MAP_STRUCT_KEY_PROXY = tuple[int, int, int, int, int, int, int, int, int, int, int, int]
GENERIC_MAP_KEY_TYPE = int | ObjectReference | bool | GENERIC_STRUCT_PROPERTY_VALUE | MAP_STRUCT_KEY_PROXY
GENERIC_MAP_VALUE_TYPE = int | ObjectReference | bool | GENERIC_STRUCT_PROPERTY_VALUE


class MapProperty(AbstractBaseProperty):

    def __init__(self, key_type: str, value_type: str, ue_type: str, index: int):
        super().__init__('MapProperty', ue_type, index)
        self.key_type = key_type
        self.value_type = value_type
        self.mode_type = 0
        self.mode_unk1 = None
        self.mode_unk2 = ''
        self.mode_unk3 = ''
        self.values: list[tuple[GENERIC_MAP_KEY_TYPE, GENERIC_MAP_VALUE_TYPE]] = []

    @staticmethod
    def parse(reader: BinaryReadable, property_name: str, build_version: int, size: int, ue_type: str = 'MapProperty', index: int = 0) -> 'MapProperty':
        start = reader.get_buffer_position()
        property = MapProperty(
            reader.read_string(), reader.read_string(), ue_type, index
        )

        unk = reader.read_byte()  # 0
        property.mode_type = reader.read_int32()  # 0

        element_count = reader.read_int32()
        for _ in range(element_count):
            if property.key_type == 'StructProperty':
                if property_name in ['mSaveData', 'mUnresolvedSaveData']:
                    key = tuple(reader.read_bytes(12))
                else:
                    key = DynamicStructPropertyValue.read(reader, 0, property.key_type)
            elif property.key_type == 'ObjectProperty':
                key = ObjectProperty.read_value(reader)
            elif property.key_type in ['StrProperty', 'NameProperty']:
                key = StrProperty.read_value(reader)
            elif property.key_type == 'EnumProperty':
                key = EnumProperty.read_value(reader)
            elif property.key_type in ['IntProperty', 'Int32Property']:
                key = Int32Property.read_value(reader)
            elif property.key_type == 'Int64Property':
                key = Int64Property.read_value(reader)
            elif property.key_type == 'ByteProperty':
                key = ByteProperty.read_value(reader)
            else:
                raise ValueError(f'not implemented map key type {property.key_type}')

            if property.value_type == 'StructProperty':
                value = DynamicStructPropertyValue.read(reader, 0, property.value_type)
            elif property.value_type == 'ObjectProperty':
                value = ObjectProperty.read_value(reader)
            elif property.value_type in ['StrProperty', 'NameProperty']:
                value = StrProperty.read_value(reader)
            elif property.value_type == 'EnumProperty':
                value = EnumProperty.read_value(reader)
            elif property.value_type in ['IntProperty', 'Int32Property']:
                value = Int32Property.read_value(reader)
            elif property.value_type == 'Int64Property':
                value = Int64Property.read_value(reader)
            elif property.value_type == 'ByteProperty':
                value = ByteProperty.read_value(reader)
            else:
                raise ValueError(f'not implemented map value type {property.value_type}')

            property.values.append((key, value))

        return property

    @staticmethod
    def calc_overhead(property: 'MapProperty') -> int:
        return len(property.key_type) + 5 + len(property.value_type) + 5 + 1

    @staticmethod
    def serialize(writer: ByteWriter, property: 'MapProperty') -> None:
        writer.write_string(property.key_type)
        writer.write_string(property.value_type)

        writer.write_byte(0)
        writer.write_int32(property.mode_type)

        writer.write_int32(len(property.values))
        for entry in property.values:
            if property.key_type == 'StructProperty':
                if property.name in ['mSaveData', 'mUnresolvedSaveData']:
                    writer.write_bytes_array(entry[0])
                else:
                    DynamicStructPropertyValue.write(writer, 0, entry[0])
            elif property.key_type == 'ObjectProperty':
                ObjectProperty.serialize_value(writer, entry[0])
            elif property.key_type in ['StrProperty', 'NameProperty']:
                StrProperty.serialize_value(writer, entry[0])
            elif property.key_type == 'EnumProperty':
                EnumProperty.serialize_value(writer, entry[0])
            elif property.key_type in ['IntProperty', 'Int32Property']:
                Int32Property.serialize_value(writer, entry[0])
            elif property.key_type == 'Int64Property':
                Int64Property.serialize_value(writer, entry[0])
            elif property.key_type == 'ByteProperty':
                ByteProperty.serialize_value(writer, entry[0])
            else:
                raise ValueError(f'not implemented map key type {property.value_type}')

            if property.value_type == 'StructProperty':
                DynamicStructPropertyValue.write(writer, 0, entry[1])
            elif property.value_type == 'ObjectProperty':
                ObjectProperty.serialize_value(writer, entry[1])
            elif property.value_type in ['StrProperty', 'NameProperty']:
                StrProperty.serialize_value(writer, entry[1])
            elif property.value_type == 'EnumProperty':
                EnumProperty.serialize_value(writer, entry[1])
            elif property.value_type in ['IntProperty', 'Int32Property']:
                Int32Property.serialize_value(writer, entry[1])
            elif property.value_type == 'Int64Property':
                Int64Property.serialize_value(writer, entry[1])
            elif property.value_type == 'ByteProperty':
                ByteProperty.serialize_value(writer, entry[1])
            else:
                raise ValueError(f'not implemented map value type {property.value_type}')
