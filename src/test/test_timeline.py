import datetime
import unittest

from timeline.timeline import Timeline
from timeline.timeline_item import SimpleTimelineItem


class TestTimeline(unittest.TestCase):

    def test_timeline_len(self):
        """ test length """
        timeline: Timeline = Timeline()
        timeline.append(SimpleTimelineItem('2020-09-09', '2020-10-10'))
        timeline.append(SimpleTimelineItem('2022-11-11', '2022-12-12'))
        self.assertEqual(len(timeline), 2)

    def test_timeline_sort(self):
        """ test sorting """
        timeline: Timeline = Timeline()
        timeline.append(SimpleTimelineItem('2020-09-09', '2020-10-10'))
        timeline.append(SimpleTimelineItem('2022-11-11', '2022-12-12'))
        timeline.sort(reverse=True)
        self.assertEqual(timeline[0].start, datetime.date.fromisoformat('2022-11-11'))
        timeline.sort()
        self.assertEqual(timeline[0].start, datetime.date.fromisoformat('2020-09-09'))

    def test_timeline_getitem(self):
        """ test using [] to get data (index) """
        timeline: Timeline = Timeline()
        timeline.append(SimpleTimelineItem('2022-11-11', '2022-12-12'))
        timeline.append(SimpleTimelineItem('2020-09-09', '2020-10-10'))
        self.assertEqual(timeline[0].start, datetime.date.fromisoformat('2022-11-11'))

    def test_timeline_extend(self):
        """ test extending the timeline with another timeline """
        timeline: Timeline = Timeline()
        timeline.append(SimpleTimelineItem('2022-11-11', '2022-12-12'))
        timeline.append(SimpleTimelineItem('2020-09-09', '2020-10-10'))
        timeline2: Timeline = Timeline()
        timeline2.append(SimpleTimelineItem('2022-11-11', '2022-12-12'))
        timeline2.append(SimpleTimelineItem('2020-09-09', '2020-10-10'))
        timeline.extend(timeline2)
        self.assertEqual(len(timeline), 4)

    def test_filter(self):
        """ test filter mechanism """
        timeline: Timeline = Timeline()
        timeline.append(SimpleTimelineItem('2022-11-11', '2022-12-12'))
        timeline.append(SimpleTimelineItem('2020-09-09', '2020-10-10'))
        result = [t for t in timeline.filter(before=datetime.date.fromisoformat('2021-01-01'))]
        self.assertEqual(len(result), 1)

    def test_data_filter(self):
        """ test filtering with a function """
        timeline: Timeline = Timeline()
        timeline.append(SimpleTimelineItem('2022-11-11', '2022-12-12'))
        timeline.append(SimpleTimelineItem('2020-09-09', '2020-10-10'))
        result = [t for t in timeline.data_filter(lambda x: x.start > datetime.date.fromisoformat('2021-01-01'))]
        self.assertEqual(len(result), 1)
        result = [t for t in timeline.data_filter(lambda x: x.start == datetime.date.fromisoformat('2021-01-01'))]
        self.assertEqual(len(result), 0)

    def test_cls_filter(self):
        """ test filtering by class """
        class TestTimelineItem(SimpleTimelineItem):
            pass
        timeline: Timeline = Timeline()
        timeline.append(SimpleTimelineItem('2022-11-11', '2022-12-12'))
        timeline.append(TestTimelineItem('2020-09-09', '2020-10-10'))
        result = [t for t in timeline.class_filter(TestTimelineItem)]
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], TestTimelineItem)
        self.assertEqual(result[0].start, datetime.date.fromisoformat('2020-09-09'))







if __name__ == '__main__':
    unittest.main()
