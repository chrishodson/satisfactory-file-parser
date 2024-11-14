from src.parser.byte.alignment import Alignment
from src.parser.byte.byte_writer import ByteWriter
from src.parser.error.parser_error import ParserError
from src.parser.file.types import ChunkCompressionInfo, ChunkSummary
from src.parser.satisfactory.save.level import Level
from src.parser.satisfactory.save.save_writer import SaveWriter
from src.parser.satisfactory.types.objects.save_component import SaveComponent, isSaveComponent
from src.parser.satisfactory.types.objects.save_entity import SaveEntity, isSaveEntity
from src.parser.satisfactory.types.structs.col4 import col4
from src.parser.satisfactory.types.structs.object_reference import ObjectReference
from src.parser.satisfactory.blueprint.blueprint_types import BlueprintConfig, BlueprintHeader


class BlueprintWriter(ByteWriter):

    def __init__(self):
        super().__init__(Alignment.LITTLE_ENDIAN)

    @staticmethod
    def serialize_header(writer: ByteWriter, header: BlueprintHeader) -> None:
        writer.write_int32(2)  # 2
        writer.write_int32(46)  # TODO - changes with game updates. object version. - 46 in 1.0
        writer.write_int32(366202)  # TODO - some header build version? changes with game updates.   // 0xECCF0300 // 0xE6060400 //0x7A960500 in 1.0

        dimensions = [
            header.designer_dimension.x if header.designer_dimension else 4,
            header.designer_dimension.y if header.designer_dimension else 4,
            header.designer_dimension.z if header.designer_dimension else 4,
        ]
        dimensions = [dim if dim >= 4 else 4 for dim in dimensions]  # don't let smaller values than 4 slip through.

        # designer dimensions in foundations.
        writer.write_int32(dimensions[0])
        writer.write_int32(dimensions[1])
        writer.write_int32(dimensions[2])

        # list of item costs.
        writer.write_int32(len(header.item_costs))
        for item_cost in header.item_costs:
            ObjectReference.write(writer, item_cost[0])
            writer.write_int32(item_cost[1])

        # list of recipes.
        writer.write_int32(len(header.recipe_references))
        for recipe_reference in header.recipe_references:
            ObjectReference.write(writer, recipe_reference)

    def generate_chunks(
        self,
        compression_info: ChunkCompressionInfo,
        pos_after_header: int,
        options: dict = None
    ) -> list[ChunkSummary]:

        if pos_after_header <= 0:
            raise ParserError('ParserError', 'seems like this buffer has no header. Please write the header first before you can generate chunks.')

        # send plain header first.
        header = self.buffer_array[:pos_after_header]
        if options and 'on_header' in options:
            options['on_header'](header)

        # create save body
        self.buffer_array = self.buffer_array[pos_after_header:]
        chunk_summary = SaveWriter.generate_compressed_chunks_from_data(
            self.buffer_array, compression_info,
            options.get('on_binary_before_compressing', lambda x: None),
            options.get('on_chunk', lambda x: None),
            self.alignment
        )
        return chunk_summary

    @staticmethod
    def serialize_objects(writer: ByteWriter, objects: list) -> None:
        # object headers
        headers_len_indicator = writer.get_buffer_position()
        writer.write_int32(0)
        Level.serialize_all_object_headers(writer, objects)
        writer.write_binary_size_from_position(headers_len_indicator, headers_len_indicator + 4)

        # objects contents
        BlueprintWriter.serialize_object_contents(writer, objects, 0, '')

    @staticmethod
    def serialize_object_contents(writer: ByteWriter, objects: list, build_version: int, level_name: str) -> None:
        len_indicator_entities = writer.get_buffer_position()
        writer.write_int32(0)

        writer.write_int32(len(objects))
        for obj in objects:
            len_replacement_position = writer.get_buffer_position()
            writer.write_int32(0)

            if isSaveEntity(obj):
                SaveEntity.serialize_data(writer, obj, build_version)
            elif isSaveComponent(obj):
                SaveComponent.serialize_data(writer, obj, build_version)

            writer.write_binary_size_from_position(len_replacement_position, len_replacement_position + 4)
        writer.write_binary_size_from_position(len_indicator_entities, len_indicator_entities + 4)


class BlueprintConfigWriter(ByteWriter):

    def __init__(self):
        super().__init__(Alignment.LITTLE_ENDIAN)

    @staticmethod
    def serialize_config(writer: ByteWriter, config: BlueprintConfig) -> None:
        writer.write_int32(2)  # unknown, seems to always be 02.
        writer.write_string(config.description)
        writer.write_int32(config.icon_id)
        col4.serialize_rgba(writer, config.color)
        writer.write_string(config.referenced_icon_library or '')
        writer.write_string(config.icon_library_type or '')
