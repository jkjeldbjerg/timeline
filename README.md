  # Timeline #

Timeline consists of two main class types:

* `TimelineItem`
  * `SimpleTimelineItem` - base class with comparison etc.
  * `TimelineItem`
* `Timeline`

## TimelineItem ##

For the timeline we have a basic object that denotes an item in the timeline. This is a timeline item,
or *item* for short.

The basic class is the `SimpleTimelineItem` which only holds the timeline item and the operations on the 
timeline item. It can be used but has little practical value as there is no information on what the 
item denotes / points to.

The derived class `TimelineItem` contains the logic on the aspects of a timeline item. This is where
you can add tags and data. 

### SimpleTimelineItem ###

The base class for timeline items. It contains comparisons and various time-related utilities.

A timeline item is represented by a start and an end where end is greater than or equal to start.
Both can be one of `date`, `datetime`, `None`.

If start is None, it means that the start is indefinite, it started "before time". Similarly, if 
end is None, then it means that the end is indefinite. Conceptually, think of it as we do not know
when it started (or do not care), or we might not (yet) know of the end.

**Comparisons** 

All basic comparisons are implemented. They all take the `TimelineItem().start` as base for comparisons.
This means that the ends may be different for two items being equal!

In addition, more special comparisons are added for checking relationships between items.

* Overlap - Do the two item overlap?
* Distinct - Are the two items distinct (i.e. do not overlap)?
* Contained - Is one item contained in the other?
* Adjacent - Does the second item start the day after the first? 
* Same - Do the two items have the same start and end?
* Same ending - Do the two items have the same end?
* Before - does the item start before a specific date or datetime?
* After - does the item end after a specific date or datetime?
  * Combine the two by asking for overlaps with an item?

**Serialisation**

The class can be serialised and de-serialised with the `to_dict` and `@staticmethod from_dict`. 
In addition, `__str__` is implemented.

**Length**

The length of an item can be retrieved by `len()` that returns the number of days. 
A more accurate measure can be found with `timedelta() -> timedelta`.

**Various**

If both start and end are indefinite (yes, I had a use-case for that) then it can be tested by
the property `endless`.

At the other end of the scale an item might be an event which means that `start == end` and can
be checked by the property `is_event`. This will not return True if the item is *endless*.

### TimelineItem(SimpleTimelineItem) ###

This class holds the payload of a timeline item. It can hold any `data` and a set of `tags`.

**Data** 

Can be anything.

**Tagging**

There is a mechanism for tagging items. It is implemented as a `set()` where it is possible to ask
for the existence of a tag, add a tag, or check whether two items share tags.

Deleting tags is under consideration.

**Merging**

If two events share start and end, then the other can be merged into the first. Data will 
automatically be stored in the first and missing tags from the other is added to the first.

**Events**

A factory method `@staticmethod event` allows for creation of an event. All it in fact does is to
set the end = start.


## Testing ##

Testing can be done with Python Unittest framework. All tests are located in [src/test](src/test). 

## Version history

0.1.1 - Minor fixes. Timeline.sort now returns self for chaining. Timeline now supports indices 
for getting items in timeline. Unstable idea as the ordering may change with a `sort`!


## License ##

MIT License, see [LICENSE](LICENSE) file.