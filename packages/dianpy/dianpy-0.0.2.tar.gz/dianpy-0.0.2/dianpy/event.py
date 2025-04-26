
from typing import List, Literal
from .athlete import Athlete
from xmlbind import XmlRoot, XmlAttribute, XmlElementWrapper


class Event(XmlRoot):
    name: str = XmlAttribute('name')
    gender: Literal['M', 'F', 'X'] = XmlAttribute('gender')
    stroke: str = XmlAttribute('stroke')
    distance: int = XmlAttribute('distance')
    heatcount: int = XmlAttribute('heatcount')
    relaycount: int = XmlAttribute('relaycount')
    athletes: List[Athlete] = XmlElementWrapper('ATHLETE')
