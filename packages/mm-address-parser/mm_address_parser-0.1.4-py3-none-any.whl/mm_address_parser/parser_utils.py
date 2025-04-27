import re

def normalize_text(text):
    """
    Preprocesses and normalizes input Myanmar address text.
    """
    keywords = ['ရွာ', 'ရပ်ကွက်', 'လမ်း', 'ရပ်', 'ရပ်ကွပ်', 'မြို့', 'မြို့နယ်', 'ခရိုင်', 'တိုင်း', 'တိုင်းဒေသကြီး', 'ပြည်နယ်', 'ကျေးရွာ', 'နယ်မြေ']
    
    pattern = r'\s+(' + '|'.join(keywords) + r')'
    text = re.sub(pattern, r'\1', text)
    text = text.replace(",", "၊ ").replace(".", "။ ")    
    clean_text = re.sub(r'[^a-zA-Z0-9\u1000-\u109F\s]', '', text)

    pattern = r'(\s*([၊။,])\s*|\s+|(?:၊)(?!\s))'
    text = re.sub(pattern, lambda match: match.group(2) + ' ' if match.group(2) else ' ', clean_text)     
    return text.strip()

def get_street_name(address):
    """
    Function to get street names from the address.
    """
    street_match=re.search(r"([\u1000-\u109F]*(?:\([\d\u1040-\u104F]+\))?\s*လမ်း\s*[\d\u1040-\u104F]*)", address)
    if street_match:
        result = street_match.group(1).strip()
        return result + 'လမ်း' if 'လမ်း' not in result else result
    return None

def get_village_name(address):
    """
    Function to get village names from the address (ရွာ).
    """
    village_match = re.search(r"([\u1000-\u109F\s]+?)(?:ရွာ|ကျေးရွာ)", address)
    if village_match:
        result= village_match.group(1).strip() 
        if not re.search(r'ရွာ|ကျေးရွာ', result):
            return result.split(' ')[-1] + 'ကျေးရွာ'
        else:
            return result.split(' ')[-1]
    return None

def get_ward_name(address):
    """
    Function to get ward names from the address (ရပ်ကွက် / ရပ်ကွပ် / ရပ်).
    """
    ward_match = re.search(r"([\u1000-\u109F\s]*(?:\([\d\u1040-\u104F]+\))?\s?(?:ရပ်ကွက်|ရပ်ကွပ်|ရပ်))", address)
    if ward_match:
        result = ward_match.group(1).strip()
        if not re.search(r'ရပ်ကွက်|ရပ်ကွပ်|ရပ်', result):
            return result.split(' ')[-1] + 'ရပ်ကွက်'
        else:
            return result.split(' ')[-1]
    return None


def get_town_name(address):
    """
    Function to get town names from the address (မြို့, excluding မြို့နယ်).
    """
    town_match = re.search(r"([\u1000-\u109F\s]+)(?=မြို့(?!နယ်))", address)    
    if town_match:
        result = town_match.group(1).strip() + 'မြို့'
        return result.split(' ')[-1] + 'မြို့' if 'မြို့' not in result else result.split(' ')[-1]
    return None


def get_township_name(address):
    """
    Function to get township names from the address (မြို့နယ်).
    """
    township_match = re.search(r"([\u1000-\u109F\s]+)(?=မြို့နယ်)", address)
    if township_match:
        resut =  township_match.group(1).strip()
        return resut.split(' ')[-1] + 'မြို့နယ်' if 'မြို့နယ်' not in resut else resut.split(' ')[-1]
    return None


def get_district_name(address):
    """
    Function to get district names from the address (ခရိုင်).
    """
    district_match = re.search(r"([\u1000-\u109F\s]+ခရိုင်)", address)
    if district_match:
        result =  district_match.group(1).strip()
        return result.split(' ')[-1] + 'ခရိုင်' if 'ခရိုင်' not in result else result.split(' ')[-1]
    return None


def get_region_name(address):
    """
    Function to get region/state names from the address (တိုင်းဒေသကြီး / တိုင်း / ပြည်နယ်).
    """
    if "နေပြည်တော်" in address:
        return "နေပြည်တော်"
    
    region_match = re.search(r"([\u1000-\u109F\s]+(?:နယ်မြေ၊တိုင်းဒေသကြီး|တိုင်း|ပြည်နယ်))", address)
    if region_match:
        result =  region_match.group(1).strip()
        return result.split(' ')[-1] + 'တိုင်း' if 'တိုင်း' not in result else result.split(' ')[-1]
    return None




