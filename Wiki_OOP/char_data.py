from enum import Enum
from typing import Any, Literal

from pyFunction import B, R, RE, Y, printf
from pyFunction_Wiki import load_json

used_json = [
                "json_character",
                "json_characterEN",
                "json_characterKR",
                "json_characterJP",
                "json_char_meta",
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
        self.char_meta = DB["json_char_meta"]["spCharGroups"]

    def _get_name(self, char_id : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN"):
        if not char_id:
            return ""
        elif char_id in DB_json[lang].value:
            return DB_json[lang].value[char_id]["name"]
        elif char_id in DB_json["CN"].value and DB_json["CN"].value[char_id]["appellation"] not in ["", " ", None]:
            print(f'{char_id} not available in {lang}')
            return DB_json["CN"].value[char_id]["appellation"]
        elif char_id in DB_json["CN"].value:
            return DB_json["CN"].value[char_id]["name"]
        else:
            print(f'{char_id} not available')
            exit()
    
    def _get_id(self, char_name :str, lang : Literal["EN", "CN", "JP", "KR"] = "EN", isObtainable : bool = True):
        if not char_name:
            return ""
        
        for char_id in DB_json[lang].value:
            if isObtainable and DB_json[lang].value[char_id]["isNotObtainable"]: continue
            if char_name in [DB_json[lang].value[char_id]["name"], DB_json[lang].value[char_id]["appellation"]]:
                print(char_name, char_id)
                return char_id
        for char_id in DB_json["CN"].value:
            if isObtainable and DB_json["CN"].value[char_id]["isNotObtainable"]: continue
            if char_name in [DB_json["CN"].value[char_id]["name"], DB_json["CN"].value[char_id]["appellation"]]:
                print(char_name, char_id)
                return char_id
        return ""

    def getdesc(self, char_id : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN"):
        if not char_id:
            return ""
        if char_id.startswith("trap_"):
            if char_id in DB_json[lang].value:
                return DB_json[lang].value[char_id]["itemDesc"] or DB_json[lang].value[char_id]["description"] or ""
            elif char_id in DB_json["CN"].value:
                print(f'{char_id} not available in {lang}')
                return DB_json["CN"].value[char_id]["itemDesc"] or DB_json["CN"].value[char_id]["description"] or ""
            else:
                printf(f'{char_id} not available', file=__file__)
                exit()
        else:
            if char_id in DB_json[lang].value:
                return DB_json[lang].value[char_id]["description"] or ""
            elif char_id in DB_json["CN"].value:
                print(f'{char_id} not available in {lang}')
                return DB_json["CN"].value[char_id]["description"] or ""
            else:
                printf(f'{char_id} not available', file=__file__)
                exit()

    def getid(self, char_str : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN", isObtainable : bool = True):
        if not char_str.startswith(("char_", "trap_", "token_")):
            return self._get_id(char_str, lang, isObtainable)
        else:
            return self._get_name(char_str, lang)

    def getname(self, char_str : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN", isObtainable : bool = True):
        if char_str.startswith(("char_", "trap_", "token_")):
            return self._get_name(char_str, lang)
        else:
            return self._get_id(char_str, lang, isObtainable)
    
    def getname_base(self, char_id : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN"):
        if not char_id:
            return ""
        if char_id in DB["json_char_patch"]["infos"]["char_002_amiya"]["tmplIds"]:
            return self._get_name(char_id, lang)
        for char in self.char_meta:
            if char_id not in self.char_meta[char]:
                continue
            elif len(self.char_meta[char]) == 1:
                return self._get_name(self.char_meta[char][0], lang)
            elif len(self.char_meta[char]) != 2:
                printf(f'Wait that\'s weird : {B}{self.char_meta[char]}{RE} {Y}(len = {len(self.char_meta[char])})', file=__file__)
            else:
                return self._get_name(self.char_meta[char][0], lang)
        
        printf(f'{char_id} not available', file=__file__)
        exit()
    
    def getname_alter(self, char_id : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN"):
        if not char_id:
            return ""
        
        for char in self.char_meta:
            if char_id not in self.char_meta[char]:
                continue
            elif len(self.char_meta[char]) == 1:
                printf(f'{Y}{char_id} {R}doesn\'t{RE} has an {R}alter')
                return ""
            elif len(self.char_meta[char]) != 2:
                printf(f'Wait that\'s weird : {B}{self.char_meta[char]}{RE} {Y}(len = {len(self.char_meta[char])})', file=__file__)
            elif self.char_meta[char].index(char_id) == 0:
                return self._get_name(self.char_meta[char][1], lang)
            else:
                printf(f'{Y}{char_id} {R}ALREADY{RE} is an {R}alter', file=__file__)
        
        printf(f'{Y}{char_id} {R}doesn\'t{RE} has an {R}alter', file=__file__)
        return ""
    
    def getrarity(self, char_id : str):
        if not char_id:
            return ""
        else:
            return self.CN[char_id]["rarity"]
    
    def getskillId(self, char_id : str, index : int):
        if index not in [0, 1, 2]:
            return ""
        elif char_id in self.CN:
            return self.CN[char_id]["skills"][index]["skillId"]
        else:
            printf(f'{char_id} not available', file=__file__)
            exit()