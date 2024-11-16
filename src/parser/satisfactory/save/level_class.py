from ..byte.binary_readable_interface import BinaryReadable
from ..byte.byte_writer import ByteWriter
from ..error.parser_error import CorruptSaveError, UnimplementedError
from ..types.objects.save_component import SaveComponent, is_save_component
from ..types.objects.save_entity import SaveEntity, is_save_entity
from ..types.objects.save_object import SaveObject
from ..types.structs.object_reference import ObjectReference
from .object_references_list import ObjectReferencesList
from .save_reader import SaveReader

class Level:
    def __init__(self, name: str, objects: list, collectables: list):
        self.name = name
        self.objects = objects
        self.collectables = collectables

    @staticmethod
    def read_level(reader: SaveReader, level_name: str, build_version: int) -> 'Level':
        level = Level(level_name, [], [])

        headers_bin_len = reader.read_int32()
        reader.read_int32()

        pos_before_headers = reader.get_buffer_position()
        Level.read_all_object_headers(reader, level.objects)

        remaining_size = headers_bin_len - (reader.get_buffer_position() - pos_before_headers)
        if remaining_size > 0:
            doubled_collectables_ignored = ObjectReferencesList.read_list(reader)

        remaining_size = headers_bin_len - (reader.get_buffer_position() - pos_before_headers)
        if remaining_size != 0:
            print('remaining size not 0. Save may be corrupt.', remaining_size, level_name)

        object_contents_bin_len = reader.read_int32()
        reader.read_int32()

        pos_before_contents = reader.get_buffer_position()
        Level.read_all_object_contents(level_name, reader, level.objects, build_version, reader.on_progress_callback)
        pos_after_contents = reader.get_buffer_position()
        if pos_after_contents - pos_before_contents != object_contents_bin_len:
            print('save seems corrupt.', level.name)

        level.collectables = ObjectReferencesList.read_list(reader)

        return level

    @staticmethod
    def serialize_level(writer: ByteWriter, level: 'Level', build_version: int):
        len_indicator_header_and_destroyed_entities_size = writer.get_buffer_position()
        writer.write_int32(0)
        writer.write_int32(0)

        Level.serialize_all_object_headers(writer, level.objects)

        if level.collectables:
            ObjectReferencesList.serialize_list(writer, level.collectables)

        writer.write_binary_size_from_position(len_indicator_header_and_destroyed_entities_size, len_indicator_header_and_destroyed_entities_size + 8)

        Level.serialize_all_object_contents(writer, level.objects, build_version, level.name)

        ObjectReferencesList.serialize_list(writer, level.collectables)

    @staticmethod
    def read_all_object_contents(level_name: str, reader: BinaryReadable, objects_list: list, build_version: int, on_progress_callback: callable):
        count_entities = reader.read_int32()
        if count_entities != len(objects_list):
            raise ValueError(f"possibly corrupt. entity content count {count_entities} does not equal object count of {len(objects_list)}")

        batch_size = 10000
        read_objects_count = 0
        last_progress_report = 0
        while read_objects_count < count_entities:
            Level.read_n_object_contents(reader, min(batch_size, count_entities - read_objects_count), objects_list, read_objects_count, build_version)
            read_objects_count += min(batch_size, count_entities - read_objects_count)

            if read_objects_count - last_progress_report > batch_size:
                on_progress_callback(reader.get_buffer_progress(), f"read object count [{read_objects_count}/{count_entities}] in level {level_name}")
                last_progress_report = read_objects_count

    @staticmethod
    def read_n_object_contents(reader: BinaryReadable, count: int, objects: list, object_list_offset: int = 0, build_version: int = 0):
        for i in range(count):
            objects[i + object_list_offset].object_version = reader.read_int32()
            objects[i + object_list_offset].unknown_type2 = reader.read_int32()
            binary_size = reader.read_int32()

            before = reader.get_buffer_position()
            if is_save_entity(objects[i + object_list_offset]):
                SaveEntity.parse_data(objects[i + object_list_offset], binary_size, reader, build_version, objects[i + object_list_offset].type_path)
            elif is_save_component(objects[i + object_list_offset]):
                SaveComponent.parse_data(objects[i + object_list_offset], binary_size, reader, build_version, objects[i + object_list_offset].type_path)

            after = reader.get_buffer_position()
            if after - before != binary_size:
                raise CorruptSaveError(f"Could not read entity {objects[i + object_list_offset].instance_name}, as {after - before} bytes were read, but {binary_size} bytes were indicated.")

    @staticmethod
    def serialize_all_object_contents(writer: ByteWriter, objects: list, build_version: int, level_name: str):
        len_indicator_entities = writer.get_buffer_position()
        writer.write_int32(0)

        writer.write_int32(0)

        writer.write_int32(len(objects))
        for obj in objects:
            writer.write_int32(obj.object_version)
            writer.write_int32(obj.unknown_type2)
            len_replacement_position = writer.get_buffer_position()
            writer.write_int32(0)

            if is_save_entity(obj):
                SaveEntity.serialize_data(writer, obj, build_version)
            elif is_save_component(obj):
                SaveComponent.serialize_data(writer, obj, build_version)

            writer.write_binary_size_from_position(len_replacement_position, len_replacement_position + 4)
        writer.write_binary_size_from_position(len_indicator_entities, len_indicator_entities + 8)

    @staticmethod
    def read_all_object_headers(reader: BinaryReadable, objects_list: list):
        count_object_headers = reader.read_int32()

        batch_size = 10000
        read_object_headers_count = 0
        while read_object_headers_count < count_object_headers:
            objects_list.extend(Level.read_n_object_headers(reader, min(batch_size, count_object_headers - read_object_headers_count)))
            read_object_headers_count += min(batch_size, count_object_headers - read_object_headers_count)

    @staticmethod
    def read_n_object_headers(reader: BinaryReadable, count: int) -> list:
        objects = []
        for _ in range(count):
            object_type = reader.read_int32()
            if object_type == SaveEntity.TypeID:
                obj = SaveEntity('', '', '', '')
                SaveEntity.parse_header(reader, obj)
            elif object_type == SaveComponent.TypeID:
                obj = SaveComponent('', '', '', '')
                SaveComponent.parse_header(reader, obj)
            else:
                raise CorruptSaveError(f'Unknown object type {object_type}')
            objects.append(obj)
        return objects

    @staticmethod
    def serialize_all_object_headers(writer: ByteWriter, objects: list):
        writer.write_int32(len(objects))
        for obj in objects:
            if obj.type == 'SaveEntity':
                writer.write_int32(SaveEntity.TypeID)
                SaveEntity.serialize_header(writer, obj)
            elif obj.type == 'SaveComponent':
                writer.write_int32(SaveComponent.TypeID)
                SaveComponent.serialize_header(writer, obj)
            else:
                raise UnimplementedError(f"Unknown object type {obj.type}. Not implemented.")
