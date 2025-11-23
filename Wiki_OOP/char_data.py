from enum import Enum
from typing import Any, Literal

from pyFunction_Wiki import load_json

used_json = [
                "json_character",
                "json_characterEN",
                "json_characterKR",
                "json_characterJP",
                "json_char_patch",
                "json_char_patchEN",
                "json_char_patchKR",
                "json_char_patchJP",
            ]

DB = load_json(used_json)

DB["json_character"].update(DB["json_char_patch"]["patchChars"])
DB["json_characterEN"].update(DB["json_char_patchEN"]["patchChars"])
DB["json_characterKR"].update(DB["json_char_patchKR"]["patchChars"])
DB["json_characterJP"].update(DB["json_char_patchJP"]["patchChars"])

class DB_json(Enum):
    CN     = DB["json_character"]
    EN     = DB["json_characterEN"]
    KR     = DB["json_characterKR"]
    JP     = DB["json_characterJP"]

class Character_Database:
    def __init__(self):
        self.CN = DB["json_character"]
        self.EN = DB["json_characterEN"]
        self.KR = DB["json_characterKR"]
        self.JP = DB["json_characterJP"]

    def getname(self, char_id : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN"):
        if not char_id:
            return ""
        match lang:
            case "CN" | "JP" | "KR":
                if char_id in DB_json[lang].value:
                    return DB_json[lang].value[char_id]["name"]
                else:
                    print(f'{char_id} not available in {lang}')
                    exit()
            case _: # default EN
                if char_id in DB_json["EN"].value:
                    return DB_json["EN"].value[char_id]["name"]
                elif char_id in DB_json["CN"].value and DB_json["CN"].value[char_id]["appellation"] not in ["", " ", None]:
                    return DB_json["CN"].value[char_id]["appellation"]
                elif char_id in DB_json["CN"].value:
                    return DB_json["CN"].value[char_id]["name"]
                else:
                    print(f'{char_id} not available')
                    exit()
    def getskillId(self, char_id : str, index : int):
        if index not in [0, 1, 2]:
            return ""
        elif char_id in self.CN:
            return self.CN[char_id]["skills"][index]["skillId"]
        else:
            print(f'{char_id} not available')
            exit()