# tests/test_address_parser.py
from mm_address_parser.parser import Parser

def test_parse_full_address():
    parser = Parser()
    address = "မန္တလေးတိုင်းဒေသကြီး မန္တလေးခရိုင် အမရပူမြို့နယ် အမရပူမြို့ ၁၀ရပ်ကွက် မဟာဗန္ဓုလလမ်း"
    
    result = parser.parse(address) 
    print(result)
    assert result["state"] == "မန္တလေးတိုင်း"
    assert result["district"] == "မန္တလေးခရိုင်"
    assert result["township"] == "အမရပူမြို့နယ်"
    assert result["town"] == "အမရပူမြို့"
    assert result["ward"] == "၁၀ရပ်ကွက်"
    assert result["street"] == "မဟာဗန္ဓုလလမ်း"
  

def test_partial_address():
    parser = Parser()
    address = "ရန်ကုန်တိုင်းဒေသကြီး လှိုင်မြို့နယ်"

    result = parser.parse(address)

    assert result["state"] == "ရန်ကုန်တိုင်း"
    assert result["township"] == "လှိုင်မြို့နယ်"

def test_parse_full_address_withspace():
    parser = Parser()
    address = "မန္တလေး တိုင်းဒေသကြီး မန္တလေးခရိုင် အမရပူ မြို့နယ် အမရပူ မြို့ ၁၀ ရပ်ကွက် မဟာဗန္ဓုလ လမ်း"
    
    result = parser.parse(address) 
    print(result)
    assert result["state"] == "မန္တလေးတိုင်း"
    assert result["district"] == "မန္တလေးခရိုင်"
    assert result["township"] == "အမရပူမြို့နယ်"
    assert result["town"] == "အမရပူမြို့"
    assert result["ward"] == "၁၀ရပ်ကွက်"
    assert result["street"] == "မဟာဗန္ဓုလလမ်း"