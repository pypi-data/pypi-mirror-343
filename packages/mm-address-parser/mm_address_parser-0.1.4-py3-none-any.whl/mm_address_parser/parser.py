import re
from .parser_utils import (
    normalize_text,
    get_street_name,
    get_ward_name,
    get_town_name,
    get_township_name,
    get_district_name,
    get_region_name,
    get_village_name,
)

class Parser:
    def __init__(self):
        self.extractors = {
        "state": get_region_name,
        "district": get_district_name,
        "township": get_township_name,
        "town": get_town_name,
        "ward": get_ward_name,
        "street": get_street_name,
        "village": get_village_name,
    } 

    def parse(self, address):
        """
        Parses a Myanmar address string and returns a dictionary of components.
        """
        address = normalize_text(address)
        parts = re.split(r"[၊။\s]+", address)
        parsed = {}
        for part in parts:
            cleaned = part.strip()
            for label, extractor in self.extractors.items():
                if label not in parsed:
                    result = extractor(cleaned)
                    if result:
                        parsed[label] = result
                        break  

        return parsed