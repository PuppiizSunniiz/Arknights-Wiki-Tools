import re
from typing import Literal
from Wiki_OOP.enemy_data import Enemy_Database
from pyFunction import printc, printf, stage_load
from pyFunction_Wiki import load_json

used_json = [
                "json_activity",
                "json_activityEN",
                "json_character",
                "json_characterEN",
                "json_enemy_database",
                "json_enemy_databaseEN",
                "json_enemy_handbook",
                "json_enemy_handbookEN",
                "json_item",
                "json_itemEN",
                "json_roguelike_topic",
                "json_roguelike_topicEN",
                "json_skill",
                "json_skillEN",
                "json_stage",
                "json_stageEN",
                "json_uniequip",
                "json_zone",
                "json_zoneEN"
            ]

DB = load_json(used_json)
ENEMIES = Enemy_Database()
class Stage_Database:
    def __init__(self):
        pass
        #self.data : dict = stage_loader()
    
    def Lister(
                self, 
                event_id : str = "", 
                event_type : Literal['episode', 'intermezzo', 'sidestory', 'storycollection', 'ig', 'is', 'sss', 'tn', 'vb'] = "",
                year : str | int = "",
                ):
        match event_type:
            case "is":
                rogue_dict          = {"stage" : {}, "hard_dict" : {}}
                rogue_season        = f'rogue_{int(year) - 1}'
                rogue_dict["stage"] = DB["json_roguelike_topicEN"]["details"][rogue_season]["stages"] if rogue_season in DB["json_roguelike_topicEN"]["details"] else DB["json_roguelike_topic"]["details"][rogue_season]["stages"] if rogue_season in DB["json_roguelike_topic"]["details"] else {}
                for stage in rogue_dict["stage"]:
                    if rogue_dict["stage"][stage]["linkedStageId"]:
                        rogue_dict["hard_dict"][stage] = rogue_dict["stage"][stage]["linkedStageId"]
                return rogue_dict
    
    def get_stage_data(level_id : str, isHard : bool = False, is6Star : bool = False):
        stage_data  = {}
        diff_type   = "SIX_STAR" if is6Star else "FOUR_STAR" if isHard else "NORMAL"
        stage_json  = stage_load(level_id)
        enemies_list = enemies_lister(stage_json["waves"], stage_json["enemyDbRefs"], stage_json["runes"], diff_type)
        #terrain_list = terrain_lister(stage_json)
        
        unit_limit  = global_deploy(stage_json["runes"], stage_json["options"]["characterLimit"], diff_type)
        enemies     = enemies_list.get("counter")
        lp          = global_lifepoint(stage_json["runes"], stage_json["options"]["maxLifePoint"], diff_type)
        dp          = global_dp(stage_json["runes"], stage_json["options"]["initialCost"], diff_type)
        dp_regen    = global_dp_regen(stage_json["runes"], stage_json["options"]["costIncreaseTime"], diff_type)
        maxPlayTime = stage_json["options"]["maxPlayTime"]
        #deployable  = 
        #static      = 
        #terrain     = terrain_list
        normal      = enemies_list.get("NORMAL")
        elite       = enemies_list.get("ELITE")
        boss        = enemies_list.get("BOSS")
        
'''
def stage_loader():
    stage_dict = {}
    zone_dict = {}
    for stage in DB["json_stage"]["stages"]:
        match DB["json_stage"]["stages"][stage]["stageType"]:
            case _ :
                pass
'''

def enemies_lister(stage_waves : list, enemyDbRefs : list, runes_data : dict, diff : Literal["NORMAL", "FOUR_STAR", "SIX_STAR"] = "ALL"):
    enemy_counter = {"NORMAL" : {}, "ELITE" : {}, "BOSS" : {}, "counter" : {}, }
    enemy_replace = {}
    valid_group = [None]
    if runes_data:
        for rune in runes_data:
            if rune["key"] == "level_hidden_group_enable" and rune["difficultyMask"] in ["ALL", diff]:
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "value":
                        valid_group.append(blackboard["valueStr"])
            elif rune["key"] == "level_hidden_group_disable" and rune["difficultyMask"] in ["ALL", diff]:
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "value":
                        try :
                            valid_group.remove(blackboard["valueStr"])
                        except ValueError :
                            print(blackboard["valueStr"])
            elif rune["key"] == "level_enemy_replace" and rune["difficultyMask"] in ["ALL", diff]:
                replace_key     = ""
                replace_value   = ""
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "key":
                        replace_key = blackboard["valueStr"]
                    elif blackboard["key"] == "key":
                        replace_value = blackboard["valueStr"]
                if replace_key and replace_value:
                    enemy_replace[replace_key] = replace_value
                else:
                    printf(f'"level_enemy_replace" incomplete : {rune}', __file__, "c")
    for wave in stage_waves:
        for fragment in wave["fragments"]:
            GroupKey = {}
            GroupPackKey = {}
            for action in fragment["actions"]:
                if action["actionType"] == "SPAWN" and action["hiddenGroup"] in valid_group:
                    if GroupKey or GroupPackKey:
                        pass
                    else:
                        

def global_dp(runes_data : dict, default_dp : int, diff = "ALL"):
    dp = default_dp
    if runes_data:
        for rune in runes_data:
            if rune["key"] == "global_initial_cost_add" and rune["difficultyMask"] in ["ALL", diff]:
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "value":
                        dp += blackboard["value"]
    return dp

def global_dp_regen(runes_data : dict, default_dp_regen : int, diff = "ALL"):
    dp_regen = default_dp_regen
    if runes_data:
        for rune in runes_data:
            if rune["key"] == "global_cost_recovery_mul" and rune["difficultyMask"] in ["ALL", diff]:
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "value":
                        dp_regen *= blackboard["value"]
    return dp_regen

def global_deploy(runes_data : dict, default_deploy : int, diff = "ALL"):
    deploy_count = default_deploy
    if runes_data:
        for rune in runes_data:
            if rune["key"] == "global_placable_char_num_add" and rune["difficultyMask"] in ["ALL", diff]:
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "value":
                        deploy_count += blackboard["value"]
    return deploy_count

def global_lifepoint(runes_data, default_lp = 3, diff = "ALL"):
    lp = default_lp
    if runes_data:
        for rune in runes_data:
            if rune["key"] == "global_lifepoint_add" and rune["difficultyMask"] in ["ALL", diff]:
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "value":
                        lp += blackboard["value"]
            elif rune["key"] == "global_lifepoint" and rune["difficultyMask"] in ["ALL", diff]:
                return blackboard["value"]
    return lp