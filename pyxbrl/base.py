from typing import ClassVar, Dict

from pydantic import BaseModel as PydanticBaseModel, Field
from xml.etree.ElementTree import Element


class BaseModel(PydanticBaseModel):
    xml_key_map: ClassVar[Dict[str, str]] = Field(default_factory=lambda: {})

    @classmethod
    def from_lxml(cls, elem: Element, **kwargs):
        data: Dict[str, str] = {}
        for xml_key, model_key in cls.xml_key_map.items():
            data[model_key] = elem.get(xml_key)
        data.update(kwargs)
        return cls(**data)

