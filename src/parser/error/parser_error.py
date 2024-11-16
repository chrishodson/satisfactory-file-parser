class ParserError(Exception):
    def __init__(self, name: str, message: str):
        super().__init__(message)
        self.name = name


class UnsupportedVersionError(ParserError):
    def __init__(self, message: str = 'This save version is not supported.'):
        super().__init__('UnsupportedVersionError', message)


class CorruptSaveError(ParserError):
    def __init__(self, message: str = 'This save data is most likely corrupt.'):
        super().__init__('CorruptSaveError', message)


class CompressionLibraryError(ParserError):
    def __init__(self, message: str = 'Failed to compress/decompress save data.'):
        super().__init__('CompressionLibraryError', message)


class TimeoutError(ParserError):
    def __init__(self, message: str = 'Operation timed out.'):
        super().__init__('TimeoutError', message)


class UnimplementedError(ParserError):
    def __init__(self, message: str = 'Unimplemented Operation.'):
        super().__init__('UnimplementedError', message)
