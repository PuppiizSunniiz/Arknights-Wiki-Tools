from typing import Any

from pyFunction_Wiki import load_json

used_json = [
                "json_enemy_database",
                "json_enemy_databaseEN",
                "json_enemy_handbook",
                "json_enemy_handbookEN",
            ]

DB = load_json(used_json)

class Enemy_Database:
    def __init__(self):
        self.DB = enemy_loader(DB)
        self.TYPE = enemy_type(DB)

    def get(self, key: str):
        return self.DB.get(key)

    def __getitem__(self, key: str):
        return self.DB[key]

def enemy_type(DB : dict[str, Any]):
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

def enemy_loader(DB):
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