from pathlib import PosixPath, Path
from typing import Sequence, List, Union, Optional

from pydantic import FilePath, HttpUrl
from lxml import etree
import requests

from pyxbrl.base import BaseModel
from pyxbrl.element import XBRLXSElement


class XBRLSchema(BaseModel):
    elements: List[XBRLXSElement]

    def merge(self, schema: 'XBRLSchema') -> 'XBRLSchema':
        elements = self.elements + schema.elements

        return XBRLSchema(elements=elements)

    def merges(self, schemas: Sequence['XBRLSchema']) -> 'XBRLSchema':
        out = self
        for schema in schemas:
            out = out.merge(schema)
        return out


class XBRLSchemaParser(BaseModel):
    path: Union[FilePath, HttpUrl]
    content: Optional[bytes] = None

    def load(self):
        if isinstance(self.path, (FilePath, Path, PosixPath)):
            self.content = self.path.read_bytes()
        elif isinstance(self.path, HttpUrl):
            response = requests.get(self.path)
            self.content = response.content
        else:
            raise ValueError(f'improper type of path {self.path}: {type(self.path)}')

    def parse(self) -> 'XBRLSchema':
        from pyxbrl.nsimport import XBRLImport

        if self.content is None:
            self.load()

        tree = etree.fromstring(self.content)
        # ns_map = {key: value for key, value in tree.nsmap.items() if key is not None}
        ns_map = tree.nsmap


        element_elems = tree.findall('.//xs:element', namespaces=ns_map)
        elements = [XBRLXSElement.from_lxml(elem) for elem in element_elems]
        schema = XBRLSchema(elements=elements)

        import_elems = tree.findall('.//xs:import', namespaces=ns_map)
        imports = [XBRLImport.from_lxml(imp, base_path=self.path.parent) for imp in import_elems]
        schemas = [imp.resolve() for imp in imports]
        schema = schema.merges(schemas)
        return schema

