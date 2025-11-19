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

    def getname(self, key : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN"):
        match lang:
            case "CN" | "JP" | "KR":
                if key in DB_json[lang].value:
                    return DB_json[lang].value[key]["name"]
                else:
                    print(f'{key} not available in {lang}')
                    exit()
            case _: # default EN
                if key in DB_json["EN"].value:
                    return DB_json["EN"].value[key]["name"]
                elif key in DB_json["CN"].value and DB_json["CN"].value[key]["appellation"] not in ["", " ", None]:
                    return DB_json["CN"].value[key]["appellation"]
                elif key in DB_json["CN"].value:
                    return DB_json["CN"].value[key]["name"]
                else:
                    print(f'{key} not available')
                    exit()
    def getskillId(self, key : str, index : int):
        if key in self.CN:
            return self.CN[key]["skills"][index]["skillId"]
        else:
            print(f'{key} not available')
            exit()