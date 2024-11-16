from parser.byte.binary_readable_interface import BinaryReadable
from parser.byte.byte_writer import ByteWriter
from parser.satisfactory.types.structs.guid_info import GUIDInfo
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from parser.satisfactory.types.property.generic.struct_property import StructProperty

def is_struct_array_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'StructArrayProperty'

class StructArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[StructProperty], struct_value_fields: 'ArrayPropertyStructValueFields', ue_type: str = 'StructArrayProperty', index: int = 0):
        super().__init__('StructArrayProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values
        self.struct_value_fields = struct_value_fields

    @staticmethod
    def parse(reader: BinaryReadable, element_count: int, subtype: str, ue_type: str, index: int = 0) -> 'StructArrayProperty':
        name = reader.read_string()
        all_ue_type = reader.read_string()
        binary_size = reader.read_int32()
        all_index = reader.read_int32()
        all_struct_type = reader.read_string()
        all_guid = GUIDInfo.read(reader)
        all_unk1 = reader.read_int32()
        all_unk2 = reader.read_int32()
        all_unk3 = reader.read_int32()
        all_unk4 = reader.read_int32()

        struct_value_fields = ArrayPropertyStructValueFields(all_struct_type, all_index if all_index > 0 else None, all_guid)
        if all_unk1 != 0:
            struct_value_fields.all_unk1 = all_unk1
        if all_unk2 != 0:
            struct_value_fields.all_unk2 = all_unk2
        if all_unk3 != 0:
            struct_value_fields.all_unk3 = all_unk3
        if all_unk4 != 0:
            struct_value_fields.all_unk4 = all_unk4

        before = reader.get_buffer_position()
        values = [StructProperty(all_struct_type, all_ue_type, all_index, all_guid) for _ in range(element_count)]
        for struct in values:
            struct.value = StructProperty.parse_value(reader, all_struct_type, binary_size)
        read_bytes = reader.get_buffer_position() - before
        if read_bytes != binary_size:
            raise ValueError('possibly corrupt in array of struct.')

        return StructArrayProperty(subtype, values, struct_value_fields, ue_type, index)

    @staticmethod
    def serialize(writer: ByteWriter, property: 'StructArrayProperty') -> None:
        writer.write_string(property.name)
        writer.write_string(property.subtype)
        len_indicator = writer.get_buffer_position()
        writer.write_int32(0)
        writer.write_int32(property.struct_value_fields.all_index or 0)
        writer.write_string(property.struct_value_fields.all_struct_type)
        GUIDInfo.write(writer, property.struct_value_fields.all_guid)
        writer.write_int32(property.struct_value_fields.all_unk1 or 0)
        writer.write_int32(property.struct_value_fields.all_unk2 or 0)
        writer.write_int32(property.struct_value_fields.all_unk3 or 0)
        writer.write_int32(property.struct_value_fields.all_unk4 or 0)
        before = writer.get_buffer_position()
        for v in property.values:
            StructProperty.serialize_value(writer, property.struct_value_fields.all_struct_type, v.value)
        writer.write_binary_size_from_position(len_indicator, before)

class ArrayPropertyStructValueFields:
    def __init__(self, all_struct_type: str, all_index: int = None, all_guid: GUIDInfo = None, all_unk1: int = 0, all_unk2: int = 0, all_unk3: int = 0, all_unk4: int = 0):
        self.all_struct_type = all_struct_type
        self.all_index = all_index
        self.all_guid = all_guid
        self.all_unk1 = all_unk1
        self.all_unk2 = all_unk2
        self.all_unk3 = all_unk3
        self.all_unk4 = all_unk4
