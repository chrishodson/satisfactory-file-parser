from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.error.parser_error import ParserError
from src.parser.satisfactory.types.property.generic.abstract_base_property import PropertiesMap
from src.parser.satisfactory.types.property.properties_list import PropertiesList
from src.parser.satisfactory.types.property.special.special_properties import SpecialProperties

class SaveObjectHeader:
    def __init__(self, type_path: str, root_object: str, instance_name: str):
        self.type_path = type_path
        self.root_object = root_object
        self.instance_name = instance_name

class SaveObject(SaveObjectHeader):
    def __init__(self, type_path: str, root_object: str, instance_name: str):
        super().__init__(type_path, root_object, instance_name)
        self.properties: PropertiesMap = {}
        self.special_properties: SpecialProperties.AvailableSpecialPropertiesTypes = {'type': 'EmptySpecialProperties'}
        self.trailing_data: list[int] = []
        self.object_version: int = 0
        self.unknown_type2: int = 0

    @staticmethod
    def parse_header(reader: BinaryReadable, obj: 'SaveObject') -> None:
        obj.type_path = reader.read_string()
        obj.root_object = reader.read_string()
        obj.instance_name = reader.read_string()

    @staticmethod
    def serialize_header(writer: ByteWriter, obj: 'SaveObject') -> None:
        writer.write_string(obj.type_path)
        writer.write_string(obj.root_object)
        writer.write_string(obj.instance_name)

    @staticmethod
    def parse_data(obj: 'SaveObject', length: int, reader: BinaryReadable, build_version: int, type_path: str) -> None:
        start = reader.get_buffer_position()
        obj.properties = PropertiesList.parse_list(reader, build_version)
        reader.read_int32()  # 0
        remaining_size = length - (reader.get_buffer_position() - start)
        obj.special_properties = SpecialProperties.parse_class_specific_special_properties(reader, type_path, remaining_size)
        remaining_size = length - (reader.get_buffer_position() - start)
        if remaining_size > 0:
            obj.trailing_data = list(reader.read_bytes(remaining_size))
        elif remaining_size < 0:
            raise ParserError('ParserError', f'Unexpected. Read more bytes than are indicated for entity {obj.instance_name}. bytes left to read is {remaining_size}')

    @staticmethod
    def serialize_data(writer: ByteWriter, obj: 'SaveObject', build_version: int) -> None:
        PropertiesList.serialize_list(obj.properties, writer, build_version)
        writer.write_int32(0)
        SpecialProperties.serialize_class_specific_special_properties(writer, obj.type_path, obj.special_properties)
        writer.write_bytes_array(obj.trailing_data)
