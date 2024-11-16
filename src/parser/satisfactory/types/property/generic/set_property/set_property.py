from src.parser.byte.binary_readable_interface import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.error.parser_error import UnimplementedError
from .int32_set_property import Int32SetProperty, is_int32_set_property
from .object_set_property import ObjectSetProperty, is_object_set_property
from .str_set_property import StrSetProperty, is_str_set_property
from .struct_set_property import StructSetProperty, is_struct_set_property
from .uint32_set_property import Uint32SetProperty, is_uint32_set_property

def is_set_property(obj):
    return (
        is_uint32_set_property(obj)
        or is_int32_set_property(obj)
        or is_object_set_property(obj)
        or is_str_set_property(obj)
        or is_struct_set_property(obj)
    )

class SetProperty:

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int, property_name: str):
        subtype = reader.read_string()
        reader.skip_bytes(1)  # 0
        reader.skip_bytes(4)  # 0
        element_count = reader.read_int32()

        if subtype == "UInt32Property":
            return Uint32SetProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "IntProperty":
            return Int32SetProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "ObjectProperty":
            return ObjectSetProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "NameProperty":
            return StrSetProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "StructProperty":
            return StructSetProperty.parse(reader, element_count, subtype, ue_type, index, property_name)
        else:
            raise ValueError(f"Not Implemented SetProperty of {subtype}.")

    @staticmethod
    def calc_overhead(property):
        return len(property.subtype) + 5 + 1

    @staticmethod
    def serialize(writer: ByteWriter, property):
        writer.write_string(property.subtype)
        writer.write_byte(0)
        writer.write_int32(0)
        writer.write_int32(len(property.values))

        if is_int32_set_property(property):
            Int32SetProperty.serialize(writer, property)
        elif is_uint32_set_property(property):
            Uint32SetProperty.serialize(writer, property)
        elif is_object_set_property(property):
            ObjectSetProperty.serialize(writer, property)
        elif is_str_set_property(property):
            StrSetProperty.serialize(writer, property)
        elif is_struct_set_property(property):
            StructSetProperty.serialize(writer, property)
        else:
            raise UnimplementedError(f"Not Implemented Serializing SetProperty of {property.subtype}.")
