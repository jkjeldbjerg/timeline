import unittest
from datetime import date, timedelta

from timeline.timeline_item import SimpleTimelineItem


class TestSimpleTimelineItem(unittest.TestCase):

    def setUp(self) -> None:
        """ Set up some standard varibles for tests """
        self.first: SimpleTimelineItem = SimpleTimelineItem('2020-01-01', '2020-12-31')
        self.second: SimpleTimelineItem = SimpleTimelineItem('2021-01-01', '2021-12-31')
        self.equal: SimpleTimelineItem = SimpleTimelineItem('2020-01-01', None)
        self.ending: SimpleTimelineItem = SimpleTimelineItem('2020-02-02', '2020-12-31')
        self.event: SimpleTimelineItem = SimpleTimelineItem('2020-12-24', '2020-12-24')
        self.endless: SimpleTimelineItem = SimpleTimelineItem(None, None)

    def test_init(self):
        self.assertTrue(SimpleTimelineItem('2020-11-11', '2022-11-11') is not None)
        self.assertTrue(SimpleTimelineItem('2020-11-11', '2020-11-11') is not None)
        self.assertRaises(ValueError, SimpleTimelineItem, '2022-11-11', '1980-11-11')

    def test_basic_comparisons(self):
        """ Test the standard comparisons: ==, !=, <, <=, >, >= """
        # ==
        self.assertEqual(self.first, self.equal)
        self.assertNotEqual(self.first, self.second)
        # !=
        self.assertNotEqual(self.first, self.second)
        self.assertTrue(self.first != self.second)
        # <
        self.assertTrue(self.first < self.second)
        self.assertFalse(self.second < self.first)
        self.assertFalse(self.first < self.equal)
        # <=
        self.assertTrue(self.first <= self.second)
        self.assertTrue(self.first <= self.equal)
        self.assertFalse(self.second <= self.first)
        self.assertTrue(self.equal <= self.first)
        # >
        self.assertTrue(self.second > self.first)
        self.assertFalse(self.first > self.second)
        self.assertFalse(self.equal > self.first)
        # >=
        self.assertTrue(self.second >= self.first)
        self.assertTrue(self.equal >= self.first)
        self.assertFalse(self.first >= self.second)
        self.assertTrue(self.first >= self.equal)

    def test_advanced_comparisons(self):
        """ This test checks if a None value yields the correct comparison results: ==, !=, <, <=, >, >= """
        # ==
        self.assertEqual(self.first, self.equal)
        self.assertEqual(self.endless, self.endless)
        self.assertNotEqual(self.first, self.endless)
        self.assertNotEqual(self.endless, self.second)
        # !=
        self.assertNotEqual(self.first, self.endless)
        self.assertTrue(self.endless != self.second)
        self.assertFalse(self.endless != self.endless)
        # <
        self.assertTrue(self.endless < self.second)
        self.assertFalse(self.second < self.endless)
        # <=
        self.assertTrue(self.endless <= self.second)
        self.assertTrue(self.endless <= self.equal)
        self.assertFalse(self.second <= self.endless)
        self.assertTrue(self.endless <= self.endless)
        # >
        self.assertTrue(self.second > self.endless)
        self.assertFalse(self.endless > self.second)
        self.assertFalse(self.endless > self.endless)
        # >=
        self.assertTrue(self.second >= self.endless)
        self.assertTrue(self.endless >= self.endless)
        self.assertFalse(self.endless >= self.second)

    def test_is_event(self):
        """ Test whether the start and end are the same """
        self.assertTrue(self.event.is_event)
        self.assertFalse(self.first.is_event)
        self.assertFalse(self.endless.is_event)

    def test_same(self):
        """ Test whether intervals are exactly the same """
        self.assertTrue(self.first.same(self.first))
        self.assertTrue(self.endless.same(self.endless))
        self.assertTrue(self.second.same(self.second))
        self.assertFalse(self.first.same(self.second))
        self.assertFalse(self.endless.same(self.first))
        self.assertFalse(self.second.same(self.first))

    def test_same_ending(self):
        """ Test for same ending works """
        self.assertTrue(self.first.same_ending(self.first), "Same ending")
        self.assertTrue(self.first.same_ending(self.ending), "Same ending")
        self.assertFalse(self.first.same_ending(self.second), "Different endings")

    def test_endless(self):
        """ Test if endless property works """
        self.assertTrue(self.endless.endless)
        self.assertFalse(self.first.endless)

    def test_overlap(self):
        """ Test whether overlap works - items overlap with dates
            Important: None means no end, so there are corner cases
        """
        self.assertTrue(self.first.overlap(self.first))
        self.assertTrue(self.first.overlap(self.endless))
        self.assertTrue(self.endless.overlap(self.first))
        self.assertTrue(self.event.overlap(self.first))
        self.assertFalse(self.first.overlap(self.second))
        self.assertFalse(self.second.overlap(self.first))

    def test_distinct(self):
        """ Test whether distinct works - items do not overlap with dates
            Important: None means no end, so there are corner cases
            Note: the implementation of this is `not item.overlap(other)`
        """
        first: SimpleTimelineItem = SimpleTimelineItem('2020-01-01', '2020-12-31')
        second: SimpleTimelineItem = SimpleTimelineItem('2021-01-01', '2021-12-31')
        endless: SimpleTimelineItem = SimpleTimelineItem(None, None)
        event: SimpleTimelineItem = SimpleTimelineItem('2020-12-24', '2020-12-24')
        self.assertFalse(first.distinct(first))
        self.assertFalse(first.distinct(endless))
        self.assertFalse(endless.distinct(first))
        self.assertFalse(event.distinct(first))
        self.assertTrue(first.distinct(second))
        self.assertTrue(second.distinct(first))

    def test_contains(self):
        """ Test contains method """
        reference: SimpleTimelineItem = SimpleTimelineItem('2022-01-01', '2022-12-31')
        contained: SimpleTimelineItem = SimpleTimelineItem('2022-01-01', '2022-12-12')
        outside: SimpleTimelineItem = SimpleTimelineItem('2021-01-01', '2021-02-02')
        overlaps: SimpleTimelineItem = SimpleTimelineItem('2022-12-12', '2023-12-12')
        no_start: SimpleTimelineItem = SimpleTimelineItem(None, '2022-02-02')
        self.assertTrue(reference.contains(contained))
        self.assertFalse(reference.contains(outside))
        self.assertFalse(reference.contains(overlaps))
        self.assertFalse(reference.contains(no_start))

    def test_adjacent(self):
        """ Test whether another is right after the current """
        self.assertTrue(self.first.adjacent(self.second))
        self.assertFalse(self.first.adjacent(self.equal))
        self.assertFalse(self.first.adjacent(self.endless))
        self.assertFalse(self.second.adjacent(self.first))
        self.assertFalse(self.endless.adjacent(self.first))

    def test_dict_methods(self):
        """ Test whether dictionary methods work"""
        start: date = date.fromisoformat('2022-01-01')
        end = None
        item: SimpleTimelineItem = SimpleTimelineItem(start, end)
        d: dict = item.to_dict()
        self.assertEqual(d['_start'], start)
        self.assertEqual(d['_end'], end)
        from_dict: SimpleTimelineItem = SimpleTimelineItem.from_dict(d)
        self.assertEqual(from_dict.start, start)
        self.assertEqual(from_dict.end, end)

    def test_len(self):
        """ Test the length method """
        delta: timedelta = timedelta(days=1)
        start: date = date.fromisoformat('2022-11-11')
        end: date = start + delta
        test: SimpleTimelineItem = SimpleTimelineItem(start, end)
        self.assertEqual(len(test), delta.days)
        item: SimpleTimelineItem = SimpleTimelineItem(start, None)
        self.assertRaises(ValueError, len, item)

    def test_timedelta(self):
        """ Test the timedelta length method"""
        delta: timedelta = timedelta(days=1)
        start: date = date.fromisoformat('2022-11-11')
        end: date = start + delta
        test: SimpleTimelineItem = SimpleTimelineItem(start, end)
        self.assertEqual(test.timedelta(), delta)
        item: SimpleTimelineItem = SimpleTimelineItem(start, None)
        self.assertRaises(ValueError, item.timedelta)


if __name__ == '__main__':
    unittest.main()
