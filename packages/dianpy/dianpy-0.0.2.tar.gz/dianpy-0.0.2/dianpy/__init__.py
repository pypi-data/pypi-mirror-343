from typing import Literal
import lxml.etree as ET

from .meet import Meet
from .event import Event
from .athlete import Athlete

from xmlbind.compiler import XmlCompiler
from xmlbind.settings import add_compiler


class LiteralCompiler(XmlCompiler[Literal]):
    def __init__(self):
        super().__init__(Literal)

    def unmarshal(self, v):
        return v

    def marshal(self, v):
        return v


def fromfile(path):
    with open(path, 'rb') as file:
        element = ET.fromstring(file.read())
    return Meet._parse(element)


def tofile(meet: Meet, path):
    element = meet.dump('MEET')
    text = ET.tostring(
        element,
        encoding='utf-8',
        xml_declaration=True,
        pretty_print=True,
        method='xml'
    )
    with open(path, 'wb+') as file:
        file.write(text)


add_compiler(LiteralCompiler())
