from ....byte.binary_readable import BinaryReadable
from ....byte.byte_writer import ByteWriter
from ....error.parser_error import UnimplementedError
from .bool_array_property import BoolArrayProperty, is_bool_array_property
from .byte_array_property import ByteArrayProperty, is_byte_array_property
from .double_array_property import DoubleArrayProperty, is_double_array_property
from .enum_array_property import EnumArrayProperty, is_enum_array_property
from .float_array_property import FloatArrayProperty, is_float_array_property
from .int32_array_property import Int32ArrayProperty, is_int32_array_property
from .int64_array_property import Int64ArrayProperty, is_int64_array_property
from .object_array_property import ObjectArrayProperty, is_object_array_property
from .soft_object_array_property import SoftObjectArrayProperty, is_soft_object_array_property
from .str_array_property import StrArrayProperty, is_str_array_property
from .struct_array_property import StructArrayProperty, is_struct_array_property
from .text_array_property import TextArrayProperty, is_text_array_property

def is_array_property(obj):
    return (
        is_bool_array_property(obj)
        or is_byte_array_property(obj)
        or is_double_array_property(obj)
        or is_enum_array_property(obj)
        or is_float_array_property(obj)
        or is_int32_array_property(obj)
        or is_int64_array_property(obj)
        or is_object_array_property(obj)
        or is_soft_object_array_property(obj)
        or is_str_array_property(obj)
        or is_struct_array_property(obj)
        or is_text_array_property(obj)
    )

class ArrayProperty:

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int, size: int):
        subtype = reader.read_string()
        reader.skip_bytes(1)  # 0

        property = None
        element_count = reader.read_int32()
        if subtype == "FloatProperty":
            property = FloatArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "BoolProperty":
            property = BoolArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "IntProperty":
            property = Int32ArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "Int64Property":
            property = Int64ArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "DoubleProperty":
            property = DoubleArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "ByteProperty":
            property = ByteArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "StrProperty":
            property = StrArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "EnumProperty":
            property = EnumArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "TextProperty":
            property = TextArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "InterfaceProperty" or subtype == "ObjectProperty":
            property = ObjectArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "SoftObjectProperty":
            property = SoftObjectArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        elif subtype == "StructProperty":
            property = StructArrayProperty.parse(reader, element_count, subtype, ue_type, index)
        else:
            raise UnimplementedError(f"Unknown array property subtype {subtype} for {ue_type}. Not implemented.")

        return property

    @staticmethod
    def calc_overhead(property):
        return len(property.subtype) + 5 + 1

    @staticmethod
    def serialize(writer: ByteWriter, property):
        writer.write_string(property.subtype)
        writer.write_byte(0)
        writer.write_int32(len(property.values))

        if is_float_array_property(property):
            FloatArrayProperty.serialize(writer, property)
        elif is_bool_array_property(property):
            BoolArrayProperty.serialize(writer, property)
        elif is_int32_array_property(property):
            Int32ArrayProperty.serialize(writer, property)
        elif is_int64_array_property(property):
            Int64ArrayProperty.serialize(writer, property)
        elif is_double_array_property(property):
            DoubleArrayProperty.serialize(writer, property)
        elif is_byte_array_property(property):
            ByteArrayProperty.serialize(writer, property)
        elif is_str_array_property(property):
            StrArrayProperty.serialize(writer, property)
        elif is_enum_array_property(property):
            EnumArrayProperty.serialize(writer, property)
        elif is_text_array_property(property):
            TextArrayProperty.serialize(writer, property)
        elif is_object_array_property(property):
            ObjectArrayProperty.serialize(writer, property)
        elif is_soft_object_array_property(property):
            SoftObjectArrayProperty.serialize(writer, property)
        elif is_struct_array_property(property):
            StructArrayProperty.serialize(writer, property)
        else:
            raise UnimplementedError(f"Unknown array property to serialize. {getattr(property, 'type', '')}, {getattr(property, 'subtype', '')}")
