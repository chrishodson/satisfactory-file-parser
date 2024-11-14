from ..types.structs.ObjectReference import ObjectReference

class ObjectReferencesList:

    @staticmethod
    def SerializeList(writer, collectables):
        writer.writeInt32(len(collectables))
        for collectable in collectables:
            ObjectReference.write(writer, collectable)

    @staticmethod
    def ReadList(reader):
        collected = []
        count = reader.readInt32()
        for _ in range(count):
            collected.append(ObjectReference.read(reader))
        return collected
