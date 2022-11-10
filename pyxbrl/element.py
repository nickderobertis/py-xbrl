from typing import ClassVar, Dict, Optional

from pyxbrl.base import BaseModel


class XBRLXSElement(BaseModel):
    id: str
    name: str
    nillable: bool
    substitution_group: Optional[str] = None
    abstract: Optional[bool] = None
    xml_key_map: ClassVar[Dict[str, str]] = {
        'id': 'id',
        'name': 'name',
        'abstract': 'abstract',
        'nillable': 'nillable',
        'substitutionGroup': 'substitution_group',
    }