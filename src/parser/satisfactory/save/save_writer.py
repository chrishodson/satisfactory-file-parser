import zlib
from parser.byte.alignment import Alignment
from parser.byte.byte_writer import ByteWriter
from parser.error.parser_error import CompressionLibraryError, ParserError, UnsupportedVersionError
from parser.file.types import ChunkCompressionInfo, ChunkSummary, CompressionAlgorithmCode
from parser.satisfactory.types.structs.md5_hash import MD5Hash
from parser.satisfactory.save.level import Level
from parser.satisfactory.save.satisfactory_save import SatisfactorySave
from parser.satisfactory.save.save_reader import Grids, SaveBodyValidation, SaveReader
from parser.satisfactory.save.save_types import SatisfactorySaveHeader


class SaveWriter(ByteWriter):

    def __init__(self):
        super().__init__(Alignment.LITTLE_ENDIAN)

    @staticmethod
    def write_header(writer: ByteWriter, header: SatisfactorySaveHeader) -> None:
        writer.write_int32(header.save_header_type)
        writer.write_int32(header.save_version)
        writer.write_int32(header.build_version)
        writer.write_string(header.map_name)
        writer.write_string(header.map_options)
        writer.write_string(header.session_name)
        writer.write_int32(header.play_duration_seconds)
        writer.write_int64(int(header.save_date_time) * 10000 + SaveReader.EPOCH_TICKS)
        writer.write_byte(header.session_visibility)

        if header.save_header_type >= 7:
            writer.write_int32(header.f_editor_object_version)
        if header.save_header_type >= 8:
            if header.mod_metadata:
                writer.write_string(json.dumps(header.mod_metadata))
            else:
                writer.write_string(header.raw_mod_metadata_string)
            writer.write_int32(header.is_modded_save)
        if header.save_header_type >= 10:
            writer.write_string(header.save_identifier)

        # U8 jumped directly to 13.
        if header.save_header_type >= 11:
            writer.write_int32(1 if header.partition_enabled_flag else 0)

        if header.save_header_type >= 12:
            MD5Hash.write(writer, header.consistency_hash_bytes)

        # 13 is U8 Experimental First Release
        if header.save_header_type >= 13:
            writer.write_int32(1 if header.creative_mode_enabled else 0)

        if header.save_version >= 21:
            # ready to write levels now.
            pass
        else:
            raise UnsupportedVersionError("The save version is too old to be supported currently.")

    @staticmethod
    def write_save_body_hash(writer: ByteWriter, save_body_validation: SaveBodyValidation) -> None:
        writer.write_int32(0)
        writer.write_int32(save_body_validation.version)
        writer.write_string('None')
        writer.write_int32(0)
        writer.write_bytes_array(save_body_validation.hash1)
        writer.write_int32(1)
        writer.write_string('None')
        writer.write_bytes_array(save_body_validation.hash2)

    @staticmethod
    def write_grids(writer: ByteWriter, grids: Grids) -> None:
        for grid_name, grid_data in grids.items():
            writer.write_string(grid_name)
            writer.write_int32(grid_data['cell_size'])
            writer.write_uint32(grid_data['grid_hash'])

            writer.write_uint32(len(grid_data['children']))
            for child_name, child_data in grid_data['children'].items():
                writer.write_string(child_name)
                writer.write_uint32(child_data)

    @staticmethod
    def write_levels(writer: ByteWriter, save: SatisfactorySave, build_version: int) -> None:
        writer.write_int32(len(save.levels) - 1)
        for level in save.levels:
            if level.name != save.header.map_name:
                writer.write_string(level.name)
            Level.serialize_level(writer, level, build_version)

    @staticmethod
    def generate_compressed_chunks_from_data(
        buffer_array: bytearray,
        compression_info: ChunkCompressionInfo,
        on_binary_before_compressing: callable,
        on_chunk: callable,
        alignment: Alignment = Alignment.LITTLE_ENDIAN
    ) -> list[ChunkSummary]:

        total_uncompressed_size = len(buffer_array)

        save_body = bytearray(total_uncompressed_size + 8)
        save_body[4:] = buffer_array
        save_body_view = memoryview(save_body)
        save_body_view[:4] = total_uncompressed_size.to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
        on_binary_before_compressing(save_body)

        handled_byte = 0
        chunk_summary = []
        while handled_byte < len(save_body):
            uncompressed_content_size = min(compression_info.max_uncompressed_chunk_content_size, len(save_body) - handled_byte)
            uncompressed_chunk = save_body[handled_byte:handled_byte + uncompressed_content_size]

            try:
                compressed_chunk = zlib.compress(uncompressed_chunk)
            except zlib.error as err:
                raise CompressionLibraryError("Could not compress save data. " + str(err))

            chunk = bytearray(compression_info.chunk_header_size + len(compressed_chunk))
            chunk[compression_info.chunk_header_size:] = compressed_chunk

            view = memoryview(chunk)
            view[:4] = compression_info.package_file_tag.to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[4:8] = (0x22222222).to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[8:12] = compression_info.max_uncompressed_chunk_content_size.to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[12:16] = (0).to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[16] = CompressionAlgorithmCode.ZLIB
            view[17:21] = len(compressed_chunk).to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[21:25] = (0).to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[25:29] = uncompressed_content_size.to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[29:33] = (0).to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[33:37] = len(compressed_chunk).to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[37:41] = (0).to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[41:45] = uncompressed_content_size.to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')
            view[45:49] = (0).to_bytes(4, byteorder='little' if alignment == Alignment.LITTLE_ENDIAN else 'big')

            on_chunk(chunk)
            chunk_summary.append({
                'uncompressed_size': uncompressed_content_size + compression_info.chunk_header_size,
                'compressed_size': len(compressed_chunk) + compression_info.chunk_header_size
            })
            handled_byte += uncompressed_content_size

        return chunk_summary

    def generate_chunks(
        self,
        compression_info: ChunkCompressionInfo,
        pos_after_header: int,
        on_binary_before_compressing: callable,
        on_header: callable,
        on_chunk: callable
    ) -> list[ChunkSummary]:

        if pos_after_header <= 0:
            raise ParserError('ParserError', 'Seems like this buffer has no header. Please write the header first before you can generate chunks.')

        header = self.buffer_array[:pos_after_header]
        on_header(header)

        self.buffer_array = self.buffer_array[pos_after_header:]
        chunk_summary = SaveWriter.generate_compressed_chunks_from_data(self.buffer_array, compression_info, on_binary_before_compressing, on_chunk, self.alignment)

        return chunk_summary
