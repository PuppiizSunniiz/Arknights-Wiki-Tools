from typing import Any
from pyFunction_Wiki import load_json

used_json = [
                "json_item",
                "json_itemEN",
            ]

DB = load_json(used_json)

class Item_Database:
    def __init__(self):
        self.data : dict = item_loader(DB)
    
    def getname(self, key: str):
        return self.data[key]["name"]
    
    def getdesc(self, key: str):
        return self.data[key]["desc"]
    
    def geticonId(self, key: str):
        return self.data[key]["iconId"]
    
    def get(self, key: str):
        return self.data.get(key)
    
    def __getitem__(self, key: str):
        return self.data[key]

def item_loader(DB):
    item_dict = {}
    for item in DB["json_item"]["items"]:
        item_data = DB["json_itemEN"]["items"][item] if item in DB["json_itemEN"]["items"] else DB["json_item"]["items"][item]
        item_dict[item] = {
                            "name"              : item_data["name"],
                            "description"       : item_data["description"],
                            "rarity"            : item_data["rarity"],
                            "iconId"            : item_data["iconId"],
                            "sortId"            : item_data["sortId"],
                            "usage"             : item_data["usage"],
                            "obtainApproach"    : item_data["obtainApproach"],
        }
    return item_dict