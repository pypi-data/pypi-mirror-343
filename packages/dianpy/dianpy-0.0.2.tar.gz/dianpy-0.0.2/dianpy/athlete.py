from typing import Literal
from xmlbind import XmlRoot, XmlAttribute


class Athlete(XmlRoot):
    firstname: str = XmlAttribute('firstname')
    lastname: str = XmlAttribute('lastname')
    gender: Literal['M', 'F', 'X'] = XmlAttribute('gender')
    birthdate: str = XmlAttribute('birthdate')
    club: str = XmlAttribute('club')
    time: str = XmlAttribute('time')
    heatnum: int = XmlAttribute('heatnum')
    lanenum: int = XmlAttribute('lanenum')
    entrytime: str = XmlAttribute('entrytime')
    starttime: str = XmlAttribute('starttime')
    completeddistance: int = XmlAttribute('completeddistance')
    timemodified: str = XmlAttribute('timemodified')
    disqualification: str = XmlAttribute('disqualification')
