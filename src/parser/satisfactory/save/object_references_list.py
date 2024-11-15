from ..types.structs.object_reference import ObjectReference

class ObjectReferencesList:

    @staticmethod
    def serialize_list(writer, collectables):
        writer.write_int32(len(collectables))
        for collectable in collectables:
            ObjectReference.write(writer, collectable)

    @staticmethod
    def read_list(reader):
        collected = []
        count = reader.read_int32()
        for _ in range(count):
            collected.append(ObjectReference.read(reader))
        return collected
