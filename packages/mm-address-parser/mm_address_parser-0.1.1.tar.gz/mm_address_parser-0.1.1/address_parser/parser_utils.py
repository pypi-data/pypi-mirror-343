import re

def normalize_text(text):
    """
    Preprocesses and normalizes input Myanmar address text.
    """
    text = re.sub(r'၊(?!\s)', '၊ ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_street_name(address):
    """
    Function to get street names from the address.
    """
    street_match = re.search(r"([\u1000-\u109F]+လမ်း)", address)
    if street_match:
        return street_match.group(1)
    return None


def get_ward_name(address):
    """
    Function to get ward names from the address (ရပ်ကွက် / ရပ်ကွပ် / ရပ်).
    """
    ward_match = re.search(r"([\u1000-\u109F\s]*(?:\([\d\u1040-\u104F]+\))?\s?(?:ရပ်ကွက်|ရပ်ကွပ်|ရပ်))", address)
    if ward_match:
        return ward_match.group(1).strip()
    return None


def get_town_name(address):
    """
    Function to get town names from the address (မြို့, excluding မြို့နယ်).
    """
    town_match = re.search(r"([\u1000-\u109F\s]+)(?=မြို့(?!နယ်))", address)    
    if town_match:
        return town_match.group(1).strip()
    return None


def get_township_name(address):
    """
    Function to get township names from the address (မြို့နယ်).
    """
    township_match = re.search(r"([\u1000-\u109F\s]+)(?=မြို့နယ်)", address)
    if township_match:
        return township_match.group(1).strip()
    return None


def get_district_name(address):
    """
    Function to get district names from the address (ခရိုင်).
    """
    district_match = re.search(r"([\u1000-\u109F\s]+ခရိုင်)", address)
    if district_match:
        return district_match.group(1).strip()
    return None


def get_region_name(address):
    """
    Function to get region/state names from the address (တိုင်းဒေသကြီး / တိုင်း / ပြည်နယ်).
    """
    if "နေပြည်တော်" in address:
        return "နေပြည်တော်"
    
    region_match = re.search(r"([\u1000-\u109F\s]+(?:နယ်မြေ၊တိုင်းဒေသကြီး|တိုင်း|ပြည်နယ်))", address)
    if region_match:
        return region_match.group(1).strip()
    return None

def get_village_name(address):
    """
    Function to get village names from the address (ရွာ).
    """
    village_match = re.search(r"([\u1000-\u109F\s]+?)(?:ရွာ|ကျေးရွာ)", address)
    if village_match:
        return village_match.group(1).strip()
    return None


