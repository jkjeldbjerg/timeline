""" The TimelineItem class """
from copy import deepcopy
from datetime import date, datetime, timedelta
from typing import Union, Any


class SimpleTimelineItem:
    """ This is the base class with only the dates implemented.

        The features here are meant to basic functions of an item in a timeline.

        It can be used on its own but the benefits are probably limited...
    """

    @staticmethod
    def from_dict(d: dict):
        """ create object from dict """
        if 'type' not in d and d['type'] != SimpleTimelineItem.__name__:
            raise TypeError('from_dict: not a SimpleTimelineItem dict')
        start: str = 'start' if 'start' in d else '_start'
        end: str = 'end' if 'end' in d else '_end'
        try:
            return SimpleTimelineItem(d[start], d[end])
        except KeyError:
            raise KeyError('from_dict: Invalid serialisation')

    @staticmethod
    def _type_formatter(d: Union[date, datetime, str, None]):
        """ Ensure the format is right for the properties """
        if isinstance(d, (date, datetime)) or not d:
            # d is already in the right format: either date, datetime or None
            return d
        try:
            return date.fromisoformat(d)
        except ValueError:  # not a date iso format
            pass
        try:
            return datetime.fromisoformat(d)
        except ValueError:  # not a datetime iso format
            raise  # re-raise error as this is something to be handled by caller

    def __init__(self, start: Union[date, datetime, str, None], end: Union[date, datetime, str, None]):
        """ Set up the simple timeline item with start and end """
        self._start = SimpleTimelineItem._type_formatter(start)
        self._end = SimpleTimelineItem._type_formatter(end)
        if self._start is not None and self._end is not None and self._start > self._end:
            raise ValueError('Order of timeline is backwards: ends before it starts')

    def to_dict(self) -> dict:
        """ convert data to dictionary (serialise) """
        result: dict = {'type': self.__class__.__name__}
        result.update(self.__dict__)
        return result

    @property
    def start(self) -> Union[date, datetime, None]:
        """ return start date/datetime/None """
        return self._start

    @property
    def end(self) -> Union[date, datetime, None]:
        """ return end date/datetime/None """
        return self._end

    def __eq__(self, other):  # other: SimpleTimelineItem
        return self.start == other.start

    def __ne__(self, other):  # other: SimpleTimelineItem
        return self.start != other.start

    def __lt__(self, other):  # other: SimpleTimelineItem
        try:
            return self.start < other.start
        except TypeError:  # handle comparison None and date/datetime
            if self.start is None:
                return True
            return False

    def __le__(self, other):  # other: SimpleTimelineItem
        try:
            return self.start <= other.start
        except TypeError:  # handle comparison None and date/datetime
            if self.start is None:
                return True
            return False

    def __gt__(self, other):  # other: SimpleTimelineItem
        try:
            return self.start > other.start
        except TypeError:  # handle comparison None and date/datetime
            if self.start is None:
                return False
            return True

    def __ge__(self, other):  # other: SimpleTimelineItem
        try:
            return self.start >= other.start
        except TypeError:  # handle comparison None and date/datetime
            if self.start is None and other.start is None:
                return True
            if self.start is None:
                return False
            return True

    def before(self, other: Union[date, datetime]):
        """ does it start before some point in time? Use-case: filtering data on a timeline """
        if self.start is None:
            return True
        if type(other) is date:
            comparator = other if type(self.start) is date else datetime.combine(other, datetime.min.time())
        elif type(other) is datetime:
            comparator = other if type(self.start) is datetime else other.date()
        else:
            raise ValueError('before: argument must be date or datetime')
        return self.start < comparator

    def after(self, other: Union[date, datetime]):
        """ does is end after some point in time? Use-case: filtering data on a timeline """
        if self.end is None:
            return True
        if type(other) is date:
            comparator = other if type(self.end) is date else datetime.combine(other, datetime.min.time())
        elif type(other) is datetime:
            comparator = other if type(self.end) is datetime else other.date()
        else:
            raise ValueError('after: argument must be date or datetime')
        return self.end > comparator

    def __str__(self) -> str:
        """ to string method """
        st = self._start.isoformat() if self._start else 'None'
        sl = self._end.isoformat() if self._end else 'None'
        return st + " - " + sl

    @property
    def endless(self) -> bool:
        """ is this endless, i.e. start == end == None """
        return self._start is None and self._end is None

    @property
    def is_event(self) -> bool:
        """ is the start and end the same and not endless (None)? """
        return self._start and self._start == self._end

    def same(self, other) -> bool:  # other: SimpleTimelineItem
        """ True if both starts and ends are the same"""
        return self.start == other.start and self.end == other.end

    def same_ending(self, other) -> bool:  # other: SimpleTimelineItem
        """ does two items have the same ending?
            NOT IMPLEMENTED (CONSIDERING THE SANITY): Check on dates only (add strict mode to class property)?
        """
        # if type(self.end) is date and type(other.end) is datetime:
        #     return self.end == other.end.date
        # if type(other.end) is date and type(self.end) is datetime:
        #     return self.end.date == other.end
        return self.end == other.end

    def overlap(self, other) -> bool:  # other: SimpleTimelineItem
        """ does two items overlap? """
        if self.endless or other.endless:
            return True
        try:
            return self.start <= other.start <= self.end or self.start <= other.end <= self.end \
                   or other.start <= self.start <= other.end or other.start <= self.end <= other.end
        except TypeError:
            pass
        try:
            if self.start is None:
                return other.start <= self.end
        except TypeError:
            pass
        try:
            if self.end is None:
                return self.start <= other.end
        except TypeError:
            pass
        try:
            if other.start is None:
                return self.start <= other.end <= self.end
        except TypeError:
            pass
        try:
            if other.end is None:
                return self.start <= other.start <= self.end
        except TypeError:
            pass
        return False

    def distinct(self, other) -> bool:  # other: SimpleTimelineItem
        """ are two items distinct (not overlapping) """
        return not self.overlap(other)

    def contains(self, other) -> bool:  # other: SimpleTimelineItem
        """ does this contain the other? """
        if self.endless:
            return True
        # check self.start <= other.start
        if self.start is not None and (other.start is None or self.start > other.start):
            return False
        if self.end is not None and (other.end is None or self.end < other.end):
            return False
        return True

    def adjacent(self, other) -> bool:  # other: SimpleTimelineItem
        """ is the other the day after this? (checking for patterns) """
        if self.end is None or other.start is None:
            return False
        t1 = self.end if type(self.end) is date else self.end.date()
        t2 = other.start if type(other.start) is date else other.start.date()
        return t1 + timedelta(days=1) == t2

    def __len__(self) -> int:
        """ return the length of a Timeline Item as the number of days or -1 if it has a None start or end """
        if self._start is None or self._end is None:
            raise ValueError('len: Cannot find length with indeterminate start or end')
        return (datetime.combine(self._end, datetime.min.time()) -
                datetime.combine(self._start, datetime.min.time())).days

    def timedelta(self) -> timedelta:
        """ return the length as a timedelta or -1 days if it has a None start or end """
        if self._start is None or self._end is None:
            raise ValueError('timedelta: Cannot find length with indeterminate start or end')
        return datetime.combine(self._end, datetime.min.time()) - datetime.combine(self._start, datetime.min.time())

    # class SimpleTimeline


class TimelineItem(SimpleTimelineItem):
    """ A timeline item with user defined data and a user defined tag (only one tag per item) """

    @staticmethod
    def from_dict(d: dict):  # -> TimelineItem
        """ Deserialise / get from dictionary """
        if 'type' not in d and d['type'] != TimelineItem.__name__:
            raise TypeError('from_dict: Not a TimelineItem dict')
        return TimelineItem(d['start'], d['end'], d['data'], d['tags'])

    @staticmethod
    def event(start: Union[date, datetime, str, None],
              data: Any, tags: Union[str, list, None] = None):
        """ Create an event (start and end are the same) """
        if not start:
            raise ValueError('event: Start cannot be None. It is an event, not endless'
                             '')
        return TimelineItem(start, start, data, tags)

    def __init__(self, start: Union[date, datetime, str, None], end: Union[date, datetime, str, None],
                 data: Any, tags: Union[str, set, list, None] = None):
        """ Initialiser for a TimelineItem with start, end and some data"""
        super().__init__(start, end)
        self.data: Any = data
        self.tags: set = set()
        if type(tags) is str:
            self.tags.add(tags)
        elif type(tags) is list or type(tags) is set:
            self.tags.update(tags)

    def add_tag(self, tag: str):
        """ Adding a tag to set """
        self.tags.add(tag)

    def has_tag(self, tag: str):
        """ Does the item have a specific tag """
        return tag in self.tags

    def shares_tag(self, other) -> bool:  # other: TimelineItem
        """ Do two items share tag """
        for tag in self.tags:
            if tag in other.tags:
                return True
        return False

    def merge(self, other):  # other: TimelineItem
        """ merge if they have the same dates """
        if not self.same(other):
            raise ValueError("Items do not have the same timeline")
        self.tags.update(other.tags)
        if type(self.data) is list:
            if type(other.data) is list:
                self.data.extend(other.data)
            else:
                self.data.append(other.data)
        else:
            self.data = [self.data, other.data]
        return self

    # class TimelineItem

# EOF
