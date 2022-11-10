from pathlib import Path
from typing import Union, Dict, ClassVar, Optional, Any
from xml.etree.ElementTree import Element
import requests

from pydantic import FilePath, HttpUrl, validator, DirectoryPath, validate_arguments, ValidationError

from pyxbrl.base import BaseModel
from pyxbrl.schema import XBRLSchema, XBRLSchemaParser


class XBRLImport(BaseModel):
    namespace: str
    schema_location: Union[str, HttpUrl]
    base_path: Optional[DirectoryPath] = None
    xml_key_map: ClassVar[Dict[str, str]] = {
        'namespace': 'namespace',
        'schemaLocation': 'schema_location'
    }

    @property
    def full_schema_location(self) -> Union[Path, HttpUrl]:
        if is_url(self.schema_location):
            return self.schema_location
        if self.base_path is not None:
            return self.base_path / self.schema_location
        return Path(self.schema_location)

    def resolve(self) -> XBRLSchema:
        parser = XBRLSchemaParser(path=self.full_schema_location)
        return parser.parse()


def is_url(content: Any) -> bool:
    try:
        _url(content)
        return True
    except ValidationError:
        return False


@validate_arguments
def _url(url: HttpUrl):
    pass