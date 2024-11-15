import zlib
from src.parser.byte.alignment import Alignment
from src.parser.byte.byte_reader import ByteReader
from src.parser.error.parser_error import CompressionLibraryError, CorruptSaveError, ParserError, UnsupportedVersionError
from src.parser.file_types import ChunkCompressionInfo
from src.parser.satisfactory.types.structs.md5_hash import MD5Hash
from src.parser.satisfactory.save.level import Level
from src.parser.satisfactory.save.save_types import RoughSaveVersion, SatisfactorySaveHeader

DEFAULT_SATISFACTORY_CHUNK_HEADER_SIZE = 49

class SaveReader(ByteReader):

    EPOCH_TICKS = 621355968000000000

    def __init__(self, file_buffer, on_progress_callback=lambda progress, msg: None):
        super().__init__(file_buffer, Alignment.LITTLE_ENDIAN)
        self.header = None
        self.compression_info = {
            "packageFileTag": 0,
            "maxUncompressedChunkContentSize": 0,
            "chunkHeaderSize": DEFAULT_SATISFACTORY_CHUNK_HEADER_SIZE
        }
        self.on_progress_callback = on_progress_callback

    def expect(self, value, expected):
        if value != expected:
            print(f"Read a value that's usually {expected}, but this time {value}. Meaning unclear. Raise an issue or contact me if you want.")

    def read_header(self):
        self.header = {
            "saveHeaderType": 0,
            "saveVersion": 0,
            "buildVersion": 0,
            "mapName": "DEFAULT",
            "mapOptions": "",
            "sessionName": "",
            "playDurationSeconds": 0,
            "saveDateTime": "0",
            "sessionVisibility": 0
        }

        self.header["saveHeaderType"] = self.read_int32()
        self.header["saveVersion"] = self.read_int32()
        self.header["buildVersion"] = self.read_int32()
        self.header["mapName"] = self.read_string()
        self.header["mapOptions"] = self.read_string()
        self.header["sessionName"] = self.read_string()
        self.header["playDurationSeconds"] = self.read_int32()
        raw_save_date_time_in_ticks = self.read_long()
        unix_milliseconds = (raw_save_date_time_in_ticks - SaveReader.EPOCH_TICKS) / 10000
        self.header["saveDateTime"] = str(unix_milliseconds)
        self.header["sessionVisibility"] = self.read_byte()

        if self.header["saveHeaderType"] >= 7:
            self.header["fEditorObjectVersion"] = self.read_int32()
        if self.header["saveHeaderType"] >= 8:
            self.header["rawModMetadataString"] = self.read_string()
            try:
                self.header["modMetadata"] = json.loads(self.header["rawModMetadataString"])
            except:
                pass
            self.header["isModdedSave"] = self.read_int32()

        if self.header["saveHeaderType"] >= 10:
            self.header["saveIdentifier"] = self.read_string()

        if self.header["saveHeaderType"] >= 11:
            self.header["partitionEnabledFlag"] = self.read_int32() == 1

        if self.header["saveHeaderType"] >= 12:
            self.header["consistencyHashBytes"] = MD5Hash.read(self)

        if self.header["saveHeaderType"] >= 13:
            self.header["creativeModeEnabled"] = self.read_int32() == 1

        if self.header["saveVersion"] >= 21:
            pass
        else:
            raise UnsupportedVersionError("The save version is too old to support encoding currently. Save in newer game version.")

        return self.header

    @staticmethod
    def get_rough_save_version(save_version, header_type_version):
        if save_version >= 46:
            return 'U1.0+'
        elif header_type_version >= 13:
            return 'U8'
        elif save_version >= 29:
            return 'U6/U7'
        else:
            return '<U6'

    def inflate_chunks(self):
        self.file_buffer = self.file_buffer[self.current_byte:]

        self.handled_byte = 0
        self.current_byte = 0
        self.max_byte = len(self.file_buffer)

        current_chunks = []
        total_uncompressed_body_size = 0

        while self.handled_byte < self.max_byte:
            chunk_header = memoryview(self.file_buffer[:self.compression_info["chunkHeaderSize"]])
            self.current_byte = self.compression_info["chunkHeaderSize"]
            self.handled_byte += self.compression_info["chunkHeaderSize"]

            if self.compression_info["packageFileTag"] <= 0:
                self.compression_info["packageFileTag"] = int.from_bytes(chunk_header[:4], byteorder='little' if self.alignment == Alignment.LITTLE_ENDIAN else 'big')
            if self.compression_info["maxUncompressedChunkContentSize"] <= 0:
                self.compression_info["maxUncompressedChunkContentSize"] = int.from_bytes(chunk_header[8:12], byteorder='little' if self.alignment == Alignment.LITTLE_ENDIAN else 'big')

            chunk_compressed_length = int.from_bytes(chunk_header[33:37], byteorder='little' if self.alignment == Alignment.LITTLE_ENDIAN else 'big')
            chunk_uncompressed_length = int.from_bytes(chunk_header[25:29], byteorder='little' if self.alignment == Alignment.LITTLE_ENDIAN else 'big')
            total_uncompressed_body_size += chunk_uncompressed_length

            current_chunk_size = chunk_compressed_length
            current_chunk = self.file_buffer[self.current_byte:self.current_byte + current_chunk_size]
            self.handled_byte += current_chunk_size
            self.current_byte += current_chunk_size

            self.file_buffer = self.file_buffer[self.current_byte:]
            self.current_byte = 0

            try:
                current_inflated_chunk = zlib.decompress(current_chunk)
                current_chunks.append(current_inflated_chunk)
            except zlib.error as err:
                raise CompressionLibraryError("Failed to inflate compressed save data. " + str(err))

        new_chunk_length = sum(len(cc) for cc in current_chunks)
        big_whole_chunk = bytearray(new_chunk_length)
        current_length = 0
        for chunk in current_chunks:
            big_whole_chunk[current_length:current_length + len(chunk)] = chunk
            current_length += len(chunk)

        self.current_byte = 0
        self.max_byte = len(big_whole_chunk)
        self.buffer_view = memoryview(big_whole_chunk)

        data_length = self.read_int32()
        if total_uncompressed_body_size != data_length + 8:
            raise CorruptSaveError(f"Possibly corrupt. Indicated size of total save body ({data_length + 8}) does not match the uncompressed real size of {total_uncompressed_body_size}.")

        return {
            "concatenatedChunkLength": new_chunk_length,
            "numChunks": len(current_chunks)
        }

    def read_save_body_hash(self):
        self.expect(self.read_int32(), 0)

        save_body_validation_version = self.read_int32()

        self.expect(self.read_string(), 'None')
        self.expect(self.read_int32(), 0)

        hash1 = list(self.read_bytes(4))

        self.expect(self.read_int32(), 1)
        self.expect(self.read_string(), 'None')

        hash2 = list(self.read_bytes(4))

        return {
            "version": save_body_validation_version,
            "hash1": hash1,
            "hash2": hash2
        }

    def read_grids(self):
        grids = {}

        def read_grid():
            grid_name = self.read_string()
            cell_size = self.read_int32()
            grid_hash = self.read_uint32()
            grids[grid_name] = {"children": {}, "cellSize": cell_size, "gridHash": grid_hash}

            children_count = self.read_uint32()
            for _ in range(children_count):
                level_instance_name = self.read_string()
                cell_bin_hex = self.read_uint32()
                grids[grid_name]["children"][level_instance_name] = cell_bin_hex

        read_grid()
        read_grid()
        read_grid()
        read_grid()
        read_grid()

        return grids

    def read_levels(self):
        if not self.header:
            raise ParserError('ParserError', 'Header must be set before objects can be read.')

        rough_save_version = SaveReader.get_rough_save_version(self.header["saveVersion"], self.header["saveHeaderType"])
        if rough_save_version == '<U6':
            raise UnsupportedVersionError('Game Version < U6 is not supported.')
        elif rough_save_version == 'U6/U7':
            raise UnsupportedVersionError('Game Version U6/U7 is not supported in this package version. Consider downgrading to the latest package version supporting it, which is 0.0.34')
        elif rough_save_version == 'U8':
            raise UnsupportedVersionError('Game Version U8 is not supported in this package version. Consider downgrading to the latest package version supporting it, which is 0.3.7')

        levels = []
        level_count = self.read_int32()
        self.on_progress_callback(self.get_buffer_progress(), f"reading pack of {level_count + 1} levels.")

        for i in range(level_count + 1):
            level_single_name = self.header["mapName"] if i == level_count else self.read_string()
            if i % 500 == 0:
                self.on_progress_callback(self.get_buffer_progress(), f"reading level [{i + 1}/{level_count + 1}] {level_single_name}")

            levels.append(Level.read_level(self, level_single_name, self.header["buildVersion"]))

        self.on_progress_callback(self.get_buffer_progress(), 'finished parsing.')

        return levels
