from enum import Enum

class CompressionAlgorithmCode(Enum):
    ZLIB = 3

class ChunkCompressionInfo:
    def __init__(self, chunkHeaderSize: int, packageFileTag: int, maxUncompressedChunkContentSize: int, compressionAlgorithm: CompressionAlgorithmCode = None):
        self.compressionAlgorithm = compressionAlgorithm
        self.chunkHeaderSize = chunkHeaderSize
        self.packageFileTag = packageFileTag
        self.maxUncompressedChunkContentSize = maxUncompressedChunkContentSize

class ChunkSummary:
    def __init__(self, uncompressedSize: int, compressedSize: int):
        self.uncompressedSize = uncompressedSize
        self.compressedSize = compressedSize
