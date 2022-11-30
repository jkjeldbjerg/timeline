import unittest
from datetime import date

from timeline.timeline_item import TimelineItem


class TestTimelineItem(unittest.TestCase):
    """ Testing TimelineItem """

    def setUp(self) -> None:
        self.txt: str = 'text'
        self.tag: str = 'tag'
        self.item: TimelineItem = TimelineItem('2020-01-01', '2020-12-31', self.txt, self.tag)
        self.shares: TimelineItem = TimelineItem('2022-11-11', '2022-12-12', 'shares', ['tag', 'something else'])
        self.no_share: TimelineItem = TimelineItem('2022-11-11', '2022-12-12', 'shares')
        self.merger: TimelineItem = TimelineItem('2020-01-01', '2020-12-31', 'original', 'original')
        self.in_merge: TimelineItem = TimelineItem('2020-01-01', '2020-12-31', 'merged', 'merged')

    def test_event(self):
        """ Test creation of an event (start and end the same) """
        d = TimelineItem.event('2022-12-24', 'X-mas', 'holiday')
        self.assertEqual(d.start, d.end)

    def test_init(self):
        """ Test whether data is set correctly """
        self.assertEqual(self.item.start, date.fromisoformat('2020-01-01'))
        self.assertEqual(self.item.end, date.fromisoformat('2020-12-31'))
        self.assertEqual(self.item.data, self.txt)
        self.assertTrue(type(self.item.tags) is set)

        self.assertTrue(type(self.shares.tags) is set)
        self.assertTrue(self.shares.has_tag('tag'))
        self.assertFalse(self.shares.has_tag('no tag'))

        self.assertTrue(type(self.no_share.tags) is set)
        self.assertTrue(len(self.no_share.tags) == 0)

    def test_add_tag(self):
        """ Test whether tag can be added """
        self.item.add_tag('new')
        self.assertTrue(self.item.has_tag('new'))

    def test_has_tag(self):
        """ Test whether tags are set correctly """
        self.assertTrue(self.item.has_tag(self.tag))
        self.assertFalse(self.item.has_tag('some other tag not suppported'))

    def test_shares_tag(self):
        """ Test whether shared tags are recognised """
        self.assertTrue(self.item.shares_tag(self.shares))

    def test_merge(self):
        """ Test a basic merge of two items (tags and strings) """
        self.assertRaises(ValueError, self.item.merge, self.no_share)
        self.merger.merge(self.in_merge)
        look_for = ['original', 'merged']
        self.assertEqual(len(self.merger.tags), len(look_for))
        for tag in look_for:
            self.assertTrue(self.merger.has_tag(tag), f"tag={tag}")
        for line in look_for:
            self.assertTrue(line in self.merger.data)

    def test_merge_lists(self):
        """ Test a merge where one or both has data as list """
        pass


if __name__ == '__main__':
    unittest.main()
