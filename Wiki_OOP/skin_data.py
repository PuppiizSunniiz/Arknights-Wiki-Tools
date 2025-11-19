from typing import Any
from pyFunction_Wiki import load_json

used_json = [
                "json_skin",
                "json_skinEN",
            ]

DB = load_json(used_json)

class Skin_Database:
    def __init__(self):
        self.data : dict = skin_loader(DB)
    
    def getname(self, key: str):
        return self.data[key]["skinName"]
    
    def getdesc(self, key: str):
        return self.data[key]["description"]
    
    def get(self, key: str):
        return self.data.get(key)
    
    def __getitem__(self, key: str):
        return self.data[key]
    
def skin_loader(DB):
    skin_dict = {}
    for skin in DB["json_skin"]["charSkins"]:
        skin_data = DB["json_skinEN"]["charSkins"][skin]["displaySkin"] if skin in DB["json_skinEN"]["charSkins"] else DB["json_skin"]["charSkins"][skin]["displaySkin"]
        skin_dict[skin] = {
                            "skinName"          : skin_data["skinName"],
                            "dialog"            : skin_data["dialog"],
                            "usage"             : skin_data["usage"],
                            "description"       : skin_data["description"],
                            "obtainApproach"    : skin_data["obtainApproach"],
        }
    return skin_dict