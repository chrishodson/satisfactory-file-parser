from parser.byte.binary_readable_interface import BinaryReadable
from parser.byte.byte_writer import ByteWriter
from parser.error.parser_error import ParserError
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty, PropertiesMap
from parser.satisfactory.types.property.generic.array_property.array_property import ArrayProperty
from parser.satisfactory.types.property.generic.bool_property import BoolProperty
from parser.satisfactory.types.property.generic.byte_property import ByteProperty
from parser.satisfactory.types.property.generic.double_property import DoubleProperty
from parser.satisfactory.types.property.generic.enum_property import EnumProperty
from parser.satisfactory.types.property.generic.float_property import FloatProperty
from parser.satisfactory.types.property.generic.int32_property import Int32Property
from parser.satisfactory.types.property.generic.int64_property import Int64Property
from parser.satisfactory.types.property.generic.int8_property import Int8Property
from parser.satisfactory.types.property.generic.map_property import MapProperty
from parser.satisfactory.types.property.generic.object_property import ObjectProperty
from parser.satisfactory.types.property.generic.set_property.set_property import SetProperty
from parser.satisfactory.types.property.generic.soft_object_property import SoftObjectProperty
from parser.satisfactory.types.property.generic.str_property import StrProperty
from parser.satisfactory.types.property.generic.struct_property import StructProperty
from parser.satisfactory.types.property.generic.text_property import TextProperty
from parser.satisfactory.types.property.generic.uint32_property import Uint32Property
from parser.satisfactory.types.property.generic.uint64_property import Uint64Property
from parser.satisfactory.types.property.generic.uint8_property import Uint8Property


class PropertiesList:

    @staticmethod
    def parse_list(reader: BinaryReadable, build_version: int) -> PropertiesMap:
        properties = PropertiesMap()
        property_name = reader.read_string()
        while property_name != 'None':
            parsed_property = PropertiesList.parse_single_property(reader, build_version, property_name)

            if property_name in properties:
                if not isinstance(properties[property_name], list):
                    properties[property_name] = [properties[property_name]]
                properties[property_name].append(parsed_property)
            else:
                properties[property_name] = parsed_property

            property_name = reader.read_string()

        return properties

    @staticmethod
    def serialize_list(properties: PropertiesMap, writer: ByteWriter, build_version: int) -> None:
        for property in [val for sublist in properties.values() for val in (sublist if isinstance(sublist, list) else [sublist])]:
            writer.write_string(property.name)
            PropertiesList.serialize_single_property(writer, property, build_version)
        writer.write_string('None')

    @staticmethod
    def parse_single_property(reader: BinaryReadable, build_version: int, property_name: str) -> AbstractBaseProperty:
        current_property = {}

        property_type = reader.read_string()
        binary_size = reader.read_int32()

        index = reader.read_int32()
        before = reader.get_buffer_position()

        overhead = 0
        if property_type == 'BoolProperty':
            current_property = BoolProperty.parse(reader, property_type, index)
            overhead = BoolProperty.calc_overhead(current_property)
        elif property_type == 'ByteProperty':
            current_property = ByteProperty.parse(reader, property_type, index)
            overhead = ByteProperty.calc_overhead(current_property)
        elif property_type == 'Int8Property':
            current_property = Int8Property.parse(reader, property_type, index)
            overhead = Int8Property.calc_overhead(current_property)
        elif property_type == 'UInt8Property':
            current_property = Uint8Property.parse(reader, property_type, index)
            overhead = Uint8Property.calc_overhead(current_property)
        elif property_type in ['IntProperty', 'Int32Property']:
            current_property = Int32Property.parse(reader, property_type, index)
            overhead = Int32Property.calc_overhead(current_property)
        elif property_type == 'UInt32Property':
            current_property = Uint32Property.parse(reader, property_type, index)
            overhead = Uint32Property.calc_overhead(current_property)
        elif property_type == 'Int64Property':
            current_property = Int64Property.parse(reader, property_type, index)
            overhead = Int64Property.calc_overhead(current_property)
        elif property_type == 'UInt64Property':
            current_property = Uint64Property.parse(reader, property_type, index)
        elif property_type in ['SingleProperty', 'FloatProperty']:
            current_property = FloatProperty.parse(reader, property_type, index)
            overhead = FloatProperty.calc_overhead(current_property)
        elif property_type == 'DoubleProperty':
            current_property = DoubleProperty.parse(reader, property_type, index)
            overhead = DoubleProperty.calc_overhead(current_property)
        elif property_type in ['StrProperty', 'NameProperty']:
            current_property = StrProperty.parse(reader, property_type, index)
            overhead = StrProperty.calc_overhead(current_property)
        elif property_type in ['ObjectProperty', 'InterfaceProperty']:
            current_property = ObjectProperty.parse(reader, property_type, index)
            overhead = ObjectProperty.calc_overhead(current_property)
        elif property_type == 'SoftObjectProperty':
            current_property = SoftObjectProperty.parse(reader, property_type, index)
            overhead = SoftObjectProperty.calc_overhead(current_property)
        elif property_type == 'EnumProperty':
            current_property = EnumProperty.parse(reader, property_type, index)
            overhead = EnumProperty.calc_overhead(current_property)
        elif property_type == 'StructProperty':
            current_property = StructProperty.parse(reader, property_type, index, binary_size)
            overhead = StructProperty.calc_overhead(current_property)
        elif property_type == 'ArrayProperty':
            current_property = ArrayProperty.parse(reader, property_type, index, binary_size)
            overhead = ArrayProperty.calc_overhead(current_property)
        elif property_type == 'MapProperty':
            current_property = MapProperty.parse(reader, property_name, build_version, binary_size)
            overhead = MapProperty.calc_overhead(current_property)
        elif property_type == 'TextProperty':
            current_property = TextProperty.parse(reader, property_type, index)
            overhead = TextProperty.calc_overhead(current_property)
        elif property_type == 'SetProperty':
            current_property = SetProperty.parse(reader, property_type, index, property_name)
            overhead = SetProperty.calc_overhead(current_property)
        else:
            raise ValueError(f"Unimplemented type {property_type}")

        current_property.name = property_name

        read_bytes = reader.get_buffer_position() - before - overhead
        if read_bytes != binary_size:
            raise ParserError('ParserError', f"possibly corrupt. Read {read_bytes} bytes for {property_type} {property_name}, but {binary_size} bytes were indicated.")

        return current_property

    @staticmethod
    def serialize_single_property(writer: ByteWriter, property: AbstractBaseProperty, build_version: int) -> None:
        writer.write_string(property.ue_type)

        len_indicator = writer.get_buffer_position()
        writer.write_int32(0)

        writer.write_int32(property.index or 0)

        start = writer.get_buffer_position()
        overhead = 0
        if property.ue_type == 'BoolProperty':
            overhead = BoolProperty.calc_overhead(property)
            BoolProperty.serialize(writer, property)
        elif property.ue_type == 'ByteProperty':
            overhead = ByteProperty.calc_overhead(property)
            ByteProperty.serialize(writer, property)
        elif property.ue_type == 'Int8Property':
            overhead = Int8Property.calc_overhead(property)
            Int8Property.serialize(writer, property)
        elif property.ue_type == 'UInt8Property':
            overhead = Uint8Property.calc_overhead(property)
            Uint8Property.serialize(writer, property)
        elif property.ue_type in ['IntProperty', 'Int32Property']:
            overhead = Int32Property.calc_overhead(property)
            Int32Property.serialize(writer, property)
        elif property.ue_type == 'UInt32Property':
            overhead = Uint32Property.calc_overhead(property)
            Uint32Property.serialize(writer, property)
        elif property.ue_type == 'Int64Property':
            overhead = Int64Property.calc_overhead(property)
            Int64Property.serialize(writer, property)
        elif property.ue_type == 'UInt64Property':
            overhead = Uint64Property.calc_overhead(property)
            Uint64Property.serialize(writer, property)
        elif property.ue_type in ['SingleProperty', 'FloatProperty']:
            overhead = FloatProperty.calc_overhead(property)
            FloatProperty.serialize(writer, property)
        elif property.ue_type == 'DoubleProperty':
            overhead = DoubleProperty.calc_overhead(property)
            DoubleProperty.serialize(writer, property)
        elif property.ue_type in ['StrProperty', 'NameProperty']:
            overhead = StrProperty.calc_overhead(property)
            StrProperty.serialize(writer, property)
        elif property.ue_type in ['ObjectProperty', 'InterfaceProperty']:
            overhead = ObjectProperty.calc_overhead(property)
            ObjectProperty.serialize(writer, property)
        elif property.ue_type == 'SoftObjectProperty':
            overhead = SoftObjectProperty.calc_overhead(property)
            SoftObjectProperty.serialize(writer, property)
        elif property.ue_type == 'EnumProperty':
            overhead = EnumProperty.calc_overhead(property)
            EnumProperty.serialize(writer, property)
        elif property.ue_type == 'StructProperty':
            overhead = StructProperty.calc_overhead(property)
            StructProperty.serialize(writer, property)
        elif property.ue_type == 'ArrayProperty':
            overhead = ArrayProperty.calc_overhead(property)
            ArrayProperty.serialize(writer, property)
        elif property.ue_type == 'MapProperty':
            overhead = MapProperty.calc_overhead(property)
            MapProperty.serialize(writer, property)
        elif property.ue_type == 'TextProperty':
            overhead = TextProperty.calc_overhead(property)
            TextProperty.serialize(writer, property)
        elif property.ue_type == 'SetProperty':
            overhead = SetProperty.calc_overhead(property)
            SetProperty.serialize(writer, property)
        else:
            raise ValueError(f"Unimplemented type {property.type}")

        writer.write_binary_size_from_position(len_indicator, start + overhead)
