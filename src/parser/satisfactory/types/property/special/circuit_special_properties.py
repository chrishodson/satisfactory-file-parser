from src.parser.byte.binary_readable_interface import BinaryReadable
from src.parser.byte.binary_writable_interface import ByteWriter
from src.parser.satisfactory.types.structs.object_reference import ObjectReference

class CircuitSpecialProperties:
    def __init__(self, circuits: list):
        self.type = 'CircuitSpecialProperties'
        self.circuits = circuits

    @staticmethod
    def parse(reader: BinaryReadable) -> 'CircuitSpecialProperties':
        count = reader.read_int32()
        circuits = []
        for _ in range(count):
            circuits.append({
                'id': reader.read_int32(),
                'object_reference': ObjectReference.read(reader)
            })
        return CircuitSpecialProperties(circuits)

    @staticmethod
    def serialize(writer: ByteWriter, property: 'CircuitSpecialProperties') -> None:
        writer.write_int32(len(property.circuits))
        for circuit in property.circuits:
            writer.write_int32(circuit['id'])
            ObjectReference.write(writer, circuit['object_reference'])
