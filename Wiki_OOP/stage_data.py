import re
from typing import Literal
from Wiki_OOP.enemy_data import Enemy_Database
from pyFunction import printc, printf, printr, script_result, stage_load
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
                        base_stage = rogue_dict["stage"][stage]["linkedStageId"]
                        rogue_dict["hard_dict"][base_stage] = stage
                return rogue_dict
    
'''
def stage_loader():
    stage_dict = {}
    zone_dict = {}
    for stage in DB["json_stage"]["stages"]:
        match DB["json_stage"]["stages"][stage]["stageType"]:
            case _ :
                pass
'''

def get_stage_data(level_id : str, isHard : bool = False, is6Star : bool = False, ignored_group : list[str] = []):
    stage_data      = {}
    diff_type       = "SIX_STAR" if is6Star else "FOUR_STAR" if isHard else "NORMAL"
    stage_json      = stage_load(level_id, "EN")
    valid_list      = valid_lister(stage_json["runes"], diff_type, ignored_group)
    enemies_list    = enemies_lister(stage_json["waves"], valid_list, stage_json["enemyDbRefs"])
    #terrain_list = terrain_lister(stage_json)
    stage_data["unit_limit"]  = global_deploy(stage_json["runes"], stage_json["options"]["characterLimit"], diff_type)
    stage_data["enemies"]     = enemies_list.get("counter")
    stage_data["lp"]          = global_lifepoint(stage_json["runes"], stage_json["options"]["maxLifePoint"], diff_type)
    stage_data["dp"]          = global_dp(stage_json["runes"], stage_json["options"]["initialCost"], diff_type)
    stage_data["dp_regen"]    = global_dp_regen(stage_json["runes"], stage_json["options"]["costIncreaseTime"], diff_type)
    stage_data["maxPlayTime"] = stage_json["options"]["maxPlayTime"]
    #stage_data["deployable"]  = 
    #stage_data["static"]      = 
    #stage_data["terrain"]     = terrain_list
    stage_data["normal"]      = enemies_list.get("NORMAL")
    stage_data["elite"]       = enemies_list.get("ELITE")
    stage_data["boss"]        = enemies_list.get("BOSS")
    return stage_data

def valid_lister(runes_data : dict = {}, diff : Literal["NORMAL", "FOUR_STAR", "SIX_STAR"] = "ALL", ignored_group : list[str] = []):
    enemy_replace = {}
    enable_group = [None]
    disable_group = ignored_group
    #print(ignored_group)
    if runes_data:
        for rune in runes_data:
            if rune["difficultyMask"] not in ["ALL", diff]: continue
            if rune["key"] == "level_hidden_group_enable":
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "key" and blackboard["valueStr"] not in ignored_group:
                        enable_group.append(blackboard["valueStr"])
            elif rune["key"] == "level_hidden_group_disable":
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "key":
                        disable_group.append(blackboard["valueStr"])
            elif rune["key"] == "level_enemy_replace":
                replace_key     = ""
                replace_value   = ""
                for blackboard in rune["blackboard"]:
                    if blackboard["key"] == "key":
                        replace_key = blackboard["valueStr"]
                    elif blackboard["key"] == "value":
                        replace_value = blackboard["valueStr"]
                if replace_key and replace_value:
                    enemy_replace[replace_key] = replace_value
                else:
                    printf(f'"level_enemy_replace" incomplete : {rune}', file = __file__, mode="c")
    return {"enable" : enable_group, "disable" : disable_group, "replace" : enemy_replace}

def enemies_lister(stage_waves : list, valid_dict : dict, enemyDbRefs : list = [], ):
    def enemy_trim(enemy_name):
        trim_result = re.sub(r"(^|.+? )'(.+?)'( .+?|$)",r'\1"\2"\3', enemy_name)
        return trim_result.replace('"', "")
    
    def wiki_enemy(enemy_id : str, enemy_counter : dict[str, int]):
        unique_enemies = []
        isBoss = DB["json_enemy_handbook"]["enemyData"][enemy]["enemyLevel"] == "BOSS"
        isSummon = enemy_counter["isSummon"]
        count_min = enemy_counter["Base"] + enemy_counter["Min"]
        count_max = enemy_counter["Base"] + enemy_counter["Max"]
        enemy_name = enemy_trim(ENEMIES.getname(enemy_id))
        
        if count_min != count_max:
            return f'{{{{E|{enemy_name}|{count_min}|{count_max}}}}}'
        elif (count_min == 1 and (enemy_id in unique_enemies or isBoss)) or (count_min == 0 and isSummon):
            return f'{{{{E|{enemy_name}}}}}'
        elif count_min == 0:
            return ""
        else:
            return f'{{{{E|{enemy_name}|{count_min}}}}}'
        
    enemyDbRefs_dict    = {enemy["id"]:enemy["overwrittenData"]["prefabKey"]["m_value"] if (enemy["overwrittenData"] and enemy["overwrittenData"]["prefabKey"]["m_value"]) else enemy["id"] for enemy in enemyDbRefs}
    enemy_counter       = {"NORMAL" : {}, "ELITE" : {}, "BOSS" : {}, "counter" : "", }
    temp_enemy_counter  = {}
    temp_wave_counter   = {"Base" : 0, "Min" : 0, "Max" : 0}
    
    enable_group    = valid_dict["enable"]
    disable_group   = valid_dict["disable"]
    enemy_replace   = valid_dict["replace"]
    #print(disable_group)
    for wave in stage_waves:
        for fragment in wave["fragments"]:
            GroupKeys        = {}
            GroupKey_packs   = {}
            GroupPackKeys    = {}
            for action in fragment["actions"]:
                if action["randomSpawnGroupPackKey"]:
                    if action["randomSpawnGroupKey"]:
                        GroupKey_packs.setdefault(action["randomSpawnGroupKey"], [])
                        GroupKey_packs[action["randomSpawnGroupKey"]].append(action["randomSpawnGroupPackKey"])
                
                if action["actionType"] == "SPAWN" and action["key"]:
                    enemy_key = enemy_prefabkey(action["key"], enemyDbRefs_dict, enemy_replace)
                    #print(f'action["key"] = {action["key"]} | enemy_key = {enemy_key}')
                else:
                    continue
                
                if action["hiddenGroup"] in enable_group and action["hiddenGroup"] not in disable_group and action["key"].startswith("enemy"):
                    temp_enemy_counter.setdefault(enemy_key, {"Base" : 0, "Min" : 0, "Max" : 0, "isSummon" : False})
                    if action["randomSpawnGroupPackKey"]:
                        GroupPackKeys.setdefault(action["randomSpawnGroupPackKey"], {}).setdefault(enemy_key, 0)
                        GroupPackKeys[action["randomSpawnGroupPackKey"]][enemy_key] += action["count"]
                    elif action["randomSpawnGroupKey"]:
                        GroupKeys.setdefault(action["randomSpawnGroupKey"], {}).setdefault(enemy_key, [])
                        GroupKeys[action["randomSpawnGroupKey"]][enemy_key].append(action["count"])
                    else:
                        temp_enemy_counter[enemy_key]["Base"] += action["count"]
                        temp_wave_counter["Base"] += action["count"]
            if GroupKeys:
                for GroupKey in GroupKeys:
                    if GroupKey == "tel" : continue # extra miniboss on sui sub
                    wave_min = 9999
                    wave_max = 0
                    for enemy in GroupKeys[GroupKey]:
                        enemy_min = min(GroupKeys[GroupKey][enemy])
                        enemy_max = max(GroupKeys[GroupKey][enemy])
                        temp_enemy_counter[enemy]["Min"] += (enemy_min if len(set(GroupKeys[GroupKey].keys())) == 1 else 0)
                        temp_enemy_counter[enemy]["Max"] += enemy_max
                        wave_min = min(wave_min, enemy_min)
                        wave_max = max(wave_max, enemy_max)
                    temp_wave_counter["Min"] += wave_min
                    temp_wave_counter["Max"] += wave_max
            if GroupKey_packs:
                #printc(GroupKey_packs, GroupPackKeys)
                for GroupKey in GroupKey_packs:
                    GroupKey_enemy = set([enemy for group in GroupKey_packs[GroupKey] if group in GroupPackKeys for enemy in GroupPackKeys[group]])
                    for enemy in GroupKey_enemy:
                        enemy_count = [GroupPackKeys[group].get(enemy, 0) if group in GroupPackKeys else 0 for group in GroupKey_packs[GroupKey]]
                        temp_enemy_counter[enemy]["Min"] += min(enemy_count)
                        temp_enemy_counter[enemy]["Max"] += max(enemy_count)
                    wave_count = [sum(GroupPackKeys[group].values()) if group in GroupPackKeys else 0 for group in GroupKey_packs[GroupKey]]
                    temp_wave_counter["Min"] += min(wave_count)
                    temp_wave_counter["Max"] += max(wave_count)
            #printc(GroupKeys, GroupKey_packs, GroupPackKeys,)
    wave_counter = (temp_wave_counter["Base"] + temp_wave_counter["Min"], temp_wave_counter["Base"] + temp_wave_counter["Max"])
    enemy_counter["counter"] = wave_counter[0] if wave_counter[0] == wave_counter[1] else f'{wave_counter[0]}, {wave_counter[1]}'
    #printr(temp_enemy_counter)
    temp_writer = {"NORMAL" : [], "ELITE" : [], "BOSS" : []}
    sorted_enemies = sorted(filter(lambda enemy : enemy in DB["json_enemy_handbook"]["enemyData"], temp_enemy_counter.keys()), key = lambda x : DB["json_enemy_handbook"]["enemyData"][x]["sortId"])
    for enemy in sorted_enemies:
        enemy_wikitext = wiki_enemy(enemy, temp_enemy_counter[enemy])
        if enemy_wikitext: temp_writer[DB["json_enemy_handbook"]["enemyData"][enemy]["enemyLevel"]].append(enemy_wikitext)
    for enemyLevel in temp_writer:
        enemy_counter[enemyLevel] = ", ".join(temp_writer[enemyLevel])
    #temp_counter = (sum([enemy["Base"] + enemy["Min"] for enemy in temp_enemy_counter.values()]), sum([enemy["Base"] + enemy["Max"] for enemy in temp_enemy_counter.values()]))
    #script_result(temp_counter_dict, True, script_exit = True)
    return enemy_counter

def enemy_prefabkey(enemy_key : str, enemyDbRefs : dict = {}, enemy_replace : dict = {}):
    enemy_id = enemy_key
    #print(">>", enemy_id)
    enemy_id = enemy_replace.get(enemy_id, enemy_id)
    #print(">>", enemy_id)
    enemy_id = enemyDbRefs.get(enemy_id, enemy_id)
    #script_result(enemyDbRefs, True, script_exit = True)
    #print(">>", enemy_id)
    return enemy_id

def static_lister(stage_waves : list, valid_dict : dict):
    enable_group    = valid_dict["enable"]
    disable_group   = valid_dict["disable"]
    enemy_replace   = valid_dict["replace"]

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

def global_lifepoint(runes_data: dict, default_lp : int = 3, diff = "ALL"):
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