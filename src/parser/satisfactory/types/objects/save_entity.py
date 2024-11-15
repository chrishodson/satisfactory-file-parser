from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.satisfactory.types.structs.object_reference import ObjectReference
from src.parser.satisfactory.types.structs.transform import Transform
from src.parser.satisfactory.types.objects.save_object import SaveObject

def is_save_entity(obj):
    return obj.type == 'SaveEntity'

class SaveEntity(SaveObject):
    TypeID = 1

    def __init__(self, type_path, root_object, instance_name, parent_entity_name='', needs_transform=False):
        super().__init__(type_path, root_object, instance_name)
        self.type = 'SaveEntity'
        self.need_transform = needs_transform
        self.was_placed_in_level = False
        self.parent_object_root = ''
        self.parent_object_name = ''
        self.transform = {
            'rotation': {'x': 0, 'y': 0, 'z': 0, 'w': 1},
            'translation': {'x': 0, 'y': 0, 'z': 0},
            'scale3d': {'x': 1, 'y': 1, 'z': 1}
        }
        self.components = []

    @staticmethod
    def parse_header(reader, obj):
        SaveObject.parse_header(reader, obj)
        obj.need_transform = reader.read_int32() == 1
        obj.transform = Transform.parse_f(reader)
        obj.was_placed_in_level = reader.read_int32() == 1

    @staticmethod
    def parse_data(entity, length, reader, build_version, type_path):
        start = reader.get_buffer_position()

        entity.parent_object_root = reader.read_string()
        entity.parent_object_name = reader.read_string()

        component_count = reader.read_int32()
        for _ in range(component_count):
            component_ref = ObjectReference.read(reader)
            entity.components.append(component_ref)

        remaining_size = length - (reader.get_buffer_position() - start)
        return SaveObject.parse_data(entity, remaining_size, reader, build_version, type_path)

    @staticmethod
    def serialize_header(writer, entity):
        SaveObject.serialize_header(writer, entity)

        writer.write_int32(1 if entity.need_transform else 0)
        Transform.serialize_f(writer, entity.transform)
        writer.write_int32(1 if entity.was_placed_in_level else 0)

    @staticmethod
    def serialize_data(writer, entity, build_version):
        writer.write_string(entity.parent_object_root)
        writer.write_string(entity.parent_object_name)

        writer.write_int32(len(entity.components))
        for component in entity.components:
            writer.write_string(component.level_name)
            writer.write_string(component.path_name)

        SaveObject.serialize_data(writer, entity, build_version)
