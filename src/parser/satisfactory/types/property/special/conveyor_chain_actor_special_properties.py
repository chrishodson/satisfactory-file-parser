from ....byte.binary_readable_interface import BinaryReadable
from ....byte.byte_writer_class import ByteWriter
from ..structs.object_reference import ObjectReference
from ..structs.vec3 import vec3


def is_conveyor_chain_actor_special_properties(obj: any) -> bool:
    return obj.type == 'ConveyorChainActorSpecialProperties'


class ConveyorChainActorSpecialProperties:
    def __init__(self, first_belt: ObjectReference, last_belt: ObjectReference, belts_in_chain: list, total_length: float, total_number_items_maybe: int, first_chain_item_index: int, last_chain_item_index: int, items: list):
        self.type = 'ConveyorChainActorSpecialProperties'
        self.first_belt = first_belt
        self.last_belt = last_belt
        self.belts_in_chain = belts_in_chain
        self.total_length = total_length
        self.total_number_items_maybe = total_number_items_maybe
        self.first_chain_item_index = first_chain_item_index
        self.last_chain_item_index = last_chain_item_index
        self.items = items

    @staticmethod
    def parse(reader: BinaryReadable) -> 'ConveyorChainActorSpecialProperties':
        last_belt = ObjectReference.read(reader)
        first_belt = ObjectReference.read(reader)
        count_belts_in_chain = reader.read_int32()

        belts_in_chain = []
        for _ in range(count_belts_in_chain):
            chain_actor_ref = ObjectReference.read(reader)
            belt_ref = ObjectReference.read(reader)
            spline_points_count = reader.read_int32()

            spline_points = []
            for _ in range(spline_points_count):
                spline_points.append({
                    'location': vec3.parse(reader),
                    'arrive_tangent': vec3.parse(reader),
                    'leave_tangent': vec3.parse(reader),
                })

            offset_at_start = reader.read_float32()
            starts_at_length = reader.read_float32()
            ends_at_length = reader.read_float32()
            first_item_index = reader.read_int32()
            last_item_index = reader.read_int32()
            belt_index_in_chain = reader.read_int32()

            belts_in_chain.append({
                'chain_actor_ref': chain_actor_ref,
                'belt_ref': belt_ref,
                'spline_points': spline_points,
                'offset_at_start': offset_at_start,
                'starts_at_length': starts_at_length,
                'ends_at_length': ends_at_length,
                'first_item_index': first_item_index,
                'last_item_index': last_item_index,
                'belt_index_in_chain': belt_index_in_chain
            })

        total_length = reader.read_float32()
        total_number_items_maybe = reader.read_int32()
        first_chain_item_index = reader.read_int32()
        last_chain_item_index = reader.read_int32()
        count_items_in_chain = reader.read_int32()

        items = []
        for _ in range(count_items_in_chain):
            item = ObjectReference.read(reader)
            reader.read_int32()
            position = reader.read_int32()
            items.append({'item_reference': item, 'position': position})

        return ConveyorChainActorSpecialProperties(
            first_belt=first_belt,
            last_belt=last_belt,
            belts_in_chain=belts_in_chain,
            total_length=total_length,
            total_number_items_maybe=total_number_items_maybe,
            first_chain_item_index=first_chain_item_index,
            last_chain_item_index=last_chain_item_index,
            items=items
        )

    @staticmethod
    def serialize(writer: ByteWriter, property: 'ConveyorChainActorSpecialProperties'):
        ObjectReference.write(writer, property.last_belt)
        ObjectReference.write(writer, property.first_belt)
        writer.write_int32(len(property.belts_in_chain))

        for belt in property.belts_in_chain:
            ObjectReference.write(writer, belt['chain_actor_ref'])
            ObjectReference.write(writer, belt['belt_ref'])
            writer.write_int32(len(belt['spline_points']))

            for spline_point in belt['spline_points']:
                vec3.serialize(writer, spline_point['location'])
                vec3.serialize(writer, spline_point['arrive_tangent'])
                vec3.serialize(writer, spline_point['leave_tangent'])

            writer.write_float32(belt['offset_at_start'])
            writer.write_float32(belt['starts_at_length'])
            writer.write_float32(belt['ends_at_length'])
            writer.write_int32(belt['first_item_index'])
            writer.write_int32(belt['last_item_index'])
            writer.write_int32(belt['belt_index_in_chain'])

        writer.write_float32(property.total_length)
        writer.write_int32(property.total_number_items_maybe)
        writer.write_int32(property.first_chain_item_index)
        writer.write_int32(property.last_chain_item_index)
        writer.write_int32(len(property.items))

        for item in property.items:
            ObjectReference.write(writer, item['item_reference'])
            writer.write_int32(0)
            writer.write_int32(item['position'])


class ConveyorChainSegmentSpecialProperties:
    def __init__(self, chain_actor_ref: ObjectReference, belt_ref: ObjectReference, spline_points: list, offset_at_start: float, starts_at_length: float, ends_at_length: float, first_item_index: int, last_item_index: int, belt_index_in_chain: int):
        self.chain_actor_ref = chain_actor_ref
        self.belt_ref = belt_ref
        self.spline_points = spline_points
        self.offset_at_start = offset_at_start
        self.starts_at_length = starts_at_length
        self.ends_at_length = ends_at_length
        self.first_item_index = first_item_index
        self.last_item_index = last_item_index
        self.belt_index_in_chain = belt_index_in_chain


class ConveyorItemSpecialProperties:
    def __init__(self, position: int, item_reference: ObjectReference):
        self.position = position
        self.item_reference = item_reference
