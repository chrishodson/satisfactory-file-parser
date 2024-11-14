import zlib
from struct import unpack
from io import BytesIO

from src.parser.byte.alignment import Alignment
from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_reader import ByteReader
from src.parser.error.parser_error import CorruptSaveError, ParserError
from src.parser.file_types import ChunkCompressionInfo
from src.parser.satisfactory.save.level import Level
from src.parser.satisfactory.save.save_reader import DEFAULT_SATISFACTORY_CHUNK_HEADER_SIZE
from src.parser.satisfactory.types.objects.save_component import SaveComponent, is_save_component
from src.parser.satisfactory.types.objects.save_entity import SaveEntity, is_save_entity
from src.parser.satisfactory.types.objects.save_object import SaveObject
from src.parser.satisfactory.types.structs.col4 import col4
from src.parser.satisfactory.types.structs.object_reference import ObjectReference
from src.parser.satisfactory.types.structs.vec3 import vec3
from src.parser.satisfactory.blueprint.blueprint_types import BlueprintConfig, BlueprintHeader

class BlueprintReader(ByteReader):

    def __init__(self, bluePrintBuffer: bytes):
        super().__init__(bluePrintBuffer, Alignment.LITTLE_ENDIAN)
        self.compressionInfo = ChunkCompressionInfo(
            packageFileTag=0,
            maxUncompressedChunkContentSize=0,
            chunkHeaderSize=DEFAULT_SATISFACTORY_CHUNK_HEADER_SIZE
        )

    @staticmethod
    def read_header(reader: BinaryReadable) -> BlueprintHeader:
        always_two = reader.read_bytes(4)  # 02 00 00 00 - always
        object_version = reader.read_bytes(2 * 4)  # 24 00 00 00, 7F 3B 03 00 - varies over updates - in 1.0 it's 46 and 0x7A960500.
        dimensions = vec3.parse_int(reader)  # 04 00 00 00, 04 00 00 00, 04 00 00 00 - dimensions in foundation size

        # list of item costs.
        item_type_count = reader.read_int32()
        item_costs = [(ObjectReference.read(reader), reader.read_int32()) for _ in range(item_type_count)]

        # list of recipes
        recipe_count = reader.read_int32()
        recipe_refs = [ObjectReference.read(reader) for _ in range(recipe_count)]

        return BlueprintHeader(
            designerDimension=dimensions,
            recipeReferences=recipe_refs,
            itemCosts=item_costs
        )

    def inflate_chunks(self) -> dict:
        self.fileBuffer = self.fileBuffer[self.currentByte:]

        self.handledByte = 0
        self.currentByte = 0
        self.maxByte = len(self.fileBuffer)

        current_chunks = []
        total_uncompressed_body_size = 0

        while self.handledByte < self.maxByte:
            chunk_header = BytesIO(self.fileBuffer[:self.compressionInfo.chunkHeaderSize])
            self.currentByte = self.compressionInfo.chunkHeaderSize
            self.handledByte += self.compressionInfo.chunkHeaderSize

            if self.compressionInfo.packageFileTag <= 0:
                self.compressionInfo.packageFileTag = unpack('<I', chunk_header.read(4))[0]
            if self.compressionInfo.maxUncompressedChunkContentSize <= 0:
                self.compressionInfo.maxUncompressedChunkContentSize = unpack('<I', chunk_header.read(4))[0]

            chunk_compressed_length = unpack('<I', chunk_header.read(4))[0]
            chunk_uncompressed_length = unpack('<I', chunk_header.read(4))[0]
            total_uncompressed_body_size += chunk_uncompressed_length

            current_chunk_size = chunk_compressed_length
            current_chunk = self.fileBuffer[self.currentByte:self.currentByte + current_chunk_size]
            self.handledByte += current_chunk_size
            self.currentByte += current_chunk_size

            self.fileBuffer = self.fileBuffer[self.currentByte:]
            self.currentByte = 0

            try:
                current_inflated_chunk = zlib.decompress(current_chunk)
                current_chunks.append(current_inflated_chunk)
            except zlib.error as err:
                raise ParserError('ParserError', 'An error occurred while calling zlib decompress.' + str(err))

        new_chunk_length = sum(len(cc) for cc in current_chunks)
        big_whole_chunk = bytearray(new_chunk_length)
        current_length = 0
        for chunk in current_chunks:
            big_whole_chunk[current_length:current_length + len(chunk)] = chunk
            current_length += len(chunk)

        self.currentByte = 0
        self.maxByte = len(big_whole_chunk)
        self.bufferView = BytesIO(big_whole_chunk)

        return {
            'newChunkLength': new_chunk_length,
            'numChunks': len(current_chunks),
            'inflatedData': big_whole_chunk
        }

    @staticmethod
    def parse_objects(reader: ByteReader) -> list:
        total_body_rest_size = reader.read_int32()

        object_headers_binary_size = reader.read_int32()
        objects = []
        Level.read_all_object_headers(reader, objects)

        some_checksum_thing = reader.read_int32()

        BlueprintReader.read_blueprint_object_contents(reader, objects, 0)

        reader.get_buffer_position()

        return objects

    @staticmethod
    def read_blueprint_object_contents(reader: BinaryReadable, objects_list: list, build_version: int) -> None:
        count_entities = reader.read_int32()
        for i in range(count_entities):
            length = reader.read_int32()
            if length == 0:
                raise CorruptSaveError(f'check number is a wrong value ({length}). This normally indicates a corrupt entity or blueprint.')

            obj = objects_list[i]
            if is_save_entity(obj):
                SaveEntity.parse_data(obj, length, reader, build_version, obj.type_path)
            elif is_save_component(obj):
                SaveComponent.parse_data(obj, length, reader, build_version, obj.type_path)

class BlueprintConfigReader(ByteReader):

    def __init__(self, bluePrintConfigBuffer: bytes):
        super().__init__(bluePrintConfigBuffer, Alignment.LITTLE_ENDIAN)

    def parse(self) -> BlueprintConfig:
        return BlueprintConfigReader.parse_config(self)

    @staticmethod
    def parse_config(reader: BinaryReadable) -> BlueprintConfig:
        always_two = reader.read_int32()
        description = reader.read_string()
        icon_id = reader.read_int32()
        color = col4.parse_rgba(reader)

        config = BlueprintConfig(
            description=description,
            color=color,
            iconID=icon_id
        )

        if reader.get_buffer_position() < reader.get_buffer_length():
            config.referencedIconLibrary = reader.read_string()
            config.iconLibraryType = reader.read_string()

        return config
