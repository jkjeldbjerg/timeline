""" The timeline class """
from datetime import date, datetime
from typing import Union, Callable

from timeline import timeline_item
from timeline.timeline_item import SimpleTimelineItem, TimelineItem


class Timeline:
    """ Timeline class """

    @staticmethod
    def from_list(serialised: list):  # -> Timeline
        """ de-serialise from a list of TimelineItems """
        result: Timeline = Timeline()
        for item in serialised:
            if 'type' in item:  # this code uses the right class from the name stored in serialisation
                tli: SimpleTimelineItem = getattr(timeline_item, item['type'])
                result.append(tli.from_dict(item))

    def __init__(self):
        self._timeline: [SimpleTimelineItem] = list()

    def __getitem__(self, item: int):
        """ get an item from index """
        return self._timeline[item]

    def __len__(self):
        """ get the length of the timeline """
        return len(self._timeline)

    @property
    def timeline(self):
        return self._timeline

    def to_list(self) -> list:
        """ convert the timeline to a list """
        self._timeline.sort()
        return [item.to_dict() for item in self._timeline]

    def append(self, stl: SimpleTimelineItem):
        """ Append timeline item """
        self._timeline.append(stl)

    def extend(self, ti):  # ti: Timeline
        """ extend the timeline with timeline ti """
        self._timeline.extend(ti.timeline)

    def sort(self, reverse: bool = False):
        """ sort the timeline """
        self._timeline.sort(reverse=reverse)
        return self

    def filter(self, before: Union[None, date, datetime] = None, after: Union[None, date, datetime] = None):
        """ Filter timeline based on date/datetime """
        for item in self._timeline:
            if before is not None:
                if item.start > before:
                    continue
            if after is not None:
                if item.start < after:
                    continue
            yield item

    def data_filter(self, func: [Callable[[SimpleTimelineItem], bool]]):
        """ Filter on data by means of function """
        for item in self._timeline:
            if func(item):
                yield item

    def class_filter(self, cls):
        """ filter the timeline on the basis of the class """
        for item in self._timeline:
            if isinstance(item, cls):
                yield item

    # class Timeline


# EOF
