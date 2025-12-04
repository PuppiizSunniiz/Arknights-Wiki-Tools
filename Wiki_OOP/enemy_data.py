from enum import Enum
from typing import Any, Literal

from pyFunction import RE, Y, printc, printr
from pyFunction_Wiki import load_json

used_json = [
                "json_enemy_database",
                "json_enemy_databaseEN",
                "json_enemy_databaseJP",
                "json_enemy_databaseKR",
                "json_enemy_handbook",
                "json_enemy_handbookEN",
                "json_enemy_handbookJP",
                "json_enemy_handbookKR",
            ]

DB = load_json(used_json)

class DB_json(Enum):
    CN  = DB["json_enemy_database"]
    EN  = DB["json_enemy_databaseEN"]
    JP  = DB["json_enemy_databaseJP"]
    KR  = DB["json_enemy_databaseKR"]

class HB_json(Enum):
    CN  = DB["json_enemy_handbook"]
    EN  = DB["json_enemy_handbookEN"]
    JP  = DB["json_enemy_handbookJP"]
    KR  = DB["json_enemy_handbookKR"]
    
class Enemy_Database:
    def __init__(self):
        self.NAMES      = getname_dict()
        self.DB         = enemy_loader()
        self.TYPE       = enemy_type()
        self.NEW_DB     = new_enemy_loader()
    
    def getname(self, enemy_id : str, lang : Literal["CN", "EN", "JP", "KR"] = "EN"):
        if enemy_id in ["-", "", None]:
            return "-"
        elif self.NAMES[enemy_id][lang]:
            return self.NAMES[enemy_id][lang]
        else:
            print(f'{Y}{enemy_id}{RE} not in {Y}{lang}{RE} Server yet')
            return self.NAMES[enemy_id]["CN"]

'''def get(self, key: str):
    return self.DB.get(key)

def __getitem__(self, key: str):
    return self.DB[key]'''

def getname_dict():
    enemy_name_dict = {}
    for lang in DB_json.__dict__["_member_names_"]:
        for enemy in DB_json[lang].value["enemies"]:
            enemy_key = enemy["Key"]
            enemy_name_dict.setdefault(enemy_key, {"CN" : "", "EN" : "", "JP" : "", "KR" : ""})
            enemy_name_dict[enemy_key][lang] = HB_json[lang].value["enemyData"][enemy_key]["name"].strip() if enemy_key in HB_json[lang].value["enemyData"] else enemy["Value"][0]["enemyData"]["name"]["m_value"].strip()
    
    return enemy_name_dict

def enemy_type():
    enemy_type_dict = {}
    for enemy_type in DB["json_enemy_handbook"]["raceData"]:
        enemy_type_dict[enemy_type] = DB["json_enemy_handbookEN"]["raceData"].get(enemy_type, DB["json_enemy_handbook"]["raceData"][enemy_type])["raceName"]
    return enemy_type

def enemy_lv_data(
    enemy_data : dict, 
    enemy_data_EN : dict, 
    lv : int
    ) -> dict:
        temp : dict = {}
        for key in enemy_data[lv]["enemyData"].keys():
            if enemy_data_EN and key in ["name", "description"]:
                temp[key] = enemy_data_EN[0]["enemyData"][key]
            else:
                temp[key] = enemy_data[lv]["enemyData"][key]
        return temp

def enemy_loader():
    # json_enemy_database
    loader = {}
    enemy_database = {enemy["Key"]:enemy["Value"] for enemy in DB["json_enemy_database"]["enemies"]}
    enemy_databaseEN = {enemy["Key"]:enemy["Value"] for enemy in DB["json_enemy_databaseEN"]["enemies"]}
    
    for enemy_key in enemy_database.keys():
        enemy_data = enemy_database[enemy_key]
        enemy_data_EN = enemy_databaseEN[enemy_key] if enemy_key in enemy_databaseEN.keys() else ""
        # ['name', 'description', 'prefabKey', 'attributes', 'applyWay', 'motion', 'enemyTags', 'lifePointReduce', 'levelType', 'rangeRadius', 'numOfExtraDrops', 'viewRadius', 'notCountInTotal', 'talentBlackboard', 'skills', 'spData']
        enemy_data_key = ['name', 'description', 'prefabKey', 'applyWay', 'motion', 'enemyTags', 'lifePointReduce', 'levelType', 'rangeRadius', 'numOfExtraDrops', 'viewRadius', 'notCountInTotal']
        enemy_data_dict = {0 : enemy_lv_data(enemy_data, enemy_data_EN, 0)}
        loader[enemy_key] = {"data" : {key : enemy_data_dict[0][key]["m_value"] for key in enemy_data_key}, "lv" : {}}
        for enemy_level_data in enemy_data:
            if enemy_level_data["level"] != 0:
                enemy_data_dict[enemy_level_data["level"]] = enemy_lv_data(enemy_data, enemy_data_EN, enemy_level_data["level"])
            # ['maxHp', 'atk', 'def', 'magicResistance', 'cost', 'blockCnt', 'moveSpeed', 'attackSpeed', 'baseAttackTime', 'respawnTime', 'hpRecoveryPerSec', 'spRecoveryPerSec', 'maxDeployCount', 'massLevel', 'baseForceLevel', 'tauntLevel', 'epDamageResistance', 'epResistance', 'damageHitratePhysical', 'damageHitrateMagical', 'epBreakRecoverSpeed', 'stunImmune', 'silenceImmune', 'sleepImmune', 'frozenImmune', 'levitateImmune', 'disarmedCombatImmune', 'fearedImmune', 'palsyImmune', 'attractImmune']
            enemy_attr_key = ['maxHp', 'atk', 'def', 'magicResistance', 'moveSpeed', 'attackSpeed', 'baseAttackTime', 'respawnTime', 'hpRecoveryPerSec', 'spRecoveryPerSec', 'massLevel', 'baseForceLevel', 'tauntLevel', 'epDamageResistance', 'epResistance', 'damageHitratePhysical', 'damageHitrateMagical', 'epBreakRecoverSpeed', 'stunImmune', 'silenceImmune', 'sleepImmune', 'frozenImmune', 'levitateImmune', 'disarmedCombatImmune', 'fearedImmune', 'palsyImmune', 'attractImmune']
            enemy_attr_data = {}
            for key in enemy_attr_key:
                if enemy_data_dict[enemy_level_data["level"]]["attributes"][key]["m_defined"]:
                    enemy_attr_data[key] = enemy_data_dict[enemy_level_data["level"]]["attributes"][key]["m_value"]
                else:
                    enemy_attr_data[key] = enemy_data_dict[0]["attributes"][key]["m_value"]
                # lv skill/trait/talents
                for key in ['talentBlackboard', 'skills', 'spData']:
                    if enemy_data_dict[enemy_level_data["level"]][key]:
                        enemy_attr_data[key] = enemy_data_dict[enemy_level_data["level"]][key]
                    else:
                        enemy_attr_data[key] = enemy_data_dict[0][key]
                loader[enemy_key]["lv"][enemy_level_data["level"]] = enemy_attr_data
    
    all_enemies = [[key, loader[key]["data"]["name"]] for key in loader.keys()]
    # json_enemy_handbook
    for enemy in all_enemies:
        if enemy[0] in DB["json_enemy_handbook"]["enemyData"]:
            enemy_handbook_id = enemy[0]
        else: 
            for enemy_handbook_key in DB["json_enemy_handbook"]["enemyData"]:
                if DB["json_enemy_handbook"]["enemyData"][enemy_handbook_key]["name"] == enemy[1]:
                    enemy_handbook_id = enemy_handbook_key
        loader[enemy[0]]["handbook"] = DB["json_enemy_handbookEN"]["enemyData"][enemy_handbook_id] if enemy_handbook_id in DB["json_enemy_handbookEN"]["enemyData"] else DB["json_enemy_handbook"]["enemyData"][enemy_handbook_id]

    return loader

def enemyData_trim(enemy_id : str, level_data : dict, BIG_data : dict):
    enemyData_dict = {}
    level = level_data["level"]
    enemyData = level_data["enemyData"]
    for key in enemyData:
        if key in ["attributes"]:
            enemyData_dict.setdefault("attributes", {})
            for attribute in enemyData["attributes"]:
                isUsed = level in [0, "0"] or (level not in [0, "0"] and enemyData["attributes"][attribute]["m_defined"])
                enemyData_dict["attributes"][attribute] = enemyData["attributes"][attribute]["m_value"] if isUsed else BIG_data[enemy_id][0]["attributes"][attribute]
        elif key in ["talentBlackboard", "skills", "spData"]:
            isBase = level in [0, "0"]
            # TODO
            enemyData_dict[key] = enemyData[key] if isBase else BIG_data[enemy_id][0][key]
        else:
            isUsed = level in [0, "0"] or (level not in [0, "0"] and enemyData[key]["m_defined"])
            enemyData_dict[key] = enemyData[key] if isUsed else BIG_data[enemy_id][0][key]
    return enemyData_dict

def new_enemy_loader():
    BIG_data = {}
    for enemy_data in DB["json_enemy_database"]["enemies"]:
        enemy_id = enemy_data["Key"]
        for level_data in enemy_data["Value"]:
            BIG_data.setdefault(enemy_id, {})
            BIG_data[enemy_id][level_data["level"]] = enemyData_trim(enemy_id, level_data, BIG_data)
    
    for enemy_data in DB["json_enemy_databaseEN"]["enemies"]:
        enemy_id = enemy_data["Key"]
        for key in ["name", "description"]:
            for level in BIG_data[enemy_id]:
                BIG_data[enemy_id][level][key] = enemy_data["Value"][0]["enemyData"][key]["m_value"] if enemy_data["Value"][0]["enemyData"][key]["m_value"] else BIG_data[enemy_id][0][key]
    return BIG_data