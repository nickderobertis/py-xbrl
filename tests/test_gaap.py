from tests.base import SCHEMAS_PATH, DATA_PATH
import pyxbrl as xbrl

GAAP_SCHEMA_PATH = SCHEMAS_PATH / 'us-gaap-2020-01-31' / 'elts' / 'us-gaap-2020-01-31.xsd'
MSFT_DATA_PATH = DATA_PATH / 'msft-10q_20200930_htm.xml'

def test_parse_gaap_schema():
    import xmlschema
    schema = xmlschema.XMLSchema(str(GAAP_SCHEMA_PATH))
    data = schema.to_dict(str(MSFT_DATA_PATH), validation='lax')
    breakpoint()

    parser = xbrl.XBRLSchemaParser(path=GAAP_SCHEMA_PATH)
    schema = parser.parse()
    breakpoint()