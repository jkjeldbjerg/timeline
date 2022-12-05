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

    def __getattr__(self, item):
        if not isinstance(item, int) or item < 0:
            raise IndexError(f"{item} found, expected int > 0")
        return self._timeline[item]

    def to_list(self) -> list:
        """ convert the timeline to a list """
        self._timeline.sort()
        return [item.to_dict() for item in self._timeline]

    def append(self, stl: SimpleTimelineItem):
        """ Append timeline item """
        self._timeline.append(stl)

    def sort(self, reverse: bool = False):
        """ sort the timeline """
        self._timeline.sort(reverse=reverse)
        return self

    def filter(self, before: Union[None, date, datetime] = None, after: Union[None, date, datetime] = None):
        """ Filter timeline based on dates/datetimes """
        pass

    def data_filter(self, func: [Callable[[SimpleTimelineItem], bool]]):
        """ Filter on data by means of function """
        pass

    def class_filter(self, cls: str):
        pass

    # class Timeline


# EOF
