from enum import Enum
from typing import Any, Literal
from pyFunction import printf
from pyFunction_Wiki import load_json

used_json = [
                "json_activity",
                "json_activityEN",
            ]

DB = load_json(used_json)

class DB_json(Enum):
    CN     = DB["json_activity"]
    EN     = DB["json_activityEN"]
    
class Activity_Database:
    def __init__(self):
        self.CN = DB["json_activity"]
        self.EN = DB["json_activityEN"]
    
    def _get_name(self, activity_id : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN"):
        if not activity_id:
            return ""
        if activity_id in DB_json[lang].value["basicInfo"]:
            return DB_json[lang].value["basicInfo"][activity_id]["name"]
        elif activity_id in DB_json["CN"].value["basicInfo"]:
            print(f'{activity_id} not available in {lang}')
            return DB_json["CN"].value["basicInfo"][activity_id]["name"]
        else:
            printf(f'{activity_id} not available', file=__file__)
            exit()
    
    def getname(self, activity_id : str, lang : Literal["EN", "CN", "JP", "KR"] = "EN"):
        return self._get_name(activity_id, lang)
    
    def getMission_dict(self, activity_id):
        activity_json = self.EN if activity_id in self.EN["basicInfo"] else self.CN
        missionIds_list = []
        for missionGroup in activity_json["missionGroup"]:
            if missionGroup["id"] != activity_id:
                continue
            else:
                missionIds_list = missionGroup["missionIds"]
        
        if not missionIds_list:
            print(f'There no mission in : {self._get_name(activity_id)}({activity_id})')
            exit()
        else:
            return {mission["id"]:mission for mission in activity_json["missionData"] if mission["id"] in missionIds_list}

