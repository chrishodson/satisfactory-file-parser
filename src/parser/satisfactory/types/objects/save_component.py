from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.satisfactory.types.objects.save_object import SaveObject, SaveObjectHeader

def is_save_component(obj):
    return obj.type == 'SaveComponent'

class SaveComponentHeader(SaveObjectHeader):
    def __init__(self, type_path, root_object, instance_name, parent_entity_name=''):
        super().__init__(type_path, root_object, instance_name)
        self.parent_entity_name = parent_entity_name

class SaveComponent(SaveObject, SaveComponentHeader):
    TypeID = 0

    def __init__(self, type_path, root_object, instance_name, parent_entity_name=''):
        SaveObject.__init__(self, type_path, root_object, instance_name)
        SaveComponentHeader.__init__(self, type_path, root_object, instance_name, parent_entity_name)
        self.type = 'SaveComponent'

    @staticmethod
    def parse_header(reader, obj):
        SaveObject.parse_header(reader, obj)
        obj.parent_entity_name = reader.read_string()

    @staticmethod
    def serialize_header(writer, component):
        SaveObject.serialize_header(writer, component)
        writer.write_string(component.parent_entity_name)

    @staticmethod
    def parse_data(component, length, reader, build_version, type_path):
        SaveObject.parse_data(component, length, reader, build_version, type_path)
