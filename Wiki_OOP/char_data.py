from typing import Any
from pyFunction import sorted_dict_key
from pyFunction_Wiki import load_json

used_json = [
                "json_character",
                "json_characterEN",
                "json_char_patch",
                "json_char_patchEN",
            ]

DB = load_json(used_json)

class Character_Database:
    def __init__(self):
        DB["json_character"].update(DB["json_char_patch"]["patchChars"])
        DB["json_characterEN"].update(DB["json_char_patchEN"]["patchChars"])
        self.data : dict = character_loader(DB["json_character"], DB["json_characterEN"])
    
    def get(self, key: str):
        return self.data.get(key)
    
    def __getitem__(self, key: str):
        return self.data[key]

def character_loader(DB_CN, DB_EN):
    char_dict = {}
    for char in sorted_dict_key(DB_CN, mode = "keys"):
        char_dict[char] = DB_CN[char]
    return char_dict