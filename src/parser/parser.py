from src.parser.error.parser_error import UnsupportedVersionError
from src.parser.file_types import ChunkSummary
from src.parser.satisfactory.blueprint.blueprint_reader import BlueprintConfigReader, BlueprintReader
from src.parser.satisfactory.blueprint.blueprint_writer import BlueprintConfigWriter, BlueprintWriter
from src.parser.satisfactory.blueprint.blueprint_types import Blueprint
from src.parser.satisfactory.save.satisfactory_save import SatisfactorySave
from src.parser.satisfactory.save.save_reader import SaveReader
from src.parser.satisfactory.save.save_writer import SaveWriter


class Parser:

    @staticmethod
    def parse_save(name: str, bytes: bytes, options: dict = None) -> SatisfactorySave:
        reader = SaveReader(bytes, options.get('onProgressCallback') if options else None)
        header = reader.read_header()
        save = SatisfactorySave(name, header)

        rough_save_version = SaveReader.get_rough_save_version(header.save_version, header.save_header_type)
        if rough_save_version == '<U6':
            raise UnsupportedVersionError('Game Version < U6 is not supported.')
        elif rough_save_version == 'U6/U7':
            raise UnsupportedVersionError('Game Version U6/U7 is not supported in this package version. Consider downgrading to the latest package version supporting it, which is 0.0.34')
        elif rough_save_version == 'U8':
            raise UnsupportedVersionError('Game Version U8 is not supported in this package version. Consider downgrading to the latest package version supporting it, which is 0.3.7')

        inflate_result = reader.inflate_chunks()
        save.compression_info = reader.compression_info

        if options and 'onDecompressedSaveBody' in options:
            options['onDecompressedSaveBody'](reader.get_buffer())

        save.grid_hash = reader.read_save_body_hash()
        save.grids = reader.read_grids()
        save.levels = reader.read_levels()

        return save

    @staticmethod
    def write_save(save: SatisfactorySave, on_header: callable, on_chunk: callable, options: dict = None) -> list:
        writer = SaveWriter()
        SaveWriter.write_header(writer, save.header)
        pos_after_header = writer.get_buffer_position()

        SaveWriter.write_save_body_hash(writer, save.grid_hash)
        SaveWriter.write_grids(writer, save.grids)
        SaveWriter.write_levels(writer, save, save.header.build_version)

        writer.end_writing()
        chunk_summary = writer.generate_chunks(save.compression_info, pos_after_header, options.get('onBinaryBeforeCompressing') if options else None, on_header, on_chunk)
        return chunk_summary

    @staticmethod
    def write_blueprint_files(blueprint: Blueprint, on_main_file_header: callable, on_main_file_chunk: callable, options: dict = None) -> dict:
        blueprint_writer = BlueprintWriter()
        BlueprintWriter.serialize_header(blueprint_writer, blueprint.header)
        save_body_pos = blueprint_writer.get_buffer_position()
        BlueprintWriter.serialize_objects(blueprint_writer, blueprint.objects)
        blueprint_writer.end_writing()
        main_file_chunk_summary = blueprint_writer.generate_chunks(
            blueprint.compression_info,
            save_body_pos,
            {
                'onBinaryBeforeCompressing': options.get('onMainFileBinaryBeforeCompressing') if options else None,
                'onHeader': on_main_file_header,
                'onChunk': on_main_file_chunk
            }
        )

        config_writer = BlueprintConfigWriter()
        BlueprintConfigWriter.serialize_config(config_writer, blueprint.config)
        config_file_binary = config_writer.end_writing()

        return {
            'mainFileChunkSummary': main_file_chunk_summary,
            'configFileBinary': config_file_binary
        }

    @staticmethod
    def parse_blueprint_files(name: str, blueprint_file: bytes, blueprint_config_file: bytes, options: dict = None) -> Blueprint:
        blueprint_config_reader = BlueprintConfigReader(blueprint_config_file)
        config = BlueprintConfigReader.parse_config(blueprint_config_reader)

        blueprint_reader = BlueprintReader(blueprint_file)
        header = BlueprintReader.read_header(blueprint_reader)
        inflate_result = blueprint_reader.inflate_chunks()

        if options and 'onDecompressedBlueprintBody' in options:
            options['onDecompressedBlueprintBody'](inflate_result['inflatedData'])

        blueprint_objects = BlueprintReader.parse_objects(blueprint_reader)
        blueprint = Blueprint(
            name=name,
            compression_info=blueprint_reader.compression_info,
            header=header,
            config=config,
            objects=blueprint_objects
        )
        return blueprint

    @staticmethod
    def json_stringify_modified(obj: any, indent: int = 0) -> str:
        def custom_serializer(key, value):
            if isinstance(value, int) and value.bit_length() > 63:
                return str(value)
            elif value == 0 and 1 / value < 0:
                return '-0'
            return value

        return json.dumps(obj, default=custom_serializer, indent=indent)
