import re
from typing import Any
from Wiki_Dict import ENEMY_NAMES_TL, ITEM_NAMES_TL, SKILL_NAMES_TL, TOKEN_NAMES_TL
from pyFunction_Wiki import load_json, wiki_story, wiki_trim
from pyFunction import B, G, R, RE, Y, decimal_format, falsy_compare, join_and, json_load, printc, printr, script_result

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
                "json_skill",
                "json_skillEN",
                "json_stage",
                "json_stageEN",
                "json_zone",
                "json_zoneEN"
            ]

DB = load_json(used_json)

def wiki_enemies(event : str = "", show : bool = False) -> dict :
    def enemy_lv_data(enemy_data : dict, enemy_data_EN : dict, lv : int) -> dict:
        temp : dict = {}
        for key in enemy_data_EN[lv]["enemyData"].keys():
            if enemy_data_EN and key in ["name", "description"]:
                temp[key] = enemy_data_EN[lv]["enemyData"][key]
            else:
                temp[key] = enemy_data[lv]["enemyData"][key]
        return temp
        
    data = {"zone" : {}, "stage" : {}, "enemies" : {}, "enemy_type" : {}}
    ACT = event if event else "act43side" # "act43side" = Act or Die
    ZonetoAct = DB["json_activity"]["zoneToActivity"]
    actzone = [zone for zone in ZonetoAct.keys() if ZonetoAct[zone] == ACT]
    if not actzone:
        printr(f'There no zone in this activity : {ACT}')
        exit()
    for zone in actzone:
        if zone in DB["json_zoneEN"]["zones"].keys():
            data["zone"].setdefault(zone, {})["name"] = DB["json_zoneEN"]["zones"][zone]["zoneNameSecond"]
        else:
            data["zone"].setdefault(zone, {})["name"] = DB["json_zone"]["zones"][zone]["zoneNameSecond"]
    
    CN_stage = DB["json_stage"]["stages"]
    EN_stage = DB["json_stageEN"]["stages"]
    stages = {}
    for stage in CN_stage.keys():
        if CN_stage[stage]["zoneId"] in actzone:
            stages[stage] = CN_stage[stage]
            if stage in EN_stage:
                for key in ["name", "description"]:
                    stages[stage][key] = EN_stage[stage][key]
                

            if stage.find("#f#") == -1: data["zone"][CN_stage[stage]["zoneId"]].setdefault("stages", []).append(CN_stage[stage]["code"])
    
    data["stage_data"] = stages
    
    for stage in stages.keys():
        if stage.find("easy_") != -1: continue
        #printr(stage)
        if stage.find("#f#") == -1 and stages[stage]["levelId"]:
            stage_json = json_load(rf'json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\{stages[stage]["levelId"].lower()}.json')
            if not isinstance(stage_json, dict):
                printr(f'\n{R}File path error {G}"{stage}" : {B}{stages[stage]["levelId"].lower()}{RE}')
                exit()
            
            for key in ["options", "mapData", "runes", "globalBuffs", "enemyDbRefs", "predefines", "hardPredefines", "routes", "waves"]:
                data["stage"].setdefault(stage, {})[key] = stage_json[key]
                if key == "enemyDbRefs":
                    for enemy in stage_json[key]:
                        if enemy["overwrittenData"] and enemy["overwrittenData"]["prefabKey"]["m_defined"]:
                            data["enemies"][enemy["overwrittenData"]["prefabKey"]["m_value"]] = {}
                        else :
                            data["enemies"][enemy["id"]] ={}
    # json_enemy_database
    act_enemies = data["enemies"].keys()
    
    enemy_database = {enemy["Key"]:enemy["Value"] for enemy in DB["json_enemy_database"]["enemies"]}
    enemy_databaseEN = {enemy["Key"]:enemy["Value"] for enemy in DB["json_enemy_databaseEN"]["enemies"]}
    
    for enemy_key in enemy_database.keys():
        if enemy_key in act_enemies:
            enemy_data = enemy_database[enemy_key]
            enemy_data_EN = enemy_databaseEN[enemy_key] if enemy_key in enemy_databaseEN.keys() else ""
            # ['name', 'description', 'prefabKey', 'attributes', 'applyWay', 'motion', 'enemyTags', 'lifePointReduce', 'levelType', 'rangeRadius', 'numOfExtraDrops', 'viewRadius', 'notCountInTotal', 'talentBlackboard', 'skills', 'spData']
            enemy_data_key = ['name', 'description', 'prefabKey', 'applyWay', 'motion', 'enemyTags', 'lifePointReduce', 'levelType', 'rangeRadius', 'numOfExtraDrops', 'viewRadius', 'notCountInTotal']
            enemy_data_dict = {0 : enemy_lv_data(enemy_data, enemy_data_EN, 0)}
            data["enemies"][enemy_key] = {"data" : {key : enemy_data_dict[0][key]["m_value"] for key in enemy_data_key}, "lv" : {}}
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
                    data["enemies"][enemy_key]["lv"][enemy_level_data["level"]] = enemy_attr_data
    
    act_enemies = [[key, data["enemies"][key]["data"]["name"]] for key in data["enemies"].keys()]
    # json_enemy_handbook
    for enemy in act_enemies:
        if enemy[0] in DB["json_enemy_handbook"]["enemyData"]:
            enemy_handbook_id = enemy[0]
        else: 
            for enemy_handbook_key in DB["json_enemy_handbook"]["enemyData"]:
                if DB["json_enemy_handbook"]["enemyData"][enemy_handbook_key]["name"] == enemy[1]:
                    enemy_handbook_id = enemy_handbook_key
        data["enemies"][enemy[0]]["handbook"] = DB["json_enemy_handbookEN"]["enemyData"][enemy_handbook_id] if enemy_handbook_id in DB["json_enemy_handbookEN"]["enemyData"] else DB["json_enemy_handbook"]["enemyData"][enemy_handbook_id]
        #print(data["enemies"][enemy[0]])
    # Enemy type dict
    ## CN
    for enemy_type in DB["json_enemy_handbook"]["raceData"]:
        data["enemy_type"][enemy_type] = DB["json_enemy_handbookEN"]["raceData"].get(enemy_type, DB["json_enemy_handbook"]["raceData"][enemy_type])["raceName"]
    
    #script_result(data, show)
    return data
    
def wiki_article(event_code : str, event_type = "", event_name = "") -> list:
    '''
        event_type = episode/ intermezzo/ sidestory/ storycollection
                    vb/ ig
        
        page_footer = 
        
            "Side Story operations" - intermezzo/ sidestory/ storycollection
        
            "Seasonal game modes" - vb/ ig
            
            "Other event operations" - ig
        
    '''
    enemy_rune = ["enemy_attribute_mul", "char_attribute_mul", "level_enemy_replace", "level_hidden_group_enable", "level_hidden_group_disable", "env_gbuff_new_with_verify", "env_gbuff_new", "cooperate_enemy_side_shared", "enemy_talent_blackb_mul"]
    non_enemy_rune = ["env_system_new", "global_cost_recovery_mul", "global_lifepoint", "map_tile_blackb_assign", "env_gbuff_new_with_verify", "env_gbuff_new", "char_attribute_add", "cbuff_max_cost", "char_skill_blackb_mul", "char_cost_add", "global_cost_recovery", "char_blockcnt_add", "char_skill_cd_mul"]
    both_rune = ["env_gbuff_new_with_verify", "env_gbuff_new"]
    skip_rune = ["env_035_act1break_boss[hud]", "global_placable_char_num_add"]
    
    enemy_buffs = ["cooperate_enemy_catch_up", "cooperate_enemy_after_attack_harder"]
    non_enemy_buffs = ["periodic_damage", "cooperate_fortress_global_buff", "character_in_magiccircuit_env"]
    skip_buffs = ["strife_mode_feature", "act27sisde_enemy_global_buff", "mainline12_sightManager", "night_map_default"]
    
    def stage_level(level : str) -> str:
            if level == "-" or not level:
                return ""
            elif level.find("精英") != -1:
                return f'Elite {level.split("精英")[-1].split("LV.")[0].strip()} Level {level.split("LV.")[-1]}'.replace("二", "2")
            else:
                return f'Level {level.split("LV.")[-1]}'
    
    def desc_cond_writer(desc_cond : str) -> str:
        def desc_tl(desc):
            desc_tl_dict = {
                "'''<[[涨潮]]>'''被淹没的地块无法部署，水中的我方单位攻击速度降低，持续受到侵蚀损伤" : "'''<[[High Tide]]>''' Unable to deploy on flooded tiles. Allied units and enemies in the water will be affected by \"Erosion\"",
                "'''<[[岩浆喷射处]]>'''每隔一定时间会喷出岩浆，对周围8格内的我方单位造成大量伤害且融化障碍物" : "'''<[[Lava Crack]]>''' spray out lava periodically, dealing massive damage to friendly units on the surrounding 8 tiles and melting down Roadblocks",
                "'''<[[热泵通道]]>'''每隔一段时间便会对其上的我军和敌军造成大量伤害" : "'''<[[Heat Pump Passage]]>''' that periodically inflict damage to units standing on them are present on the field",
                "部分敌人的基础属性提升" : "Increases some enemies' base stats.",
                "'''<[[毒性雾霾]]>'''我方单位会持续失去生命" : "'''<[[Poison Haze]]>''' Operators lose HP constantly",
                "'''<[[沼泽地段]]>'''置于其中的干员攻击速度逐渐降低，经过的敌人攻击速度和移动速度逐渐降低" : "'''<[[Mire]]>'''Gradually reduces the ASPD of Operators within, and the ASPD and Movement Speed of enemies within",
                "'''<[[芦苇丛]]>'''置于其中的干员获得\"迷彩\"" : "'''<[[Reed Beds]]>''' Operators within gain Camouflage.",
                "'''<[[玉门天灾工事]]>'''置于其中的单位对地面单位造成的伤害提升，受到来自地面单位的伤害降低" : "'''<[[Yumen Catastrophe Defense]]>''' Units placed here deal more damage to ground units and take less damage from ground units.",
                "\\n\\n<color=#FFA300>'''<[[危险区域]]>'''</color>危险区域内的干员会在波次转换时撤退" : "",
                "\\n\\n<color=#FFA300>'''<[[实体程式]]>'''</color>已完成波次再次挑战时可以激活，激活后本波次内我方干员获得大幅强化" : "",
                "\\n\\n<color=#FFA300>'''<[[定向试炼]]>'''</color>定向试炼提供3名预选干员组成的小队": "",
                "<color=#EC1F1FFF>附加条件：</color>" : ""
            }
            for k,v in desc_tl_dict.items():
                desc = desc.replace(k,v)
            return desc
        # rft skip
        desc = re.sub(r'<@lv\.(?:muitem)><(.+?)><\/>', r"'''{{Color|<[[\1]]>|muitem}}'''", desc_cond)
        desc = re.sub(r'<@lv\.(?:muitem)>(.+?)<\/>', r"{{Color|\1|muitem}}", desc)
        # stage mechanic
        desc = re.sub(r'<@[A-Za-z\.1-9_]*?><(.*?)><\/>', r"'''<[[\1]]>'''", desc)
        # challenge condition
        if re.search(r'<@lv.fs>附加条件：<\/>\\n', desc):
            desc = re.sub(r'<@lv.fs>附加条件：<\/>\\n', "", desc)
            desc = re.sub(r'<[^[](.*?)[^]\/]>', r"'''<[[\1]]>'''", desc)
        else:
            desc = re.sub(r'<([^[c/].*?[^]\/])>', r"'''<[[\1]]>'''", desc)
        return desc_tl(desc).replace("\\n", "<br/>").replace("\n", "<br/>").replace("<br/><br/>", "<br/>")
    
    def stage_kill_lister(data : dict, stage_key : str, stage_diff : str = "") -> dict:
        def enemy_ref_dict(enemyDbRefs : list) -> dict:
            temp = {}
            for enemy in enemyDbRefs:
                if enemy["overwrittenData"] and enemy["overwrittenData"]["prefabKey"]["m_defined"]:
                    temp[enemy["id"]] = enemy["overwrittenData"]["prefabKey"]["m_value"]
                else :
                    temp[enemy["id"]] = enemy["id"]
            return temp
        
        def ig_wave_lister(ig_wave_list : dict[str, dict[str, int]], ig_wave_keys : list[str]) -> dict:
            ig_wave_result = {}
            ig_enemy_result = [0, 0]
            for key in ig_wave_keys:
                ig_wave_enemy = []
                for wave_key in ig_wave_list.keys():
                    if not wave_key.startswith(key):
                        continue
                    for enemy_key in ig_wave_list[wave_key].keys():
                        ig_wave_enemy.append(enemy_key)
                
                for enemy_key in set(ig_wave_enemy):
                    enemy_count = [ig_wave_list[wave_key].get(enemy_key, 0) for wave_key in ig_wave_list.keys() if wave_key.startswith(key)]
                    ig_wave_result.setdefault(enemy_key, (0, 0))
                    ig_wave_result[enemy_key] = (ig_wave_result[enemy_key][0] + min(enemy_count), ig_wave_result[enemy_key][1] + max(enemy_count))
                
                wave_count = [sum(list(ig_wave_list[wave_key].values())) for wave_key in ig_wave_list.keys() if wave_key.startswith(key)] if not key.startswith("boss") else [1]
                
                #printc(stage_key, key, ig_wave_keys, wave_count, set(ig_wave_enemy))
                ig_enemy_result = [ig_enemy_result[0] + min(wave_count), ig_enemy_result[1] + max(wave_count)]
                #printr("ig_wave_lister", ig_wave_result, ig_enemy_result)
                #exit()
            return ig_wave_result, ig_enemy_result
        
        def spawner_finder(mapData : dict):
            spawner_index = ""
            for tile in mapData["tiles"]:
                if tile["tileKey"] == "tile_mpprts_enemy_born":
                    spawner_index = mapData["tiles"].index(tile)
                
            if spawner_index:
                x_max = len(mapData["map"][0])
                y_max = len(mapData["map"])
                
        stage_kill_data = {}
        IGNORED = {"enemy_10082_mpweak", "enemy_10072_mpprhd", "enemy_3009_mpprss"} # square / Hand / EYESOFPRIESTESS
        #stage_data = data["stage"][stage_key]
        stage_enemy_ref = enemy_ref_dict(data["stage"][stage]["enemyDbRefs"])
        # ie. Ep15 za hand spawner
        extra_spawner_int = ""
        enemy_counter : dict[str, Any] = {"KILL" : {}, "Suspect" : {}, "Extra" : {}}
        counter = [0, 0, 0]
        # data prep
        mapData = data["stage"][stage_key]["mapData"]
        stage_height = len(mapData["map"])
        stage_width = len(mapData["map"][0])
        times = 0
        
        if event_type == "ig":
            ig_wave_kill : dict[str, Any] = {"KILL" : {}, "Suspect" : {}, "Extra" : {}, "Weight" : {}}
            ig_wave_key : list[str] = []
        if event_type == "tn":
            tn_kill_lister = []
            tn_wave_kill = {"KILL" : {}, "Suspect" : {}, "Extra" : {}}
            tn_wave = 0
            
        if stage_diff:
            enable_group = []
            disble_group = []
            for rune in data["stage"][stage]["runes"]:
                if rune["difficultyMask"] in [stage_diff, "ALL"]:
                    if rune["key"] == "level_hidden_group_enable":
                        for blackboard in rune["blackboard"]:
                            if blackboard["key"] == "key":
                                enable_group.append(blackboard["valueStr"])
                    elif rune["key"] == "level_hidden_group_disable":
                        for blackboard in rune["blackboard"]:
                            if blackboard["key"] == "key":
                                disble_group.append(blackboard["valueStr"])
            enemies_group = [group for group in enable_group if not group in disble_group]
        else :
            enemies_group = []
        
        isSuiXiang = False
        waves = data["stage"][stage]["waves"]
        for wave in waves:
            times += wave["preDelay"] + wave["postDelay"]
            if event_type == "ig":
                ig_wave = ""
                ig_group = ""
            if event_type == "tn":
                if wave["fragments"][0]["actions"][0]["key"].find("trap_091_brctrl") != -1 and wave["fragments"][0]["actions"][0]["key"].find("empty") != -1:
                    tn_kill_lister.append(tn_wave_kill)
                    tn_wave_kill = {"KILL" : {}, "Suspect" : {}, "Extra" : {}}
                    tn_wave += 1
                    continue
            for fragment in wave["fragments"]:
                times += fragment["preDelay"]
                last_enemy = ""
                for action in fragment["actions"]:
                    routes = data["stage"][stage]["routes"][action["routeIndex"]]
                    
                    if action["hiddenGroup"] and action["hiddenGroup"] not in enemies_group : 
                        #printr(action["hiddenGroup"], enemies_group, action["hiddenGroup"] and action["hiddenGroup"] not in enemies_group, f'{B}Continue')
                        continue
                    
                    if action["key"].split("_")[0] == "enemy" and action["actionType"] == "SPAWN" and action["key"] not in IGNORED:
                        if event_type == "ig":
                            if not (action["randomSpawnGroupKey"] or action["randomSpawnGroupPackKey"]):
                                ig_wave = ""
                                ig_group = ""
                            if not ig_wave and action["randomSpawnGroupKey"] or (action["randomSpawnGroupKey"] and ig_wave and ig_wave != action["randomSpawnGroupKey"]):
                                ig_wave = action["randomSpawnGroupKey"]
                                ig_wave_key.append(ig_wave)
                            if ig_wave and action["randomSpawnGroupPackKey"]:
                                ig_group = f'{ig_wave}-{action["randomSpawnGroupPackKey"]}'
                            elif ig_wave and action["randomSpawnGroupKey"]:
                                ig_group = f'{ig_wave}-NOSUB'
                                ig_wave_key.append(ig_wave)
                            elif not ig_wave and action["randomSpawnGroupPackKey"]:
                                ig_group = f'NOGROUP-{action["randomSpawnGroupPackKey"]}'
                                ig_wave_key.append("NOGROUP")
                        #from Red box // or                                                                                                                                                             // prespawn                             // Sui wisp
                        if mapData["tiles"][mapData["map"][-routes["startPosition"]["row"] - 1][routes["startPosition"]["col"]]]["tileKey"] in ["tile_start", "tile_flystart", "tile_start_cooperate"] or times + action["preDelay"] == 0 or (isSuiXiang and action["key"].find("enemy_1211_msfsui") != -1): 
                            if event_type == "ig":
                                if not (action["randomSpawnGroupKey"] or action["randomSpawnGroupPackKey"]):
                                    ig_wave_kill["KILL"][stage_enemy_ref[action["key"]]] = ig_wave_kill["KILL"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                                    counter[0] += action["count"]
                                if ig_group:
                                    ig_wave_kill["Weight"].setdefault(ig_group, {}).setdefault(stage_enemy_ref[action["key"]], 0)
                                    ig_wave_kill["Weight"][ig_group][stage_enemy_ref[action["key"]]] += action["count"]
                                continue
                            elif event_type == "tn":
                                tn_wave_kill["KILL"][stage_enemy_ref[action["key"]]] = tn_wave_kill["KILL"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                                
                            enemy_counter["KILL"][stage_enemy_ref[action["key"]]] = enemy_counter["KILL"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                            counter[0] += action["count"]
                        #Go to Blue box //                                                                                                                                      #legal spawn movement
                        elif mapData["tiles"][mapData["map"][-routes["endPosition"]["row"] - 1][routes["endPosition"]["col"]]]["tileKey"] in ["tile_end", "tile_end_cooperate"]:# and enemy_motion_search(action["key"]) == routes["motionMode"]:
                            if last_enemy != "enemy_10072_mpprhd":
                                if event_type == "ig":
                                    if not (action["randomSpawnGroupKey"] or action["randomSpawnGroupPackKey"]):
                                        ig_wave_kill["Suspect"][stage_enemy_ref[action["key"]]] = ig_wave_kill["Suspect"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                                        counter[1] += action["count"]
                                    if ig_group:
                                        ig_wave_kill["Weight"].setdefault(ig_group, {}).setdefault(stage_enemy_ref[action["key"]], 0)
                                        ig_wave_kill["Weight"][ig_group][stage_enemy_ref[action["key"]]] += action["count"]
                                    continue
                                elif event_type == "tn":
                                    tn_wave_kill["Suspect"][stage_enemy_ref[action["key"]]] = tn_wave_kill["Suspect"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                                
                                enemy_counter["Suspect"][stage_enemy_ref[action["key"]]] = enemy_counter["Suspect"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                                counter[1] += action["count"]
                            else:
                                if event_type == "ig":
                                    if not (action["randomSpawnGroupKey"] or action["randomSpawnGroupPackKey"]):
                                        ig_wave_kill["Extra"][stage_enemy_ref[action["key"]]] = ig_wave_kill["Extra"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                                        counter[2] += action["count"]
                                    if ig_group:
                                        ig_wave_kill["Weight"].setdefault(ig_group, {}).setdefault(stage_enemy_ref[action["key"]], 0)
                                        ig_wave_kill["Weight"][ig_group][stage_enemy_ref[action["key"]]] += action["count"]
                                    continue
                                elif event_type == "tn":
                                    tn_wave_kill["Extra"][stage_enemy_ref[action["key"]]] = tn_wave_kill["Extra"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                                    
                                enemy_counter["Extra"][stage_enemy_ref[action["key"]]] = enemy_counter["Extra"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                                counter[2] += action["count"]
                        # count all for ig
                        elif event_type == "ig":
                            enemy_counter["Extra"][stage_enemy_ref[action["key"]]] = enemy_counter["Extra"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                            counter[2] += action["count"]
                            
                            if not (action["randomSpawnGroupKey"] or action["randomSpawnGroupPackKey"]):
                                ig_wave_kill["Extra"][stage_enemy_ref[action["key"]]] = ig_wave_kill["Extra"].get(stage_enemy_ref[action["key"]], 0) + action["count"]
                            if ig_group:
                                ig_wave_kill["Weight"].setdefault(ig_group, {}).setdefault(stage_enemy_ref[action["key"]], 0)
                                ig_wave_kill["Weight"][ig_group][stage_enemy_ref[action["key"]]] += action["count"]
                            continue
                        
                    if action["actionType"] == "SPAWN":
                        last_enemy = stage_enemy_ref[action["key"]]
                    if action["key"].find("enemy_1526_sfsui") != -1:
                        isSuiXiang = True
        
        if event_type == "ig":
            ig_kill_lister, ig_kill_wave = ig_wave_lister(ig_wave_kill["Weight"], set(ig_wave_key))
            ig_wave_kill.update({"ig_counter" : ig_kill_lister, "enemy_counter" : ig_kill_wave})
            enemy_counter = ig_wave_kill
        if event_type == "tn":
            tn_kill_lister.append(tn_wave_kill)
            enemy_counter["tn_counter"] = tn_kill_lister
        
        enemy_counter["counter"] = counter

        return enemy_counter
    
    def enemy_trim(enemy_name, e_class = ""):
            trim_result = re.sub(r"(.+?|)'(.+?)'(.+?|)",r'\1"\2"\3', enemy_name)
            if event_type == "tn" and e_class == "BOSS":
                return trim_result.replace(",", "")
            else:
                return trim_result.replace('"', "")
    
    def enemies_lister(def_data : dict) -> dict:
        enemy_classes = ["NORMAL", "ELITE", "BOSS"]
        enemy_list = {k:{} for k in enemy_classes}
        for kill_type in ["KILL", "Suspect"]:
            for enemy in def_data[kill_type]:
                enemy_class = big_data["enemies"][enemy]["data"]["levelType"]
                enemy_list[enemy_class][enemy] = enemy_list[enemy_class].get(enemy, 0) + def_data[kill_type][enemy]
        enemies_output = {k:[] for k in enemy_classes}
        #printr(stage)
        for enemy_class in enemy_classes:
            for enemy in sorted(enemy_list[enemy_class].keys(), key = lambda enemy_key : big_data["enemies"][enemy_key]["handbook"]["enemyIndex"]):
                enemy_code = big_data["enemies"][enemy]["handbook"]["enemyId"]
                enemy_names = DB["json_enemy_handbookEN"]["enemyData"][enemy_code]["name"] if enemy_code in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(enemy, f'{big_data["enemies"][enemy]["handbook"]["name"]}({enemy})')
                enemy_count = enemy_list[enemy_class][enemy]
                if enemy_class == "BOSS":
                    if event_type == "tn":
                        enemies_output[enemy_class].append(enemy_trim(enemy_names, enemy_class))
                    else:
                        enemies_output[enemy_class].append(f'{{{{E|{f'{enemy_trim(enemy_names)}|{enemy_count}' if enemy_count > 1 else enemy_trim(enemy_names)}}}}}')
                else:
                    enemies_output[enemy_class].append(f'{{{{E|{enemy_trim(enemy_names)}|{enemy_count}}}}}')
        return {k:", ".join(v) for k,v in enemies_output.items()}
    
    def ig_enemies_lister(def_data):
        enemy_classes = ["NORMAL", "ELITE", "BOSS"]
        enemy_list = {k:{} for k in enemy_classes}
        for kill_type in ["KILL", "Suspect", "Extra"]:
            for enemy in def_data[kill_type]:
                enemy_class = big_data["enemies"][enemy]["data"]["levelType"]
                enemy_list[enemy_class][enemy] = enemy_list[enemy_class].get(enemy, 0) + def_data[kill_type][enemy]
        for enemy in def_data["ig_counter"]:
            enemy_class = big_data["enemies"][enemy]["data"]["levelType"]
            enemy_kill = enemy_list[enemy_class].get(enemy, 0)
            enemy_list[enemy_class][enemy] = def_data["ig_counter"][enemy][0] + enemy_kill if len(set(def_data["ig_counter"][enemy])) == 1 else f'{def_data["ig_counter"][enemy][0] + enemy_kill}|{def_data["ig_counter"][enemy][1] + enemy_kill}'
        enemies_output = {k:[] for k in enemy_classes}

        for enemy_class in enemy_classes:
            for enemy in sorted(enemy_list[enemy_class].keys(), key = lambda enemy_key : big_data["enemies"][enemy_key]["handbook"]["enemyIndex"]):
                enemy_code = big_data["enemies"][enemy]["handbook"]["enemyId"]
                enemy_names = DB["json_enemy_handbookEN"]["enemyData"][enemy_code]["name"] if enemy_code in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(enemy, f'{big_data["enemies"][enemy]["handbook"]["name"]}({enemy})')
                enemy_count = enemy_list[enemy_class][enemy]
                if enemy_class == "BOSS":
                    enemies_output[enemy_class].append(f'{{{{E|{f'{enemy_trim(enemy_names)}|{enemy_count}' if enemy_count != "1" else enemy_trim(enemy_names)}}}}}')
                else:
                    enemies_output[enemy_class].append(f'{{{{E|{enemy_trim(enemy_names)}|{enemy_count}}}}}')
        return {k:", ".join(v) for k,v in enemies_output.items()}
        
    def tn_enemies_lister(def_data):
        enemy_classes = ["NORMAL", "ELITE", "BOSS"]
        wave_count = 1
        tn_enemies_output = []
        for wave in def_data:
            tn_enemies = enemies_lister(wave)
            for enemy_class in enemy_classes:
                tn_enemies_output.append(f'|{enemy_class.lower()} {wave_count} = {tn_enemies.get(enemy_class, "")}')
            wave_count += 1
        return "\n".join(tn_enemies_output)
    
    def token_lister(def_data : list) -> str:
        token_list = {}
        token_output = []
        # EP14 Controller / Tide Controller / TN Controller / Mouthpiece Doll / Entitative Program (TN Buff) / Icebreaker Games Control / IS mafia control
        token_skip = ["trap_162_lrctrl", "trap_042_tidectrl", "trap_091_brctrl", "trap_054_dancdol", "trap_090_recodr", "trap_179_muctrl", "trap_092_vgctrl"]
        for token in def_data:
            token_code = token["inst"].get("characterKey", token["alias"])
            if token_code in token_skip:
                continue
            else:
                token_list[token_code] = token_list.get(token_code, 0) + 1
        for token in token_list:
            token_name = DB["json_characterEN"][token]["name"] if token in DB["json_characterEN"] else TOKEN_NAMES_TL.get(token, f'{DB["json_character"][token]["name"]}({token})')
            token_output.append(f'{{{{D|{wiki_trim(token_name)}|{token_list[token]}}}}}')
            #printr(token_name)
        return ", ".join(token_output)
            
    def tile_lister(def_data : list) -> list:
        tile_output = []
        tile_skip = ["tile_wall", "tile_road", "tile_floor", "tile_toxichill", "tile_toxicroad", "tile_toxicwall", "tile_toxic", "tile_reed", "tile_reedw", "tile_mire", "tile_yinyang_wall", "tile_yinyang_road", "tile_stairs", "tile_passable_wall", "tile_passable_wall_forbidden", "tile_rcm_operator", "tile_wooden_wall", "tile_empty", "tile_deepsea"]
        tlle_full_skip = ["tile_start", "tile_end", "tile_forbidden", "tile_telin", "tile_telout", "tile_hole", "tile_fence_bound", "tile_flystart", "tile_smog", "tile_start_cooperate", "tile_end_cooperate", "tile_allygoal", "tile_football", "tile_enemygoal", "tile_green", "tile_ristar_road", "tile_ristar_road_forbidden", "tile_grvtybtn"]
        for tile in def_data:
            if (tile["tileKey"] in tile_skip and not tile["blackboard"] and not tile["effects"]) or tile["tileKey"] in tlle_full_skip:
                continue
            tile_data = {tile["tileKey"] : {"blackboard" : tile["blackboard"], "effects" : tile["effects"]}}
            if tile_data not in tile_output:
                tile_output.append(tile_data)
        #if tile_output: printc("tile_output", stage, tile_output)
        return tile_output
    
    def tile_writer(def_data : list) -> str:
        if not def_data: return ""
        tile_result = []
        for tile in def_data:
            #printr(tile)
            tile_id = list(tile.keys())[0]
            match tile_id:
                case "tile_healing":
                    heal = 0
                    for blackboard in tile[tile_id]["blackboard"]:
                        if blackboard["key"] == "HP_RECOVERY_PER_SEC_BY_MAX_HP_RATIO":
                            heal = blackboard["value"]
                    if not heal:
                        printr(f'{R}Medical Rune{RE} key is invalid : {Y}{blackboard["key"]}{RE}')
                        exit()
                    tile_result.append(f'The [[Medical Rune]] restores {heal:{".0%" if len(str(heal).split(".")[-1]) < 2 else ".1%"}} of maximum HP every second to the friendly unit on it.')
                case "tile_bigforce":
                    force = 0
                    for blackboard in tile[tile_id]["blackboard"]:
                        if blackboard["key"] == "base_force_level":
                            force = blackboard["value"]
                    if not force:
                        printr(f'{R}Specialist Tactical Point{RE} key is invalid : {Y}{blackboard["key"]}{RE}')
                        exit()
                    tile_result.append(f'The [[Specialist Tactical Point]] increases the [[shift]] force of the friendly unit on it by {force:.0f} level.')
                case "tile_toxic":
                    if tile[tile_id] == {'blackboard': [{'key': 'dynamic', 'value': 1.0, 'valueStr': None}], 'effects': None}:
                        continue
                    else:
                        printr(f'new {Y}"tile_toxic"{RE} stat just drop\n{tile[tile_id]}')
                        exit()
                case "tile_volspread":
                    damage = 0
                    cd_max = 0
                    cd_min = 0
                    for blackboard in tile[tile_id]["blackboard"]:
                        match blackboard["key"]:
                            case "damage":
                                damage = decimal_format(blackboard["value"])
                            case "cd_min":
                                cd_min = decimal_format(blackboard["value"])
                            case "cd_max":
                                cd_max = decimal_format(blackboard["value"])
                            case _ :
                                printr(f'new {Y}"tile_volspread" : Lava Crack{RE} stat just drop\n{tile[tile_id]}')
                                exit()
                    tile_result.append(f'The [[Lava Crack]]s erupt every {f'{cd_min}-{cd_max} seconds' if cd_min != cd_max else f'{cd_max} seconds'} and deals {damage} True damage to friendly units in the surrounding tiles.')
                case "tile_volcano":
                    damage = 0
                    cd_max = 0
                    cd_min = 0
                    for blackboard in tile[tile_id]["blackboard"]:
                        match blackboard["key"]:
                            case "damage":
                                damage = decimal_format(blackboard["value"])
                            case "cd_min":
                                cd_min = decimal_format(blackboard["value"])
                            case "cd_max":
                                cd_max = decimal_format(blackboard["value"])
                            case _ :
                                printr(f'new {Y}"tile_volcano" : Heat Pump Passage{RE} stat just drop\n{tile[tile_id]}')
                                exit()
                    tile_result.append(f'The [[Heat Pump Passage]] erupt every {f'{cd_min} ~ {cd_max} seconds' if cd_min !=cd_max else f'{cd_max} seconds'} and deals {damage} True damage.')
                case "tile_floor" | "tile_road":
                    default_effect = [
                                        {'blackboard': [{'key': 'tile', 'value': 0.0, 'valueStr': 'landball'}], 'effects': None}
                                    ]
                    if (len(tile[tile_id]["blackboard"]) == 1 and tile[tile_id]["blackboard"][0]["key"] == "gems_type") or tile[tile_id] in default_effect:
                        continue
                    else :
                        printc(f'New tile_floor / tile_road case just drop : {tile[tile_id]}')
                        exit()
                case "tile_defup":
                    if len(tile[tile_id]["blackboard"]) == 1 and tile[tile_id]["blackboard"][0]["key"] == "def":
                        defense = tile[tile_id]["blackboard"][0]["value"]
                        tile_result.append(f'The [[Defense Rune]] increases the DEF of the friendly unit on it by {defense:.0f}.')
                    else :
                        printc(f'New tile_defup case just drop : {tile[tile_id]}')
                        exit()
                case "tile_infection":
                    damage = 0
                    atk = 0
                    aspd = 0
                    duration = 0
                    for blackboard in tile[tile_id]["blackboard"]:
                        match blackboard["key"]:
                            case "damage":
                                damage = blackboard["value"]
                            case "atk":
                                atk = blackboard["value"]
                            case "attack_speed":
                                aspd = blackboard["value"]
                            case "duration":
                                duration = blackboard["value"]
                            case _:
                                printc(f'New {Y}tile_infection{RE} case just drop : {B}{tile[tile_id]}{RE}')
                    if damage and atk and aspd and duration:
                        tile_result.append(f'The [[Active Originium]] effect deals {damage:.0f} True damage every second, increases ATK and ASPD by {atk:{".0%" if len(str(atk).split(".")[-1]) < 2 else ".1%"}} and {aspd:.0f}, respectively, and lasts for {duration:.0f} seconds. ')
                    elif damage and atk and not aspd and duration:
                        tile_result.append(f'The [[Active Originium]] effect deals {damage:.0f} True damage every second, increases ATK by {atk:{".0%" if len(str(atk).split(".")[-1]) < 2 else ".1%"}}, and lasts for {duration:.0f} seconds. ')
                    else:
                        printr(f'Active Originium effect value if {R}not{RE} completed : {R}{stage} {B}{tile}')
                        exit()
                case "tile_yinyang_wall" | "tile_yinyang_road":
                    default_effect = [
                                        [{'key': 'dynamic', 'value': 1.0, 'valueStr': None}, {'key': 'buff_yinyang[same].atk_scale', 'value': 0.6, 'valueStr': None}, {'key': 'buff_yinyang[diff].atk_scale', 'value': 1.4, 'valueStr': None}],
                                        [{'key': 'dynamic', 'value': 0.0, 'valueStr': None}, {'key': 'buff_yinyang[same].atk_scale', 'value': 0.6, 'valueStr': None}, {'key': 'buff_yinyang[diff].atk_scale', 'value': 1.4, 'valueStr': None}]
                                    ]
                    if tile[tile_id]["blackboard"] in default_effect and not tile[tile_id]["effects"]:
                        continue
                    else :
                        printc(f'New {Y}tile_yinyang{RE} case just drop : {B}{tile[tile_id]}{RE}')
                case "tile_defbreak":
                    if tile[tile_id] == {'blackboard': [{'key': 'def', 'value': 0.5, 'valueStr': None}], 'effects': None}:
                        continue
                    else:
                        printc(f'New {Y}tile_defbreak{RE} case just drop : {B}{tile[tile_id]}{RE}')
                case "tile_creep" | "tile_creepf":
                    default_effect = [
                                        [{'key': 'mode', 'value': 1.0, 'valueStr': None}],
                                        [{'key': 'mode', 'value': 0.0, 'valueStr': None}]
                                    ]
                    if tile[tile_id]["blackboard"] in default_effect and not tile[tile_id]["effects"]:
                        continue
                    else :
                        printc(f'New {Y}tile_creep{RE} case just drop : {B}{tile[tile_id]}{RE}')
                case _ :
                    printr(f'new Terrain to add : {Y}{tile_id}\n\t{G}{tile[tile_id]["blackboard"]}\n\t{B}{tile[tile_id]["effects"]}{RE}')
                    exit()
        
        if tile_result:
            #printr(f'{B}tile_writer {G}{stage} {Y}{tile_result}{RE}')
            if len(tile_result) > 1:
                return f'\n*{"\n*".join(tile_result)}'
            else:
                return f'\n{"\n".join(tile_result)}'
        else:
            return ""
    
    def addendum_writer(runes = [], buffs = [], DP = 1, diff = "", head = "", foot = "", ig_ctrl = {}):
        def ig_wave_addendum_writer(Blackboards):
            ig_writer = []
            ig_writer.append(f'\n<!-- {"|".join([f'{bb["key"]} : {bb["valueStr"]}' if bb["valueStr"] else f'{bb["key"]} : {bb["value"]}' for bb in Blackboards])} -->')
            new_Blackboards = {bb["key"]:bb["valueStr"] if bb["valueStr"] else bb["value"] for bb in Blackboards}
            match new_Blackboards["ability_name"] :
                case "car":
                    ig_writer.append(f'Push $1 in {decimal_format(new_Blackboards["time_x"])} seconds{f' with {decimal_format(new_Blackboards["rest_time"])} seconds break time' if new_Blackboards.get("rest_time", 0) else "" }')
                case "kill":
                    ig_writer.append(f'Defeat enemies in {decimal_format(new_Blackboards["time_x"])} seconds{f' with {decimal_format(new_Blackboards["rest_time"])} seconds break time' if new_Blackboards.get("rest_time", 0) else "" }')
                case "protect":
                    ig_writer.append(f'Rescue in {decimal_format(new_Blackboards["time_x"])} seconds{f' with {decimal_format(new_Blackboards["rest_time"])} seconds break time' if new_Blackboards.get("rest_time", 0) else "" }')
                case "survive":
                    ig_writer.append(f'Survive for {decimal_format(new_Blackboards["time_x1"])} seconds{f' with {decimal_format(new_Blackboards["rest_time"])} seconds break time' if new_Blackboards.get("rest_time", 0) else "" }')
                case "target" | "boss":
                    ig_writer.append(f'Defeat target in {decimal_format(new_Blackboards["time_x"])} seconds{f' with {decimal_format(new_Blackboards["rest_time"])} seconds break time' if new_Blackboards.get("rest_time", 0) else "" }')
                case "tower":
                    ig_writer.append(f'Capture Gramophones in {decimal_format(new_Blackboards["time_x"])} seconds{f' with {decimal_format(new_Blackboards["rest_time"])} seconds break time' if new_Blackboards.get("rest_time", 0) else "" }')
                case _:
                    printc(f'{Y}New IG Wave case{RE} just drop !!! : ', new_Blackboards)
                    exit()
            return "\n".join(ig_writer)
        norm_env = [
                        {'key': 'env_017_act35side', 'attack_speed': -60.0, 'max_hp': 0.1, 'atk': 0.1},
                        {'key': 'env_005_mainline12_sightSystem'},
                        {'key': 'env_012_act33side', 'stun_duration': 10.0},
                    ]

        env_name = [
                        "env_017_act35side", "env_010_act31side_pollute"
                    ]
        buff_writer = []
        if buffs:
            for buff in buffs:
                if buff["prefabKey"] in enemy_buffs:
                    continue
                elif buff["prefabKey"] in non_enemy_buffs:
                    temp = {k:v for k,v in buff.items()}
                    #printr(temp["blackboard"])
                    match buff["prefabKey"]:
                        case "periodic_damage":
                            damage = temp["blackboard"].pop("damage")
                            interval = temp["blackboard"].pop("interval")
                            if temp["blackboard"]:
                                printc(f'There new blackboard key in {Y}{buff["prefabKey"]}{RE} : {B}{temp["blackboard"]}{RE}')
                            else:
                                buff_writer.append(f'\nThe [[Poison Haze]] deals {damage:.0f} True damage every {decimal_format(interval)} seconds to all friendly units on the map.')
                        case "cooperate_fortress_global_buff":
                            rest_time       = decimal_format(temp["blackboard"].pop("rest_time"))
                            wave_time       = decimal_format(temp["blackboard"].pop("wave_time"))
                            life_point      = decimal_format(temp["blackboard"].pop("life_point"))
                            rest_add        = decimal_format(temp["blackboard"].pop("rest_add"))
                            wave_time_last  = decimal_format(temp["blackboard"].pop("wave_time_last"))
                            if temp["blackboard"]:
                                printc(f'There new blackboard key in {Y}{buff["prefabKey"]}{RE} : {B}{temp["blackboard"]}{RE}')
                            else:
                                buff_writer.append(f'\nSurvive for {wave_time} seconds and have {rest_time} seconds break time\nOn break, recover up to {life_point} life points and increase next break time by {rest_add} seconds\nMonument of Trial last for {wave_time_last} seconds')
                        case "character_in_magiccircuit_env":
                            sp_recover_ratio_minus  = temp["blackboard"].pop("sp_recover_ratio")
                            sp_recover_ratio_add    = temp["blackboard"].pop("character_in_magiccircuit[normal].sp_recover_ratio")
                            if temp["blackboard"]:
                                printc(f'There new blackboard key in {Y}{buff["prefabKey"]}{RE} : {B}{temp["blackboard"]}{RE}')
                                exit()
                            else:
                                buff_writer.append(f'\n*Waste Energy Interference reduces the automatic SP generation rate of friendly units by {abs(sp_recover_ratio_minus):%}.\n*Friendly units linked with [[Realigned Flux]]es have their automatic SP generation rate increased by {abs(sp_recover_ratio_add):%}.')
                        case _:
                            printc(f'There new case in addendum Towns : {buff["prefabKey"]}')
                else:
                    printc(f'New buff in town !!! {buff["prefabKey"]}')
        
        addendum = f'{"\n".join(buff_writer)}\n{head}'
        if DP != 1: addendum += f'DP regeneration rate is reduced by 100%. '
        rune_writer = []
        for rune in runes:
            temp = {k:v for k,v in rune.items()}
            if (rune["key"] in enemy_rune and rune["key"] not in both_rune) or rune["key"] in skip_rune:
                continue
            if rune["key"] not in non_enemy_rune:
                printc(f'{Y}{rune["key"]}{RE} is {R}not{RE} in {G}non_enemy_rune{RE} : {B}{non_enemy_rune}{RE}')
                
            if rune["difficultyMask"] == "ALL" or rune["difficultyMask"] == diff:
                match rune["key"]:
                    case "env_system_new":
                        if rune["blackboard"] in norm_env or rune["blackboard"].get("key","") in env_name:
                            continue
                        else :
                            printc(f'New Environment just drop : {rune["blackboard"]}')
                    case "global_cost_recovery":
                            scale = temp["blackboard"].pop("scale")
                            if temp["blackboard"]:
                                printc(f'There new blackboard key in {Y}{rune["prefabKey"]}{RE} : {B}{temp["blackboard"]}{RE}')
                            else:
                                rune_writer.append(f'\n(Possible Key Typo) The automatic DP generation rate is {"reduced" if scale > 1 else "increased"} to 1 DP every {decimal_format(scale)} seconds.')
                    case "global_cost_recovery_mul":
                            scale = temp["blackboard"].pop("scale")
                            if temp["blackboard"]:
                                printc(f'There new blackboard key in {Y}{rune["prefabKey"]}{RE} : {B}{temp["blackboard"]}{RE}')
                            else:
                                rune_writer.append(f'\nThe automatic DP generation rate is {"reduced" if scale > 1 else "increased"} to 1 DP every {decimal_format(scale)} seconds.')
                    case "global_lifepoint":
                        # global_lifepoint()
                        continue
                    case "map_tile_blackb_assign":
                        default_effect = [
                                            {'tile': 'tile_reed|tile_reedf|tile_reedw', 'ignite_duration': 15.0, 'extinct_duration': 20.0, 'cooldown_duration': 5.0, 'damage': 40.0, 'ep_damage': 40.0},
                                        ]
                        if rune["blackboard"] in default_effect:
                            continue
                        else :
                            printr(f'{Y}New {rune["key"]} just drop : {B}{rune["blackboard"]}')
                    case "env_gbuff_new_with_verify":
                        if rune["blackboard"].get("key", "") == "cooperate_enemy_side_shared": # enemy
                            continue
                        else :
                            printr(f'{Y}New {rune["key"]} just drop : {B}{rune["blackboard"]}')
                    case "env_gbuff_new":
                        if rune["blackboard"].get("key", "") == "cooperate_get_branch":
                            continue
                        elif rune["blackboard"].get("key", "") == "sp_recovery_reduction":
                            new_sp = 1 + rune["blackboard"].get("sp_recovery_per_sec")
                            rune_writer.append(f'\nThe SP generation rate is {"reduced" if new_sp < 1 else "increased"} to {decimal_format(new_sp)} SP per second.')
                        else :
                            printr(f'{Y}New {rune["key"]} just drop : {B}{rune["blackboard"]}')
                    case "char_attribute_add":
                        char_add : str = rune["blackboard"].pop("char")
                        char_add_name = join_and([DB["json_characterEN"][char]["name"] if char in DB["json_characterEN"] else DB["json_character"][char]["appellation"]  for char in char_add.split("|")])
                        char_all_attribute = []
                        for char_attribute in rune["blackboard"].keys():
                            match char_attribute:
                                case "hp_recovery_per_sec":
                                    char_all_attribute.append(f'recover {decimal_format(rune["blackboard"][char_attribute])} HP every second')
                                case "max_hp":
                                    char_all_attribute.append(f'Max HP increased by {decimal_format(rune["blackboard"][char_attribute])}')
                                case _:
                                    printr(rune["blackboard"])
                                    exit()
                        rune_writer.append(f'\nAll {char_add_name} have {join_and(char_all_attribute)}.')
                    case "cbuff_max_cost":
                        max_cost        = rune["blackboard"].pop("max_cost")
                        max_cost_ceil   = rune["blackboard"].pop("max_cost_ceil")
                        if rune["blackboard"]:
                            printr(f'{Y}New {rune["key"]} just drop : {B}{rune["blackboard"]}')
                            exit()
                        rune_writer.append(f'\nThe [[DP]] cap is reduced to {decimal_format(max_cost)}. ')
                    case "char_skill_cd_mul":
                        char_skill_cd   = rune["blackboard"].pop("scale")
                        if rune["blackboard"]:
                            printr(f'{Y}New {rune["key"]} bb just drop : {B}{rune["blackboard"]}')
                            exit()
                        rune_writer.append(f'\nAll skill cost reduce by {1 - char_skill_cd:%}')
                    case "char_skill_blackb_mul":
                        char_add : str = rune["blackboard"].pop("char").split("#")[0]
                        hp_max = rune["blackboard"].pop("hp_max") if "hp_max" in rune["blackboard"].keys() else ""
                        hp_x1 = rune["blackboard"].pop("hp_x1") if "hp_x1" in rune["blackboard"].keys() else ""
                        if char_add in ["trap_179_mpctrl"]:
                            char_add_name = "<!--Multi-player controller-->"
                            rune_writer.append(f'\n<!--Multi-player controller--> have hp_x1 : {hp_x1} change by hp_max : {hp_max}')
                        else :
                            char_add_name = join_and([DB["json_characterEN"][char]["name"] if char in DB["json_characterEN"] else DB["json_character"][char]["appellation"]  for char in char_add.split("|")])
                        if rune["blackboard"]:
                            printr(f'{Y}New {rune["key"]} bb just drop : {B}{rune["blackboard"]}')
                            exit()
                    case "char_cost_add":
                        char_add : str = rune["blackboard"].pop("char_id")
                        char_add_name = join_and([DB["json_characterEN"][char]["name"] if char in DB["json_characterEN"] else DB["json_character"][char]["appellation"]  for char in char_add.split("|")])
                        cost_add = rune["blackboard"].pop("value")
                        if char_add and cost_add:
                            rune_writer.append(f'\n{char_add_name} DP cost {"increased" if cost_add > 0 else "reduced"} by {decimal_format(abs(cost_add))}')
                        if rune["blackboard"]:
                            printr(f'{Y}New {rune["key"]} bb just drop : {B}{rune["blackboard"]}')
                            exit()
                    case "char_blockcnt_add":
                        blockcnt_add = rune["blackboard"].pop("value")
                        if blockcnt_add:
                            rune_writer.append(f'\nAll allied units Block Count {"increased" if blockcnt_add > 0 else "reduced"} by {decimal_format(abs(blockcnt_add))}')
                        if rune["blackboard"]:
                            printr(f'{Y}New {rune["key"]} bb just drop : {B}{rune["blackboard"]}')
                            exit()
                    case _:
                        printc(f'New case just drop :', {rune["key"]}, rune["blackboard"])
                        exit()
        
        if event_type == "ig" and ig_ctrl:
            for token in ig_ctrl:
                if (token["alias"] and token["alias"].startswith("trap_179_muctrl")) or (token["inst"] and token["inst"]["characterKey"] == "trap_179_muctrl"):
                    rune_writer.append(ig_wave_addendum_writer(token["overrideSkillBlackboard"]))
        addendum += f'{"\n".join(rune_writer)}\n{foot}'
        return addendum.replace("\n\n","\n").replace(" ", " ")

    def eaddendum_lister(stage_key : str):
        eaddendum = []
        # Individual Enemy
        enemies_data_key = ["applyWay", "motion", "enemyTags", "lifePointReduce", "levelType", "rangeRadius", "numOfExtraDrops", "notCountInTotal"]
        #printr(stage)
        for enemy_ref in big_data["stage"][stage_key]["enemyDbRefs"]:
            enemy_id = enemy_ref["id"]
            enemy_lv = enemy_ref["level"]
            enemy_overwrittenData = {}
            if enemy_ref["overwrittenData"]:
                for key in enemy_ref["overwrittenData"]:
                    #printr(key, enemy_id)
                    if key == "attributes":
                        for attribute in enemy_ref["overwrittenData"][key]:
                            if enemy_ref["overwrittenData"][key][attribute]["m_defined"] and (enemy_ref["overwrittenData"][key][attribute]["m_value"] != big_data["enemies"][enemy_id]["lv"][enemy_lv][attribute]):
                                enemy_overwrittenData[attribute] = enemy_ref["overwrittenData"][key][attribute]["m_value"]
                    elif key == "prefabKey" and enemy_ref["overwrittenData"][key]["m_defined"]:
                        enemy_id = enemy_ref["overwrittenData"][key]["m_value"]
                    elif key in ["talentBlackboard", "skills", "spData"]:
                        if enemy_ref["overwrittenData"][key] and enemy_ref["overwrittenData"][key] != big_data["enemies"][enemy_id]["lv"][enemy_lv][key]:
                            match key:
                                case "talentBlackboard":
                                    blackboard_list = []
                                    dupe_value = False
                                    for blackboard in enemy_ref["overwrittenData"][key]:
                                        if big_data["enemies"][enemy_id]["lv"][enemy_lv][key]:
                                            for talent_blackboard in big_data["enemies"][enemy_id]["lv"][enemy_lv][key]:
                                                if blackboard["key"] != talent_blackboard["key"]:
                                                    continue
                                                else:
                                                    if blackboard["value"] == talent_blackboard["value"] and blackboard["valueStr"] == talent_blackboard["valueStr"]:
                                                        dupe_value = True
                                                        break
                                                    elif blackboard["value"] != talent_blackboard["value"]:
                                                        blackboard_list.append(blackboard)
                                                        break
                                                    elif blackboard["valueStr"] != talent_blackboard["valueStr"]:
                                                        blackboard_list.append(blackboard)
                                                        break
                                                    printr(f'ermmmmm blackboard not new or wat plz check this\n{G}{blackboard}\n{B}{talent_blackboard}{RE}')
                                        if not blackboard_list and not dupe_value:
                                            match blackboard["key"]:
                                                case "loot.token_key":
                                                    blackboard_list.append(blackboard)
                                                    continue
                                                case "loot.cnt":
                                                    blackboard_list.append(blackboard)
                                                    continue
                                                case _ :
                                                    printr(f'new blackboard key {Y}{blackboard["key"]}{RE} for : {Y}{enemy_id}{R}({stage_key}){RE}')
                                                    exit()
                                    if blackboard_list:
                                        enemy_overwrittenData[key] = blackboard_list
                                case "skills":
                                    skills_list = {}
                                    for skill_key in enemy_ref["overwrittenData"][key]:
                                        if big_data["enemies"][enemy_id]["lv"][enemy_lv][key]:
                                            for skill in big_data["enemies"][enemy_id]["lv"][enemy_lv][key]:
                                                if skill["prefabKey"] != skill_key["prefabKey"]:
                                                    continue
                                                if skill == skill_key:
                                                    break
                                                else:
                                                    for s_key in skill_key:
                                                        if s_key == "blackboard":
                                                            for bb_key in skill_key[s_key]:
                                                                for bb in skill[s_key]:
                                                                    if bb_key["key"] != bb["key"]:
                                                                        continue
                                                                    elif bb_key == bb:
                                                                        break
                                                                    else:
                                                                        skills_list.update({f'Skill-BB-{bb_key["key"]}':bb_key["valueStr"] if bb_key["valueStr"] else bb_key["value"]})
                                                        else:
                                                            if skill_key[s_key] != skill[s_key]:
                                                                skills_list.update({s_key:skill_key[s_key]})
                                case "spData":
                                    spData_list = {}
                                    sp_big_data = big_data["enemies"][enemy_id]["lv"][0][key]
                                    if not sp_big_data or (enemy_ref["overwrittenData"][key] and enemy_ref["overwrittenData"][key] == {'spType': 'INCREASE_WITH_TIME', 'maxSp': 0, 'initSp': 0, 'increment': 1.0}):
                                        continue
                                    else:
                                        printc(f'Update other case soon !!! {Y}spData{RE}', enemy_id, enemy_ref["overwrittenData"][key], big_data["enemies"][enemy_id]["lv"][enemy_lv][key], sp_big_data)
                                        exit()
                                case _:
                                    printr(f'Update other case soon !!!')
                            
                    elif key not in ["name", "description", "viewRadius"]:
                        if enemy_ref["overwrittenData"][key]["m_defined"] and not falsy_compare(enemy_ref["overwrittenData"][key]["m_value"], (big_data["enemies"][enemy_id]["lv"][enemy_lv][key] if key not in enemies_data_key else big_data["enemies"][enemy_id]["data"][key])):
                            #printc(key, (data["enemies"][enemy_id]["lv"][enemy_lv][key] if key not in enemies_data_key else data["enemies"][enemy_id]["data"][key]), enemy_ref["overwrittenData"][key]["m_value"], (data["enemies"][enemy_id]["lv"][enemy_lv][key] if key not in enemies_data_key else data["enemies"][enemy_id]["data"][key]) == enemy_ref["overwrittenData"][key]["m_value"])
                            enemy_overwrittenData[key] = enemy_ref["overwrittenData"][key]["m_value"]
            if enemy_overwrittenData: 
                eaddendum.append({enemy_id:enemy_overwrittenData})
        
        #if eaddendum: printc("eaddendum", stage, eaddendum)
        return eaddendum
    
    def eaddendum_writer(eaddendum, runes = [], buffs = [], enemyDbRefs = {}, diff = "", mul = False):
        def eaddendum_stat_writer(key, value):
            match key:
                case "rangeRadius":
                    return f'an attack range of {decimal_format(value)} tiles'
                case "lifePointReduce":
                    if value == 0:
                        return "Does not deduct [[Life Point|Life Points]]"
                    elif value < 0:
                        printr(f'There {Y}Negative value{RE} case to investigate {R}({stage}, {Y}{enemy_code}{R}){RE}')
                    else:
                        return f'deduct {int(value)} [[Life Point|Life Points]] upon entering a [[Protection Objective]]'
                case "massLevel":
                    return f'weight {value}'
                case "enemyTags":
                    return f'new case enemyTags -> {value}'
                case "enemy_exclude":
                    return f'Excluding -> {enemy_name_search(value.split("|"))}'
                case _ :
                    try:
                        return f'{decimal_format(value)} {eaddendum_dict[key]}'
                    except:
                        print(value, eaddendum_dict[key])
        
        def enemy_name_search(key : str | list) -> str:
            def searching(enemy):
                return big_data["enemies"][enemy]["data"]["name"] if enemy in big_data["enemies"].keys() else enemyDbRefs[enemy]["overwrittenData"]["name"]["m_value"]
            
            if isinstance(key, str):
                return searching(key)
            elif isinstance(key, list):
                return join_and(sorted([searching(enemy) for enemy in key], key = lambda x : x.replace("'", "")))
        
        #attribute_key = ['maxHp', 'atk', 'def', 'magicResistance', 'moveSpeed', 'attackSpeed', 'baseAttackTime', 'respawnTime', 'hpRecoveryPerSec', 'spRecoveryPerSec', 'massLevel', 'baseForceLevel', 'tauntLevel', 'epDamageResistance', 'epResistance', 'damageHitratePhysical', 'damageHitrateMagical', 'epBreakRecoverSpeed', 'stunImmune', 'silenceImmune', 'sleepImmune', 'frozenImmune', 'levitateImmune', 'disarmedCombatImmune', 'fearedImmune', 'palsyImmune', 'attractImmune']
        eaddendum_dict = {"max_hp": "HP", "maxHp": "HP", "atk": "ATK", "def": "DEF", "magicResistance": "RES", "moveSpeed": "MSPD", "move_speed": "MSPD", "rangeRadius": "Attack Range", "lifePointReduce" : "Life Points", "massLevel": "weight", "baseAttackTime": "BAT", "enemyTags" : "enemyTags"}#, "enemy_exclude" : "Excluding"}
        eaddendum_skip = ["name", "description", "spRecoveryPerSec", "talentBlackboard", "spData", "skills"]
        eaddendum_hard_skip = ["name", "description"]
        
        buff_writer = []        
        if buffs:
            for buff in buffs:
                if buff["prefabKey"] in non_enemy_buffs:
                    continue
                elif buff["prefabKey"] in enemy_buffs:
                    temp = {k:v for k,v in buff.items()}
                    match buff["prefabKey"]:
                        case "cooperate_enemy_catch_up":
                            default_effect = [
                                                {'max_hp': 0.0, 'atk': 0.0, 'move_speed': 0.0, 'attack_speed': 0.0}
                                            ]
                            if buff["blackboard"] in default_effect or sum(list(buff["blackboard"].values())) == 0:
                                continue
                            elif buff["blackboard"]:
                                stat_key = []
                                stat_value = []
                                for key in buff["blackboard"]:
                                    if buff["blackboard"][key]:
                                        stat_key.append(key)
                                        stat_value.append(buff["blackboard"][key])
                                if stat_key and stat_value:
                                    buff_writer.append(f'When enemy score behind, all enemies have {join_and([eaddendum_dict[key] for key in stat_key])} increased by {join_and([f'{value:%}' for value in stat_value])} per score different respectively')
                                else :
                                    continue
                            else :
                                printc(f'There new bb in {buff["prefabKey"]} : ', buff["blackboard"], buff)
                                exit()
                        case "cooperate_enemy_after_attack_harder":
                            default_effect = [
                                                {'atk': 0.0}
                                            ]
                            if buff["blackboard"] in default_effect:
                                continue
                            else :
                                printc(f'There new bb in {buff["prefabKey"]} : ', buff["blackboard"], buff)
                                exit()
                        case _:
                            printc("There new case in eaddendum buff Towns : ", buff["prefabKey"], buff)
                            exit()
                else:
                    printc(f'New buff in town !!! {buff["prefabKey"]}')
                    
        eaddendum_result = buff_writer
        if runes:
            for rune in runes:
                if (rune["key"] in non_enemy_rune and rune["key"] not in both_rune) or rune["key"] in skip_rune:
                    continue
                if rune["key"] not in enemy_rune:
                    printc(f'{Y}{rune["key"]}{RE} is {R}not{RE} in {G}enemy_rune{RE} : {R}{stage} {B}{enemy_rune}{RE}')
                if rune["difficultyMask"] == "ALL" or rune["difficultyMask"] == diff:
                    #printr(stage, "im here")
                    match rune["key"]:
                        case "char_attribute_mul":
                            temp_stat = []
                            temp_value = []
                            char_name = ""
                            for key in rune["blackboard"]:
                                value = rune["blackboard"][key]
                                if key in eaddendum_skip:
                                    continue
                                elif key == "char" and value.find("enemy") != -1:
                                    char_name = enemy_name_search(value)
                                elif key == "char" and value.find("enemy") == -1:
                                    char_name = DB["json_characterEN"][value]["name"] if value in DB["json_characterEN"] else TOKEN_NAMES_TL.get(value, DB["json_character"][value]["name"])
                                elif key in eaddendum_dict.keys():
                                    temp_stat.append(eaddendum_dict[key])
                                    temp_value.append(f'{value - 1:.0%}')
                                else:
                                    printr(f'{Y}{key}{RE} is {R}not{RE} in {Y}eaddendum_dict !!! {R}({stage}){RE}')
                                    exit()
                            if temp_stat and temp_value:
                                eaddendum_result.append(f'\n{char_name} have {join_and(temp_stat)} increased by {join_and(set(temp_value) if len(set(temp_value)) == 1 else temp_value)}.')
                        case "enemy_attribute_mul":
                            temp_stat = []
                            temp_value = []
                            temp_exclude = []
                            all_enemy = []
                            enemy_name = ""
                            for key in rune["blackboard"]:
                                value = rune["blackboard"][key]
                                if key in eaddendum_skip or value == 0:
                                    continue
                                elif key in eaddendum_dict.keys():
                                    temp_stat.append(eaddendum_dict[key])
                                    if isinstance(value, str):
                                        temp_value.append(join_and(value.split("|")))
                                    else :
                                        temp_value.append(f'{value - 1:.0%}')
                                elif key == "enemy":
                                    all_enemy = value.split("|")
                                    enemy_name = join_and([big_data["enemies"][enemy]["data"]["name"] if enemy in big_data["enemies"].keys() else enemyDbRefs[enemy]["overwrittenData"]["name"]["m_value"] for enemy in all_enemy])
                                elif key == "enemy_exclude":
                                    temp_exclude.append(eaddendum_stat_writer(key, value))
                                else:
                                    printr(f'{Y}{key}{RE} is {R}not{RE} in {Y}eaddendum_dict !!! {R}({stage}){RE}')
                                    #exit()
                            if temp_stat and temp_value:
                                eaddendum_result.append(f'\n{enemy_name if enemy_name else "All enemies"} have their {join_and(temp_stat)} increased by {join_and(set(temp_value) if len(set(temp_value)) == 1 else temp_value)}{f' ({join_and(temp_exclude)})' if temp_exclude else ""}.')
                        case "level_enemy_replace":
                            enemy_base = ""
                            enemy_replace = "" 
                            for key in rune["blackboard"]:
                                if key == "key":
                                    base_enemy = rune["blackboard"][key].split("|")
                                    enemy_base = join_and([big_data["enemies"][enemy]["data"]["name"] for enemy in base_enemy])
                                elif key == "value":
                                    replace_enemy = rune["blackboard"][key].split("|")
                                    enemy_replace = join_and([big_data["enemies"][enemy]["data"]["name"] if enemy in big_data["enemies"].keys() else enemyDbRefs[enemy]["overwrittenData"]["name"]["m_value"] for enemy in replace_enemy])
                                else :
                                    printr(f'new key for {Y}level_enemy_replace{RE} just drop : {B}{key}{R} ({stage}){RE}')
                                    exit()
                            if enemy_base and enemy_replace:
                                eaddendum_result.append(f'\nAll {enemy_base} are replaced with {enemy_replace}.')
                        case "env_gbuff_new_with_verify":
                            if rune["blackboard"].get("key", "") == "cooperate_enemy_side_shared":
                                share_enemy_id = rune["blackboard"]["enemy"].split("|")
                                share_enemy = join_and([DB["json_enemy_handbookEN"]["enemyData"][enemy]["name"] if enemy in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(enemy, f'{big_data["enemies"][enemy]["data"]["name"]}({enemy})') for enemy in share_enemy_id if not re.match(r'enemy_.+?enemy_.+?', enemy)])
                                eaddendum_result.append(f'\n{share_enemy} will deduct both players [[Life Point|Life Points]] upon entering a [[Protection Objective]].')
                            else :
                                printr(f'{Y}New env_gbuff_new_with_verify just drop : {B}{rune["blackboard"]}')
                        case "env_gbuff_new":
                            if rune["blackboard"].get("key", "") in ["cooperate_get_branch", "sp_recovery_reduction"]: # non enemy
                                continue
                            printr(rune["blackboard"])
                            exit()
                        case "cooperate_enemy_side_shared":
                            share_enemy_id = rune["blackboard"].pop("enemy").split("|")
                            share_enemy = join_and([DB["json_enemy_handbookEN"]["enemyData"][enemy]["name"] if enemy in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(enemy, f'{big_data["enemies"][enemy]["data"]["name"]}({enemy})') for enemy in share_enemy_id if not re.match(r'enemy_.+?enemy_.+?', enemy)])
                            eaddendum_result.append(f'\n{share_enemy} will deduct both players [[Life Point|Life Points]] upon entering a [[Protection Objective]].')
                            if rune["blackboard"] :
                                printr(f'New {Y}{rune["key"]}{RE} key just drop : {B}{rune["blackboard"]}')
                                exit()
                        case "level_hidden_group_enable" | "level_hidden_group_disable":
                            continue
                        case "enemy_talent_blackb_mul":
                            match sorted(list(rune["blackboard"].keys())):
                                case ["enemy", "searchBall.range_radius"] :
                                    enemy_id = rune["blackboard"].pop("enemy").split("|")
                                    enemy_name = join_and([DB["json_enemy_handbookEN"]["enemyData"][enemy]["name"] if enemy in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(enemy, f'{big_data["enemies"][enemy]["data"]["name"]}({enemy})') for enemy in enemy_id if not re.match(r'enemy_.+?enemy_.+?', enemy)])
                                    searchBall = rune["blackboard"].pop("searchBall.range_radius")
                                    if searchBall :
                                        eaddendum_result.append(f'\n{enemy_name} have Football search radius to {searchBall} tiles.')
                                        continue
                                case ["football.slapshot_force"]:
                                    slapshot_force = rune["blackboard"].pop("football.slapshot_force")
                                    multi_force = 1 - slapshot_force
                                    if slapshot_force :
                                        eaddendum_result.append(f'\nAll enemies have Football shot force increased by {multi_force:%}.')
                                        continue
                                case ["enemy", "football.slapshot_force"]:
                                    enemy_id = rune["blackboard"].pop("enemy").split("|")
                                    enemy_name = join_and([DB["json_enemy_handbookEN"]["enemyData"][enemy]["name"] if enemy in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(enemy, f'{big_data["enemies"][enemy]["data"]["name"]}({enemy})') for enemy in enemy_id if not re.match(r'enemy_.+?enemy_.+?', enemy)])
                                    slapshot_force = rune["blackboard"].pop("football.slapshot_force")
                                    multi_force = 1 - slapshot_force
                                    if slapshot_force :
                                        eaddendum_result.append(f'\n{enemy_name} have Football shot force increased by {multi_force:%}.')
                                        continue
                                case ["Reborn.duration"]:
                                    Reborn_duration = rune["blackboard"].pop("Reborn.duration")
                                    if Reborn_duration :
                                        eaddendum_result.append(f'\nReduce all enemies break time by {1 - Reborn_duration:%}.')
                                        continue
                                case _ :
                                    printr(f'New {Y}{rune["key"]}{RE} key just drop : {B}{rune["blackboard"]}')
                                    exit()
                        case _:
                            printc(f'{Y}{stage}{RE} New enemy rune key just drop : {B}{rune["key"]}{RE}', rune)
                            exit()
                #else: printr(f'New Difficulty to add : {Y}{rune["difficultyMask"]}{RE}')
        
        # Individual enemies
        for enemy in eaddendum:
            eaddendum_parse = []
            eaddendum_exclude = []
            enemy_key = list(enemy.keys())[0]
            enemy_code = big_data["enemies"][enemy_key]["handbook"]["enemyId"]
            enemy_name = DB["json_enemy_handbookEN"]["enemyData"][enemy_code]["name"] if enemy_code in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(enemy_key, f'{big_data["enemies"][enemy_key]["data"]["name"]}({enemy_key})')
            for ref_stat in list(enemy.values()):
                for k,v in ref_stat.items():
                    if k in eaddendum_skip or (k == "attackSpeed" and v == 100) or k == "rangeRadius" and v in [0, -1] or (k == "enemyTags" and v == big_data["enemies"][enemy_key]["data"]["enemyTags"]):
                        continue
                    if k not in eaddendum_dict:
                        printr(f'{Y}{k}{RE} is {R}not{RE} in {G}eaddendum_dict !!!{RE} {R}({stage}, {Y}{enemy_key}{R}){RE}')
                        exit()
                    else:
                        eaddendum_parse.append(eaddendum_stat_writer(k, v))
                if eaddendum_parse:
                    eaddendum_result.append(f'\n*{enemy_name} have {join_and(eaddendum_parse)}.')
        return "".join(eaddendum_result)
    
    def rune_lister(def_data : list) -> list:
        rune_list = []
        for rune in def_data:
            temp = {k:v for k,v in rune.items()}
            temp["blackboard"] = {}
            for blackboard in rune["blackboard"]:
                if blackboard["valueStr"] and blackboard["valueStr"] in skip_rune:
                    temp["blackboard"] = {}
                    break
                else :
                    temp["blackboard"].update({blackboard["key"]:(blackboard["valueStr"] if blackboard["valueStr"] else blackboard["value"])})
            if temp["blackboard"]:
                rune_list.append(temp)
        
        new_rune_list = [new_rune for new_rune in[rune["key"] for rune in rune_list] if new_rune not in (enemy_rune + non_enemy_rune + skip_rune)]
        if new_rune_list != []:
            printr(f'{Y}{stage}{RE} There {R}new rune(s){RE} in town !!! : {B}{new_rune_list}{RE}')
            exit()
        return rune_list
    
    def global_buff_lister(def_data : list) -> list:
        global_buff = []
        if sorted([buff["prefabKey"] for buff in def_data]) != sorted(list(set([buff["prefabKey"] for buff in def_data]))):
            printc(sorted([buff["prefabKey"] for buff in def_data]), sorted(list(set([buff["prefabKey"] for buff in def_data]))), sorted([buff["prefabKey"] for buff in def_data]) != sorted(list(set([buff["prefabKey"] for buff in def_data]))))
            printc(f'There dupe buff key need fix {[buff["prefabKey"] for buff in def_data]}')
            exit()
        for buff in def_data:
            if buff["prefabKey"] in skip_buffs:
                continue
            elif buff["prefabKey"] not in (non_enemy_buffs + enemy_buffs):
                printr(f'{Y}{stage}{RE} New global buff just drop !!! : {B}{buff["prefabKey"]}{RE}')
                exit()
            else:
                temp = {k:v for k,v in buff.items()}
                temp["blackboard"] = {}
                for blackboard in buff["blackboard"]:
                    temp["blackboard"][blackboard["key"]] = blackboard["valueStr"] if blackboard["valueStr"] else blackboard["value"]
                global_buff.append(temp)
        return global_buff

    def global_lifepoint(def_data, default = 3, diff = "ALL"):
        if def_data:
            for rune in def_data:
                if rune["key"] == "global_lifepoint" and diff == rune["difficultyMask"]:
                    for blackboard in rune["blackboard"]:
                        if blackboard["key"] == "value":
                            return int(blackboard["value"])
        return default
    
    def global_deploy(def_data, default, diff = "ALL"):
        if def_data:
            for rune in def_data:
                if rune["key"] == "global_placable_char_num_add" and diff == rune["difficultyMask"]:
                    for blackboard in rune["blackboard"]:
                        if blackboard["key"] == "value":
                            return int(default + blackboard["value"])
        return default

    def operators_predefine_writer(def_comp_data, def_preauto_data, def_auto_data, fixed):
        #printt("stage, fixed, def_comp_data, def_preauto_data, def_auto_data\n", stage, fixed, def_comp_data, def_preauto_data, def_auto_data ,mode="c")
        def elite_parse(elite):
            if elite.find("PHASE") != -1:
                return elite[-1]
            else:
                printr(f'There is no "PHASE" !!! : {elite}')
                exit()
        
        def op_lister(op, group):
            op_id = op["inst"].get("characterKey", op["alias"])
            op_name = DB["json_characterEN"][op_id]["name"] if op_id in DB["json_characterEN"] else DB["json_characterEN"][op_id]["appellation"]
            op_elite = elite_parse(op["inst"].get("phase", 0))
            op_level = op["inst"].get("level", 1)
            op_skill = op["skillIndex"]
            op_sklv = op["mainSkillLvl"]
            op_trust = op["inst"].get("favorPoint", 0) * 2
            op_mod = op["uniEquipIds"]
            
            group[op_id] = {
                                "name" : op_name, 
                                "elite" : op_elite, 
                                "level" : op_level, 
                                "skill" : op_skill, 
                                "skilllv" : op_sklv, 
                                "trust" : op_trust, 
                                "mod" : op_mod
                            }
            return f'\n\t{op_name} has {op_trust} trust' 
        
        def op_writer(text, lister, mod_count):
            def skill_mastery(skill_lv):
                if skill_lv > 7:
                    return f'Spec. Level {skill_lv - 7}'
                else:
                    return f'Level {skill_lv}'
                
            writer = [f'\n{text} = ']
            sorted_lister = lister.keys() if text[1:] == "comp" else sorted(lister.keys(), key = lambda k : lister[k]["name"])
            for op_id in sorted_lister:
                op_name = lister[op_id]["name"]
                if op_name not in all_op:
                    all_op.append(op_name)
                else:
                    redeploy_op.append(op_name)
                op_elite = lister[op_id]["elite"]
                op_level = lister[op_id]["level"]
                skill_id = DB["json_character"][op_id]["skills"][lister[op_id]["skill"]]["skillId"]
                skill_name = DB["json_skillEN"][skill_id]["levels"][0]["name"] if skill_id in DB["json_skillEN"] else SKILL_NAMES_TL.get(skill_name, f'{DB["json_skill"][skill_id]["levels"][0]["name"]}({skill_id})')
                skill_lv = skill_mastery(lister[op_id]["skilllv"])
                
                trust = lister[op_id]["trust"]
                if trust not in all_trust:
                    all_trust.append(trust)

                if lister[op_id]["mod"]:
                    mod_key = lister[op_id]["mod"][0]["key"]
                    mod_lv = lister[op_id]["mod"][0]["level"]
                    mod_abb = f'{DB["json_uniequip"]["equipDict"][mod_key]["typeIcon"].upper()}'.replace("-D", "-Δ").replace("-A", "-α")
                    
                    all_mod.append([op_name, f'uses {mod_abb} {'[[Operator Module]]' if mod_count == 0 else 'Operator Module'} at Stage {mod_lv}.'])
                    mod_count += 1
                
                writer.append(f'*{{{{C|{op_name}}}}} (Elite {op_elite} Level {op_level}, {{{{Skill|{skill_name}}}}} {skill_lv})')
            
            return "\n".join(writer)
        
        predefine_result = ""
        comp = {}
        pre = {}
        auto = {}
        all_op = []
        redeploy_op = []
        all_trust = []
        all_mod = []
        mod_count = 0
        
        comp_op = ""
        auto_op = ""
        pre_op = ""
        
        if fixed:
            predefine_result += "|fixed = true"
            if def_comp_data:
                for op in def_comp_data:
                    comp_op += op_lister(op, comp)
                predefine_result += op_writer("|comp", comp, mod_count)
            else:
                predefine_result += "\n|comp = None"
            
            if def_preauto_data:
                for op in def_preauto_data:
                    if op["hidden"]:
                        auto_op += op_lister(op, auto)
                    else:
                        pre_op += op_lister(op, pre)
                predefine_result += op_writer("|auto", auto, mod_count)
                predefine_result += op_writer("|pre", pre, mod_count)
            
            predefine_result += "\n|saddendum = \n"
            
            if len(all_op) > 1:
                if len(all_trust) == 1:
                    predefine_result += f'All Operators have {all_trust[0]}% [[Trust]].'
                else:
                    predefine_result += f'''$1 and $2 have $3% [[Trust]].
                                        <!--
                                        Comp = {comp_op}
                                        
                                        Auto = {auto_op}
                                        
                                        Pre = {pre_op}
                                        -->'''.replace("                                        ", "")
                    #exit()

                if all_mod:
                    for mod in all_mod:
                        predefine_result += f'\n*{mod[0]} {mod[1]}'
            elif len(all_op) == 1:
                predefine_result += f'{all_op[0]} has {all_trust[0]}% [[Trust]]{f' and {all_mod[0][1]}' if all_mod else ""}.'
            
        return predefine_result
    
    def auto_deploy_lister(waves):
        ops = []
        for wave in waves:
            for fragment in wave["fragments"]:
                for action in fragment["actions"]:
                    if action["actionType"] == "ACTIVATE_PREDEFINED" and action["key"].split("_") == "char":
                        ops.append(action["key"])
    
    def stage_article_data(data : dict, stage : str, mode : str, diff : str = "") -> dict:            
        def drop_lister(def_data : list) -> dict:
            drop_types = ["COMPLETE", "NORMAL", "ADDITIONAL", "SPECIAL"]
            drop_list = {k:{} for k in drop_types}
            drop_rates = {"ALWAYS": 1, "ALMOST": 2, "USUAL": 3, "OFTEN": 4, "SOMETIMES": 5}
            for drop in def_data:
                if drop["dropType"] == "COMPLETE":
                    drop_list["COMPLETE"][drop["id"]] = drop
                else:
                    drop_list["NORMAL"][drop["id"]] = drop
            drop_output = {k:[] for k in drop_types}
            for drop_type in drop_types:
                for drop in sorted(drop_list[drop_type].keys(), key = lambda k : -100000000000 if k == "4002" else DB["json_item"]["items"][k]["sortId"]):
                    drop_name = DB["json_itemEN"]["items"][drop]["name"] if drop in DB["json_itemEN"]["items"] else ITEM_NAMES_TL.get(drop, f'{DB["json_item"]["items"][drop]["name"]}({drop})')
                    drop_rate = 0 if drop_type == "COMPLETE" else drop_rates[drop_list[drop_type][drop]["occPercent"]]
                    if drop_type == "ADDITIONAL":
                        drop_output[drop_type].append(f'{{{{I|{drop_name}}}}}')
                    else:
                        drop_output[drop_type].append(f'{{{{I|{drop_name}|rate={drop_rate}}}}}')
            
            return {k:" ".join(v) for k,v in drop_output.items()}
            
        match mode :
            case "info":
                code = data["stage_data"][stage]["code"]
                part = data["stage_data"][stage]["zoneId"]
                return {
                            "stage_id" : stage,
                            "code" : code,
                            "name" : data["stage_data"][stage]["name"],
                            "part" : data["zone"][part]["name"],
                            "prev" : data["zone"][part]["stages"][data["zone"][part]["stages"].index(code) - 1] if data["zone"][part]["stages"].index(code) - 1 in range(len(data["zone"][part]["stages"])) else "",
                            "next" : data["zone"][part]["stages"][data["zone"][part]["stages"].index(code) + 1] if data["zone"][part]["stages"].index(code) + 1 in range(len(data["zone"][part]["stages"])) else "",
                            "desc" : data["stage_data"][stage]["description"],
                            "note" : "",
                            "map name" : "",
                            "type" : data["stage_data"][stage],
                            "adverse" : ""
                    }
            case "data":
                enemies_data = enemies_lister(data["enemies_stage"][stage])
                drop_data = drop_lister(data["stage_data"][stage]["stageDropInfo"]["displayDetailRewards"])
                match diff:
                    case "hard" :
                        stage_id = stage + "#f#"
                    case _ :
                        stage_id = stage
                diff_type = data["stage_data"][stage_id]["difficulty"]
                return {
                            "stage_id"      : stage_id,
                            "cond"          : data["stage_data"][stage_id]["description"] if diff else "",
                            "level"         : stage_level(data["stage_data"][stage_id]["dangerLevel"]),
                            "sanity"        : data["stage_data"][stage_id]["apCost"],
                            "drill"         : data["stage_data"][stage_id]["practiceTicketCost"] if isinstance(data["stage_data"][stage_id]["practiceTicketCost"], int) and data["stage_data"][stage_id]["practiceTicketCost"] > 0 else "",
                            "unit_limit"    : data["stage"][stage]["options"]["characterLimit"],
                            "enemies"       : sum(data["enemies_stage"][stage]["counter"][0:2]),
                            "lp"            : global_lifepoint(data["stage"][stage]["runes"], data["stage"][stage]["options"]["maxLifePoint"], diff),
                            "dp"            : data["stage"][stage]["options"]["initialCost"],
                            "deployable"    : token_lister(data["stage"][stage]["predefines"]["tokenCards"]) if data["stage"][stage]["predefines"] else "",
                            "static"        : token_lister(data["stage"][stage]["predefines"]["tokenInsts"]) if data["stage"][stage]["predefines"] else "",
                            "terrain"       : tile_lister(data["stage"][stage]["mapData"]["tiles"]),
                            "addendum"      : "",
                            "firstdrop"     : drop_data.get("COMPLETE", ""),
                            "regdrops"      : drop_data.get("NORMAL", ""),
                            "specdrops"     : drop_data.get("SPECIAL", ""),
                            "extradrops"    : drop_data.get("ADDITIONAL", ""),
                            "normal"        : enemies_data.get("NORMAL", ""),
                            "elite"         : enemies_data.get("ELITE", ""),
                            "boss"          : enemies_data.get("BOSS", ""),
                            "eaddendum"     : eaddendum_lister(stage),
                            "fixed"         : data["stage_data"][stage_id]["isPredefined"] if data["stage_data"][stage_id]["isPredefined"] else "",
                            "comp"          : data["stage"][stage]["predefines"]["characterCards"] if data["stage"][stage]["predefines"] else "",
                            "pre_auto"      : data["stage"][stage]["predefines"]["characterInsts"] if data["stage"][stage]["predefines"] else "",
                            "auto"          : auto_deploy_lister(data["stage"][stage]["waves"]),
                            "saddendum"     : "",
                            "rune"          : rune_lister(data["stage"][stage]["runes"]) if data["stage"][stage]["runes"] else "",
                            "globalBuffs"   : global_buff_lister(data["stage"][stage]["globalBuffs"]) if data["stage"][stage]["globalBuffs"] else "",
                            "enemyDbRefs"   : {enemy["id"]:enemy for enemy in data["stage"][stage]["enemyDbRefs"]},
                            "diff_type"     : diff_type
                        }
            case _ :
                printr(f'Invalid mode {mode}')
                exit()
                return {}
    
    def stage_article_writer(data, mode):
        
        def event_type_writer():
            event_return = (event_name if event_name else event_code) if event_code else ""
            if event_type and event_return:
                return f'|{event_type} = {event_name}'
            else:
                return f'''|episode = {event_return}
                            |intermezzo = {event_return}
                            |sidestory = {event_return}
                            |storycollection = {event_return}
                            '''.replace("                            ", "")
        
        def stage_type_writer():
            ######################################################################################################################################################################################
            ## stage > "appearanceStyle"                                ## Wiki stage TYPE
            ######################################################################################################################################################################################
            ## 'MAIN_NORMAL'            Normal Looking                  ## standard         Normal stage                    ||  default
            ## 'TRAINING'               Training Stage                  ## sub              Sub stage                       ||  appearanceStyle = SUB
            ## 'MAIN_PREDEFINED'        Fixed squad - Main stage        ## fixed            Fixed / Training non Cinematic  ||  isPredefined = True
            ## 'SUB'                    Sub yes sub the S one           ## cinematic        Story battle stage              ||  performanceStageFlag = PERFORMANCE_STAGE
            ## 'SPECIAL_STORY'          Hidden story stage / EG         ## hard             hard/boss stage red stage       ||  hilightMark = True
            ## 'HIGH_DIFFICULTY'        H Stage / Extreme               ## extreme          Extreme stage                   ||  appearanceStyle = HIGH_DIFFICULTY
            ## 'MIST_OPS'               MO stage / Mini annihilation    ##
            ######################################################################################################################################################################################
            if data["type"]["performanceStageFlag"] == "PERFORMANCE_STAGE":
                return f'|type = cinematic'
            elif data["type"]["appearanceStyle"] == "HIGH_DIFFICULTY":
                return f'|type = extreme'
            elif data["type"]["appearanceStyle"] == "SUB":
                return f'|type = sub'
            elif data["type"]["hilightMark"] == True:
                return f'|type = hard'
            elif data["type"]["isPredefined"] == True:
                return f'|type = fixed'
            else:
                return f'|type = standard'
        # https://arknights.wiki.gg/wiki/Template:Operation_info/doc
        match mode:
            case "info":
                return f'''
                            <!-- {data["code"]} ({data["stage_id"]}) -->
                            {{{{construction}}}}
                            {{{{Spoiler notice|article}}}}
                            {{{{Translation|article}}}}
                            {{{{Operation info
                            |code = {data["code"]}
                            |name = {data["name"]}
                            {event_type_writer()}
                            |part = {data["part"]}
                            |prev = {data["prev"]}
                            |next = {data["next"]}
                            |desc = {desc_cond_writer(data["desc"])}
                            |note = {data["note"]}
                            {stage_type_writer()}
                            }}}}'''.replace("                            ", "").replace("\n\n","\n").replace(" ", " ")
            
            # https://arknights.wiki.gg/wiki/Template:Operation_data/doc
            case "data":
                return f'''{{{{Operation data
                            |cond = {desc_cond_writer(data["cond"])}
                            |level = {data["level"]}
                            |sanity = {data["sanity"]}
                            |drill = {data["drill"]}
                            |unit limit = {data["unit_limit"]}
                            |enemies = {data["enemies"]}
                            |lp = {data["lp"]}
                            |dp = {data["dp"]}
                            |deployable = {data["deployable"]}
                            |static = {data["static"] if data["static"] else ""}
                            |terrain = {tile_writer(data["terrain"])}
                            |addendum = {addendum_writer(data["rune"], data["globalBuffs"], diff = data["diff_type"])}
                            |firstdrop = {data["firstdrop"]}
                            |regdrops = {data["regdrops"]}
                            |specdrops = {data["specdrops"]}
                            |extradrops = {data["extradrops"]}
                            |normal = {data["normal"]}
                            |elite = {data["elite"]}
                            |boss = {data["boss"]}
                            |eaddendum = {eaddendum_writer(data["eaddendum"], data["rune"], data["globalBuffs"], data["enemyDbRefs"], data["diff_type"])}
                            {operators_predefine_writer(data["comp"], data["pre_auto"], data["auto"], data["fixed"])}
                            }}}}'''.replace("                            ", "").replace("\n\n","\n").replace(" ", " ")

    def ig_article_data(data, stage_key):
        # https://arknights.wiki.gg/wiki/Template:IG_operation_info
        def ig_group_diff():
            EVENT_DATA = DB["json_activityEN"]["activity"]["MULTIPLAY_V3"][event_code]
            
            map_type = EVENT_DATA["mapDataDict"][stage_key]["modeId"]
            
            ig_stage_mode = EVENT_DATA["mapTypeDataDict"][map_type]["mode"]
            ig_stage_diff = EVENT_DATA["mapTypeDataDict"][map_type]["difficulty"]
            
            group_1 = EVENT_DATA["mapModeDataDict"][ig_stage_mode]["name"]
            group_2 = EVENT_DATA["mapDiffDataDict"][ig_stage_diff]["name"]
            
            match group_2:
                case "Beginner":
                    diff = "NORMAL"
                case "Advanced":
                    diff = "FOUR_STAR"
                case _:
                    diff = ""
            
            return f'{group_1}, {group_2}', diff
        
        printr(stage_key)
        
        ig_group, ig_diff = ig_group_diff()
        currstage_enemies_lister = stage_kill_lister(big_data, stage, ig_diff)
        #printc(currstage_enemies_lister)
        #if stage_key == "act1multi_tr01":
            #script_result(currstage_enemies_lister, True, script_exit=True)
        big_data["enemies_stage"][stage_key] = currstage_enemies_lister
        enemies_data = ig_enemies_lister(currstage_enemies_lister)
        ig_season = re.search(r'act([0-9]){1,2}multi', event_code)
        
        return {
                    "stage_key"     : stage_key,
                    "ig_diff"       : ig_diff,
                    "code"          : data["stage_data"][stage_key]["code"],
                    "name"          : data["stage_data"][stage_key]["name"],
                    "nomap"         : "", 
                    "map"           : "", 
                    "season"        : ig_season.group(1) if ig_season else "", 
                    "group"         : ig_group, 
                    "desc"          : data["stage_data"][stage_key]["description"],
                    "level"         : stage_level(data["stage_data"][stage_key]["dangerLevel"]), 
                    "unit limit"    : data["stage"][stage_key]["options"]["characterLimit"], 
                    "enemies"       : ", ".join([str(counter + sum(currstage_enemies_lister["counter"])) for counter in currstage_enemies_lister["enemy_counter"]]),
                    "lp"            : global_lifepoint(data["stage"][stage_key]["runes"], data["stage"][stage_key]["options"]["maxLifePoint"], ig_diff),
                    "dp"            : global_deploy(data["stage"][stage_key]["runes"], data["stage"][stage_key]["options"]["initialCost"], ig_diff), 
                    "deployable"    : token_lister(data["stage"][stage_key]["predefines"]["tokenCards"]) if data["stage"][stage_key]["predefines"] else "",
                    "static"        : token_lister(data["stage"][stage_key]["predefines"]["tokenInsts"]) if data["stage"][stage_key]["predefines"] else "",
                    "terrain"       : tile_lister(data["stage"][stage_key]["mapData"]["tiles"]),
                    "addendum"      : "", 
                    "ig_ctrl"       : data["stage"][stage_key]["predefines"]["tokenInsts"] if data["stage"][stage_key]["predefines"] else {},
                    "obj1"          : DB["json_activity"]["activity"]["MULTIPLAY_V3"][event_code]["mapDataDict"][stage_key]["missionIdList"][0],
                    "obj2"          : DB["json_activity"]["activity"]["MULTIPLAY_V3"][event_code]["mapDataDict"][stage_key]["missionIdList"][1], 
                    "obj2+"         : DB["json_activity"]["activity"]["MULTIPLAY_V3"][event_code]["mapDataDict"][stage_key]["missionIdList"][2], 
                    "normal"        : enemies_data.get("NORMAL", ""),
                    "elite"         : enemies_data.get("ELITE", ""),
                    "boss"          : enemies_data.get("BOSS", ""),
                    "eaddendum"     : eaddendum_lister(stage_key),
                    "fixed"         : data["stage_data"][stage_key]["isPredefined"] if data["stage_data"][stage_key]["isPredefined"] else "",
                    "comp"          : data["stage"][stage_key]["predefines"]["characterCards"] if data["stage"][stage_key]["predefines"] else "",
                    "pre_auto"      : data["stage"][stage_key]["predefines"]["characterInsts"] if data["stage"][stage_key]["predefines"] else "",
                    "auto"          : auto_deploy_lister(data["stage"][stage_key]["waves"]),
                    "saddendum"     : "",
                    "rune"          : rune_lister(data["stage"][stage_key]["runes"]) if data["stage"][stage_key]["runes"] else "",
                    "globalBuffs"   : global_buff_lister(data["stage"][stage_key]["globalBuffs"]) if data["stage"][stage_key]["globalBuffs"] else ""
        }
    
    def ig_article_writer(ig_data):
        return f'''{{{{IG operation info
                |code = {ig_data["code"].replace("IG-", "", 1)}
                |name = {ig_data["name"]}
                |season = {ig_data["season"]}
                |group = {ig_data["group"]}
                |desc = {desc_cond_writer(ig_data["desc"])}
                |level = {ig_data["level"]}
                |unit limit = {ig_data["unit limit"]}
                |enemies = {ig_data["enemies"]}
                |lp = {ig_data["lp"]}
                |dp = {ig_data["dp"]}
                |deployable = {ig_data["deployable"]} 
                |static = {ig_data["static"]} 
                |terrain = {tile_writer(ig_data["terrain"])}
                |addendum = {addendum_writer(ig_data["rune"], ig_data["globalBuffs"], diff = ig_data["ig_diff"], ig_ctrl = ig_data["ig_ctrl"])},
                |obj1 = {DB["json_activityEN"]["activity"]["MULTIPLAY_V3"][event_code]["targetMissionDataDict"][ig_data["obj1"]]["title"]}; {DB["json_activityEN"]["activity"]["MULTIPLAY_V3"][event_code]["targetMissionDataDict"][ig_data["obj1"]]["description"]}.
                |obj2 = {DB["json_activityEN"]["activity"]["MULTIPLAY_V3"][event_code]["targetMissionDataDict"][ig_data["obj2"]]["title"]}; {DB["json_activityEN"]["activity"]["MULTIPLAY_V3"][event_code]["targetMissionDataDict"][ig_data["obj2"]]["description"]}.
                |obj2+ = {DB["json_activityEN"]["activity"]["MULTIPLAY_V3"][event_code]["targetMissionDataDict"][ig_data["obj2+"]]["title"]}; {DB["json_activityEN"]["activity"]["MULTIPLAY_V3"][event_code]["targetMissionDataDict"][ig_data["obj2+"]]["description"]}.
                |normal = {ig_data["normal"]}
                |elite = {ig_data["elite"]}
                |boss = {ig_data["boss"]}
                |eaddendum = {eaddendum_writer(ig_data["eaddendum"], ig_data["rune"], ig_data["globalBuffs"], diff = ig_data["ig_diff"])}
                {operators_predefine_writer(ig_data["comp"], ig_data["pre_auto"], ig_data["auto"], ig_data["fixed"])}
                }}}}
                {{{{IG operations}}}}
                '''.replace("                ", "").replace("\n\n","\n").replace(" ", " ")

    def tn_article_data(data, stage_key):
        tn_season = re.search(r'act([0-9]){1,2}bossrush', event_code)
        return {
                    "code"          : data["stage_data"][stage_key]["code"],
                    "name"          : data["stage_data"][stage_key]["name"],
                    "season"        : tn_season.group(1) if tn_season else "",
                    "desc"          : data["stage_data"][stage_key]["description"],
                    "entitative"    : "true" if int(stage_key[-1]) > 1 else "",
                    "orientation"   : "true" if stage_key.find("tm") != -1 else "",
                    "cond"          : data["stage_data"][stage_key]["description"] if data["stage_data"][stage_key]["description"].find("附加条件：") != -1 else "",
                    "unit limit"    : data["stage"][stage_key]["options"]["characterLimit"], 
                    "dp"            : data["stage"][stage_key]["options"]["initialCost"], 
                    "lp"            : global_lifepoint(data["stage"][stage_key]["runes"], data["stage"][stage_key]["options"]["maxLifePoint"]),
                    "enemies"       : sum(data["enemies_stage"][stage_key]["counter"][0:2]),
                    "deployable"    : token_lister(data["stage"][stage_key]["predefines"]["tokenCards"]) if data["stage"][stage_key]["predefines"] else "",
                    "static"        : token_lister(data["stage"][stage_key]["predefines"]["tokenInsts"]) if data["stage"][stage_key]["predefines"] else "",
                    "terrain"       : tile_lister(data["stage"][stage_key]["mapData"]["tiles"]),
                    "addendum"      : "",
                    "tn enemies"    : data["enemies_stage"][stage_key]["tn_counter"] ,
                    "eaddendum"     : eaddendum_lister(stage_key),
                    "ultimate"      : "true" if stage_key.find("04") != -1 else "",
                    "comp"          : DB["json_activityEN"]["activity"]["BOSS_RUSH"][event_code]["stageAdditionDataMap"][stage_key]["teamIdList"] if event_code in DB["json_activityEN"]["basicInfo"] else DB["json_activity"]["activity"]["BOSS_RUSH"][event_code]["stageAdditionDataMap"][stage_key]["teamIdList"],
                    "rewards"       : DB["json_activity"]["activity"]["BOSS_RUSH"][event_code]["stageDropDataMap"][stage_key],
                    "rune"          : rune_lister(data["stage"][stage_key]["runes"]) if data["stage"][stage_key]["runes"] else "",
                    "globalBuffs"   : global_buff_lister(data["stage"][stage_key]["globalBuffs"]) if data["stage"][stage_key]["globalBuffs"] else ""
        }
    
    def tn_article_writer(tn_data, mode, ext = 0):
        '''
        mode = info/ data/ squad/ rewards
        '''
        def tn_comp_writer(tn_comp_data) -> str:
            tn_comp_result = []
            tn_decode_result = []
            tn_comp_DB = DB["json_activityEN"]["activity"]["BOSS_RUSH"][event_code] if event_code in DB["json_activityEN"]["basicInfo"] else DB["json_activity"]["activity"]["BOSS_RUSH"][event_code]
            ultimate = tn_data["ultimate"]
            tn_comp_txt = ""
            for team in tn_comp_data:
                if team == "free":
                    continue
                tn_comp_result.append(f'{"*" if ultimate else ""}\'\'\'{tn_comp_DB["teamDataMap"][team]["teamName"]}\'\'\'')
                tn_comp_result.append("\n".join(sorted([f'{'**' if ultimate else "*"}[[{DB["json_characterEN"][char]["name"] if char in DB["json_characterEN"] else DB["json_character"][char]["appellation"]}]]' for char in tn_comp_DB["teamDataMap"][team]["charIdList"]])))
                tn_decode_result.append(f'{{{{Decoder|{tn_comp_DB["teamDataMap"][team]["teamBuffName"]}|{tn_comp_DB["teamDataMap"][team]["teamBuffDes"]}}}}}')
                
            if ultimate:
                tn_comp_txt = f'|comp = \n{"\n".join(tn_comp_result)}\n*7 other additional [[Operator|Operators]] (including the [[Support Unit]])'
            else:
                tn_comp_txt = f'|comp = \n{"One of the following and up to 7 additional [[Operator|Operators]] (including the [[Support Unit]]): "}\n{"\n".join(tn_comp_result)}'
            
            tn_comp_txt += f'\n|decoder = {"".join(tn_decode_result)}'
            
            return tn_comp_txt
        
        def tn_reward_writer(tn_rewards_data) -> str:
            rewards_result = ""
            for stage_reward in tn_rewards_data:
                rewards = []
                for key in sorted(stage_reward.keys()):
                    for reward in stage_reward[key]["displayDetailRewards"]:
                        if stage_reward[key]["clearWaveCount"] and reward["dropCount"]:
                            rewards.append(str(reward["dropCount"]))
                rewards_result += f'\n|{", ".join(rewards)}'
            return rewards_result
        
        match mode:
            case "info":
                return f'''{{{{construction}}}}
                            {{{{Spoiler notice|article}}}}
                            {{{{Translation|article}}}}
                            {{{{TN operation info
                            |code = {tn_data["code"]}
                            |name = {tn_data["name"]}
                            |season = {tn_data["season"]}
                            |desc = {desc_cond_writer(tn_data["desc"])}
                            |entitative = {tn_data["entitative"]}
                            }}}}'''.replace("                            ","").replace("\n\n","\n").replace(" ", " ")
            case "data":
                return f'''{{{{TN operation data
                            {f'|orientation = {tn_data["orientation"]}' if tn_data["orientation"] else ""}
                            {f'|cond = {desc_cond_writer(tn_data["cond"])}' if tn_data["cond"] else ""}
                            |unit limit = {tn_data["unit limit"]}
                            |dp = {tn_data["dp"]}
                            |lp = {tn_data["lp"]}
                            |enemies = {tn_data["enemies"]}
                            |deployable = {tn_data["deployable"]}
                            |static = {tn_data["static"]}
                            |terrain = {tile_writer(tn_data["terrain"])}
                            |addendum = {addendum_writer(tn_data["rune"], tn_data["globalBuffs"])}
                            {tn_enemies_lister(tn_data["tn enemies"])}
                            |eaddendum = {eaddendum_writer(tn_data["eaddendum"], tn_data["rune"], tn_data["globalBuffs"])}
                            }}}}'''.replace("                            ","").replace("\n\n","\n").replace("\n\n","\n").replace(" ", " ")
            case "squad":
                return f'''{{{{TN squad
                            |ultimate = {tn_data["ultimate"]}
                            {tn_comp_writer(tn_data["comp"])}
                            }}}}
                            '''.replace("                            ","").replace("\n\n","\n").replace(" ", " ")
            case "rewards":
                return f'''{{{{TN rewards
                            {tn_reward_writer(tn_data)}
                            }}}}
                            {{{{TN operations}}}}
                            '''.replace("                            ","").replace("\n\n","\n").replace(" ", " ")
            case _:
                printr(f'Seem you forgor {Y}mode{RE} : {R}"tn_article_writer"{RE}')

    def vb_article_data(data, stage_key, mode):
        def group_search(groupId, prev_next):
            match prev_next:
                case "prev": 
                    prev_stage = DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["defenseGroupDict"][groupId]["orderedStageList"][0]
                    if stage_key != prev_stage:
                        return data["stage_data"][prev_stage]["code"]
                    else:
                        return ""
                case "next":
                    next_stage = DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["defenseGroupDict"][groupId]["orderedStageList"][1]
                    if stage_key != next_stage:
                        return data["stage_data"][next_stage]["code"]
                    else:
                        return ""
                case _:
                    printr(f'VB group_search mode invalid : {prev_next}')
                    exit()
            
        vb_tl = {
                    "核心突破" : "Kernel Breakthrough",
                    "特别战线" : "Special Front"
                }

        enemies_data = enemies_lister(data["enemies_stage"][stage_key])
        code = data["stage_data"][stage_key]["code"]
        zoneId = data["stage_data"][stage_key]["zoneId"]
        
        match mode:
            case "core":
                prev_in_zone = data["zone"][zoneId]["stages"][data["zone"][zoneId]["stages"].index(code) - 1] if data["zone"][zoneId]["stages"].index(code) - 1 in range(len(data["zone"][zoneId]["stages"])) else ""
                next_in_zone = data["zone"][zoneId]["stages"][data["zone"][zoneId]["stages"].index(code) + 1] if data["zone"][zoneId]["stages"].index(code) + 1 in range(len(data["zone"][zoneId]["stages"])) else ""
                story_desc = DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["offenseStageDict"][stage_key]["storyDesc"]
                boss_info = DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["offenseStageDict"][stage_key]["bossData"]["desc"] if DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["offenseStageDict"][stage_key]["bossData"] else ""
            case "sp":
                group_id = DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["defenseBasicDict"][stage_key]["groupId"]
                prev_in_zone = group_search(group_id, "prev") if group_id else ""
                next_in_zone = group_search(group_id, "next") if group_id else ""
            case "hard":
                story_desc = DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["hardStageDict"][stage_key]["storyDesc"]
                boss_info = DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["hardStageDict"][stage_key]["bossData"]["desc"] if DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["hardStageDict"][stage_key]["bossData"] else ""
            case _ :
                printr(f'VB mode invalid : {mode}')
                exit()
        
        return {
                    "code" : data["stage_data"][stage_key]["code"],
                    "title" : "",
                    "name" : data["stage_data"][stage_key]["name"],
                    "part" : vb_tl.get(data["zone"][zoneId]["name"], data["zone"][zoneId]["name"]),
                    "prev" : prev_in_zone if mode in ["core", "sp"] else "",
                    "next" : next_in_zone if mode in ["core", "sp"] else "",
                    "story" : story_desc if mode in ["core", "hard"] else "",
                    "desc" : data["stage_data"][stage_key]["description"],
                    "boss info" : boss_info if mode in ["core", "hard"] else "",
                    "unit limit" : data["stage"][stage_key]["options"]["characterLimit"],
                    "enemies" : sum(data["enemies_stage"][stage_key]["counter"][0:2]),
                    "dp" : data["stage"][stage_key]["options"]["initialCost"],
                    "deployable" : token_lister(data["stage"][stage_key]["predefines"]["tokenCards"]) if data["stage"][stage_key]["predefines"] else "",
                    "static" : token_lister(data["stage"][stage_key]["predefines"]["tokenInsts"]) if data["stage"][stage_key]["predefines"] else "",
                    "terrain" : tile_lister(data["stage"][stage_key]["mapData"]["tiles"]),
                    "addendum" : f'\n*Only {DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["defenseDetailDict"][stage_key]["defenseCharLimit"]} [[Operator]]s can be included to the squad.\n*The [[Support Unit]] cannot be used.' if mode == "sp" else "",
                    "firstreward" : DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["stageRewardDict"][stage_key]["completeRewardCnt"],
                    "regreward" : DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["stageRewardDict"][stage_key]["normalRewardCnt"],
                    "supply" : DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["defenseDetailDict"][stage_key]["buffId"] if mode == "sp" else "",
                    "normal" : enemies_data.get("NORMAL", ""),
                    "elite" : enemies_data.get("ELITE", ""),
                    "boss" : enemies_data.get("BOSS", ""),
                    "eaddendum" : eaddendum_lister(stage_key),
                    "rune" : rune_lister(data["stage"][stage_key]["runes"]) if data["stage"][stage_key]["runes"] else "",
                    "globalBuffs" : global_buff_lister(data["stage"][stage_key]["globalBuffs"]) if data["stage"][stage_key]["globalBuffs"] else ""
        }

    def vb_article_writer(vb_data, mode):
        def vb_supply(vb_supply_id):
            vb_supply_data = DB["json_activity"]["activity"]["VEC_BREAK_V2"][event_code]["battleBuffDict"][vb_supply_id]
            return f'''|supply = {vb_supply_data["name"]}
                        |supplyno = {int(vb_supply_id.split("_rune")[-1])}
                        |supplydesc = {vb_supply_data["desc"]}'''.replace("                        ","")
        
        return f'''{{{{construction}}}}
                    {{{{Spoiler notice|article}}}}
                    {{{{Translation|article}}}}
                    {{{{VB operation info
                    |code = {vb_data["code"]}
                    |name = {vb_data["name"]}
                    |part = {vb_data["part"]}
                    |prev = {vb_data["prev"]}
                    |next = {vb_data["next"]}
                    |desc = {(f'\'\'{desc_cond_writer(vb_data["story"])}\'\'\n' if vb_data["story"] else "") + desc_cond_writer(vb_data["desc"])}
                    |boss info = {desc_cond_writer(vb_data["boss info"]) if vb_data["boss info"] else ""}
                    |unit limit = {vb_data["unit limit"]}
                    |enemies = {vb_data["enemies"]}
                    |dp = {vb_data["dp"]}
                    |deployable = {vb_data["deployable"]}
                    |static = {vb_data["static"]}
                    |terrain = {tile_writer(vb_data["terrain"])}
                    |addendum = {addendum_writer(vb_data["rune"], vb_data["globalBuffs"], foot = vb_data["addendum"]) if mode == "sp" else addendum_writer(vb_data["rune"], vb_data["globalBuffs"])}
                    |firstreward = {vb_data["firstreward"]}
                    {f'|regreward = {vb_data["regreward"]}' if mode != "sp" else ""}
                    {vb_supply(vb_data["supply"]) if mode == "sp" else ""}
                    |normal = {vb_data["normal"]}
                    |elite = {vb_data["elite"]}
                    |boss = {vb_data["boss"]}
                    |eaddendum = {eaddendum_writer(vb_data["eaddendum"], vb_data["rune"], vb_data["globalBuffs"])}
                    }}}}
                    '''.replace("                    ","").replace("\n\n","\n").replace(" ", " ")

    def enemy_article_writer(data : dict, mode : str):
        def damage_type(damageType : str) -> str:
            match damageType:
                case "PHYSIC":
                    return "Physical"
                case "MAGIC":
                    return "Arts"
                case "NO_DAMAGE":
                    return "None"
                case "HEAL":
                    return "Healing"
                case _ :
                    printr(f'New enemy damage type detected !!!')
                    exit()

        def enemy_trait(traits : list) -> str:
            form = 0
            enemy_traits = "|trait = "
            for trait in traits:
                if trait["textFormat"] == "TITLE":
                    form += 1
                    enemy_traits += f'|form{form} name = {trait["text"]}\n|form{form} =\n'
                else :
                    enemy_traits += f'*{trait["text"]}\n'
            
            return enemy_traits
        
        def enemy_stats(stats : dict) -> str:
            enemy_stat = ""
            for lv in sorted(stats.keys()):
                enemy_stat += f'|lv{lv} hp = {stats[lv]["maxHp"]}\n|lv{lv} atk = {stats[lv]["atk"]}\n|lv{lv} def = {stats[lv]["def"]}\n|lv{lv} res = {stats[lv]["magicResistance"]:0}\n|lv{lv} eres = {stats[lv]["epDamageResistance"]:0}\n|lv{lv} erst = {stats[lv]["epResistance"]:0}\n'
            return enemy_stat
            
        def base_upgrade_key(enemy_key : str, mode : str) -> str:
            '''
                Mode
                    - base
                    - upgrade
            '''
            base_key = ""
            upgrade_key = ""
            
            if len(enemy_key.split("_")) == 3:
                upgrade_key = enemy_key + "_2"
            else:
                upgrade_key = enemy_key[:-1] + str(int(enemy_key[-1]) + 1)
                if len(enemy_key.split("_")[-1]) == "2":
                    base_key = "_".join(enemy_key.split("_")[:-1])
                else:
                    base_key = enemy_key[:-1] + str(int(enemy_key[-1]) - 1)
            
            if mode == "base":
                return base_key
            elif mode == "upgrade":
                return upgrade_key
            else:
                printr(f'{Y}Wrong Mode BAKA !!!{RE} (Mode = {R}"{mode}"{RE} : Key = {R}{enemy_key}){RE}')
                exit()
            
        # https://arknights.wiki.gg/wiki/Template:Enemy_infobox
        data_name = data["data"]["name"] if data["data"]["name"] else ""
        enemy_name = ENEMY_NAMES_TL.get(data_name, data_name)
        if mode == "info":
            data_prefabKey = data["data"]["prefabKey"] if data["data"]["prefabKey"] else ""
            
            return f'''{{{{construction}}}}
                        {{{{Spoiler notice|article}}}}
                        {{{{Enemy notice|}}}}
                        {{{{Enemy infobox
                        |name = {enemy_name.replace('"',"")}
                        |title = {enemy_name if enemy_name.find('"') != -1 else ""}
                        |image = {enemy_name.replace('"',"") if enemy_name.find('"') != -1 else ""}
                        |code = {data["handbook"]["enemyIndex"]}
                        |cnname = {data["data"]["name"]}
                        |jpname = 
                        |krname = 
                        |type = {data["enemy_type"](data["data"]["enemyTags"])}
                        |grade = {data["data"]["levelType"].capitalize()}
                        |attack = {"Melee/Ranged" if data["data"]["applyWay"] == "ALL" else data["data"]["applyWay"].lower()}
                        |damage = {"/".join([damage_type(damageType) for damageType in data["handbook"]["damageType"]])}
                        |target = {"Aerial" if data["data"]["motion"] == "FLY" else "Ground"}
                        {enemy_trait(data["handbook"]["abilityList"])}
                        |intro = {event_name}
                        |base = {ENEMY_NAMES_TL[base_upgrade_key(data_prefabKey, "base")] if base_upgrade_key(data_prefabKey, "base")in DB["json_enemy_handbook"]["enemyData"].keys() else ""}
                        |upgrade = {ENEMY_NAMES_TL[base_upgrade_key(data_prefabKey, "base")] if base_upgrade_key(data_prefabKey, "base") in DB["json_enemy_handbook"]["enemyData"].keys() else ""}
                        }}}}'''.replace("                        ", "")
        if mode == "header":
            return f"The '''{enemy_name if enemy_name.find('"') != -1 else ""}''' is a [[{R} enemy]|{R}] in ''[[Arknights]]''."
        if mode == "enemy desc":
            return f'{{{{Enemy description|{data["handbook"]["description"]}}}}}'
        if mode == "Overview":
            return '''==Overview==
                        {{{{Enemy ability head}}}}
                        {{{{Enemy ability cell|info=|type=|initcd=|cd=}}}}
                        {{{{Table end}}}}'''.replace("                        ", "")
                        
        if mode == "Appearances":
            return '''==Appearances==
                        {{{{Appearances |side stories = [[EP-8]] &bull; [[EP-EX-8]]}}}}'''
        if mode == "stat":
            return f'''==Stats==
                        {{{{Enemy stats
                        {enemy_stats(data["lv"])}
                        |speed = {data["lv"]["0"]["moveSpeed"]}
                        |interval = {data["lv"]["0"]["baseAttackTime"]}
                        |range = {data["data"]["rangeRadius"] if data["data"]["rangeRadius"] != -1 else 0}
                        |range note = 
                        |regen = {data["lv"]["0"]["hpRecoveryPerSec"]}
                        |regen note = 
                        |weight = {data["lv"]["0"]["massLevel"]}
                        |weight note = 
                        |lp = {data["data"]["lifePointReduce"]}
                        |lp note = 
                        |silence = {0 if data["lv"]["0"]["silenceImmune"] else ""}
                        |stun = {0 if data["lv"]["0"]["stunImmune"] else ""}
                        |sleep = {0 if data["lv"]["0"]["sleepImmune"] else ""}
                        |freeze = {0 if data["lv"]["0"]["frozenImmune"] else ""}
                        |levitate = {0 if data["lv"]["0"]["levitateImmune"] else ""}
                        |frighten = {0 if data["lv"]["0"]["disarmedCombatImmune"] else ""}
                        |fear = {0 if data["lv"]["0"]["fearedImmune"] else ""}
                        |addendum = 
                        }}}}
                        '''.replace("                        ", "")
        if mode == "year":
            return f'{{{{Y{R} enemies}}}}'
        
    article_data = []
    ishard = False
    is6star = False
    big_data = wiki_enemies(event_code)
    big_data["enemies_stage"] = {}
    if event_type != "ig":
        for stage in big_data["stage"]:
            big_data["enemies_stage"][stage] = stage_kill_lister(big_data, stage)
        
    #script_result(big_data)
    #exit()
    # Stage article
    # - https://arknights.wiki.gg/wiki/Template:Operation_info/doc
    # - https://arknights.wiki.gg/wiki/Template:Operation_data/doc
    if event_type in ["vb", "ig", "tn"]:
        mode_info = event_type
        page_footer = "Seasonal game modes"
    else:
        mode_info = "sidestory"
        page_footer = "Side Story operations"
        
    for stage in big_data["stage"].keys():
        if mode_info == "sidestory":
            stage_info = stage_article_data(big_data, stage, "info")
            stage_data = stage_article_data(big_data, stage, "data")
            if big_data["stage_data"][stage]["hardStagedId"]:
                ishard = True
                stage_data_hard = stage_article_data(big_data, stage, "data", "hard")
            
            if big_data["stage_data"][stage]["sixStarStageId"]:
                is6star = True
                stage_data_hard = stage_article_data(big_data, stage, "data", "sandbox")
            
            if ishard or is6star:
                stage_article = [stage_article_writer(stage_info, "info"), "<tabber>", "Normal Mode=", stage_article_writer(stage_data, "data"), "|-|Challenge Mode=", stage_article_writer(stage_data_hard, "data"), "</tabber>", f'{{{{{page_footer}}}}}']
            else:
                stage_article = [stage_article_writer(stage_info, "info"), stage_article_writer(stage_data, "data"), f'{{{{{page_footer}}}}}']
            article_data += stage_article
        
        elif mode_info == "ig":
            stage_info = ig_article_data(big_data, stage)
            stage_article = [f'### {stage}', f'{{{{Construction}}}}', ig_article_writer(stage_info)]
            article_data += stage_article
        
        elif mode_info == "tn":
            tn_diff = ["Basic Trial", "Orientation Trial", "Spectacular Trial", "Ultimate Trial"]
            tn_stage_code_template = [f'{event_code}_0', f'{event_code}_tm0', f'{event_code}_ex0', f'{event_code}_fin0']
            tn_stage_count = len(list(set(big_data["zone"][f'{event_code}_zone1']["stages"])))
            for i in range(1, 1 + tn_stage_count):
                tn_wave_count = big_data["zone"][f'{event_code}_zone1']["stages"].count(f'TN-{i}')
                tn_reward = []
                for j in range(tn_wave_count):
                    tn_stage_code = f'{tn_stage_code_template[j]}{i}'
                    tn_article_data_dict = tn_article_data(big_data, tn_stage_code)
                    tn_reward.append(tn_article_data_dict["rewards"])
                    if j == 0 :
                        article_data += [f'TN-{i}', tn_article_writer(tn_article_data_dict, "info"), "<tabber> Basic Trial="]
                    else:
                        article_data += [f'|-|{tn_diff[j]}=']
                    
                    article_data += [tn_article_writer(tn_article_data_dict, "data")]
                
                article_data += ["</tabber>\n", tn_article_writer(tn_article_data(big_data, f'{tn_stage_code_template[1]}{i}'), "squad"), tn_article_writer(tn_reward, "rewards")]
            break
        
        elif mode_info == "vb":
            if stage.find("sp") != -1 :
                mode = "sp"
                #continue
            elif stage.find("_h") != -1 :
                mode = "hard"
                #continue
            else:
                mode = "core"
                #continue
            stage_info = vb_article_data(big_data, stage, mode)
            stage_article = [f'### {stage}', vb_article_writer(stage_info, mode), f'{{{{{page_footer}}}}}']
            article_data += stage_article

    # Enemies articles
    # - https://arknights.wiki.gg/wiki/Template:Enemy_infobox
    # - https://arknights.wiki.gg/wiki/Template:Appearances
    for enemy in big_data["enemies"]:
        #print(enemy)
        break
        enemy_article_writer(big_data["enemies"][enemy])
    #printc(sorted(data["enemies"].keys()))
    script_result(big_data)
    return article_data
    
#wiki_article("act40side", "sidestory")

#script_result(wiki_article("act40side", "event"))

# Trials for Navigator #04
#script_result(wiki_article("act4bossrush", "tn", "Trials for Navigator #04"))

# Rhodes Island Icebreaker Games #1
script_result(wiki_article("act1multi", "ig", "Rhodes Island Icebreaker Games #1"), True)

# Vector Breakthrough Mechanist
#script_result(wiki_article("act1break", "vb", "Vector Breakthrough Mechanist"))