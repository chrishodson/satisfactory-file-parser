from ...file import ChunkCompressionInfo
from .level import Level
from .save_reader import Grids, SaveBodyValidation
from .save_types import SatisfactorySaveHeader

class SatisfactorySave:
    def __init__(self, name: str, header: SatisfactorySaveHeader):
        self.name = name
        self.header = header
        self.gridHash: SaveBodyValidation = SaveBodyValidation(version=6, hash1=[0, 0, 0, 0], hash2=[0, 0, 0, 0])
        self.grids: Grids = {}
        self.levels: list[Level] = []
        self.compressionInfo: ChunkCompressionInfo = None
