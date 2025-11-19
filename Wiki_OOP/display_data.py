from typing import Any
from pyFunction_Wiki import load_json

used_json = [
                "json_display_meta",
                "json_display_metaEN",
            ]

DB = load_json(used_json)

class Display_Database:
    def __init__(self):
        self.data : dict = display_loader(DB)
    
    def getname(self, key: str):
        return self.data[key]["avatarItemName"]
    
    def getdesc(self, key: str):
        return self.data[key]["avatarIdDesc"]
    
    def get(self, key: str):
        return self.data.get(key)
    
    def __getitem__(self, key: str):
        return self.data[key]
    
def display_loader(DB):
    DB_CN   = {avatar["avatarId"]:avatar for avatar in DB["json_display_meta"]["playerAvatarData"]["avatarList"]}
    DB_EN   = {avatar["avatarId"]:avatar for avatar in DB["json_display_metaEN"]["playerAvatarData"]["avatarList"]}
    DB_ALL  = {k:DB_EN[k] if k in DB_EN else DB_CN[k] for k in DB_CN}
    return DB_ALL