from typing import List, Literal
from .event import Event
from xmlbind import XmlRoot, XmlAttribute, XmlElementWrapper


class Meet(XmlRoot):
    name: str = XmlAttribute('name')
    year: int = XmlAttribute('year')
    course: Literal['SCM', 'LSM'] = XmlAttribute('course')
    lanecount: int = XmlAttribute('lanecount')
    timingdistance: int = XmlAttribute('timingdistance')
    feventsagegroups: str = XmlAttribute('feventsagegroups')
    meventsagegroups: str = XmlAttribute('meventsagegroups')
    xeventsagegroups: str = XmlAttribute('xeventsagegroups')
    timestandardfilename: str = XmlAttribute('timestandardfilename')
    disqualificationcodes: str = XmlAttribute('disqualificationcodes')
    events: List[Event] = XmlElementWrapper('EVENT')
