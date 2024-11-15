from src.parser.file.file_types import ChunkCompressionInfo
from src.parser.satisfactory.save.level import Level
from src.parser.satisfactory.save.save_reader import Grids, SaveBodyValidation
from src.parser.satisfactory.save.save_types import SatisfactorySaveHeader

class SatisfactorySave:
    def __init__(self, name: str, header: SatisfactorySaveHeader):
        self.name = name
        self.header = header
        self.gridHash: SaveBodyValidation = SaveBodyValidation(version=6, hash1=[0, 0, 0, 0], hash2=[0, 0, 0, 0])
        self.grids: Grids = {}
        self.levels: list[Level] = []
        self.compressionInfo: ChunkCompressionInfo = None
