from enum import Enum
from typing import Any, Literal

from pyFunction_Wiki import load_json

used_json = [
                "json_skill",
                "json_skillEN",
            ]

DB = load_json(used_json)

class Skill_Database:
    def __init__(self):
        self.CN = DB["json_skill"]
        self.EN = DB["json_skillEN"]
    
    def getname(self, skillId : str):
        if skillId in self.EN:
            return self.EN[skillId]["levels"][0]["name"]
        else:
            return self.CN[skillId]["levels"][0]["name"]

