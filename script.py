import glob
import json
import re
from types import NoneType
from typing import Literal
import pandas as pd

from pyFunction import R, G, B, Y, RE, json_load, printr, script_result
from pyFunction_Wiki import CLASS_PARSE_EN, range_template, replace_apos_between, wiki_stage, wiki_story, wiki_trim

################################################################################################################################################################################################################################################
# JSON
################################################################################################################################################################################################################################################

def load_json() -> dict :
    return {
                "json_activity" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/activity_table.json"),
                "json_audio" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/audio_data.json"),
                "json_battle_equip" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/battle_equip_table.json"),
                "json_building" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/building_data.json"),
                "json_campaign" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/campaign_table.json"),
                "json_chapter" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/chapter_table.json"),
                "json_character" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/character_table.json"),
                "json_charm" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/charm_table.json"),
                "json_charword" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/charword_table.json"),
                "json_char_meta" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/char_meta_table.json"),
                "json_char_patch" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/char_patch_table.json"),
                "json_checkin" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/checkin_table.json"),
                "json_climb_tower" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/climb_tower_table.json"),
                "json_clue" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/clue_data.json"),
                "json_crisis" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/crisis_table.json"),
                "json_crisis_v2" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/crisis_v2_table.json"),
                "json_display_meta" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/display_meta_table.json"),
                "json_enemy_handbook" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/enemy_handbook_table.json"),
                "json_favor" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/favor_table.json"),
                "json_gacha" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/gacha_table.json"),
                "json_gamedata" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/gamedata_const.json"),
                "json_handbook_info" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/handbook_info_table.json"),
                "json_handbook" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/handbook_table.json"),
                "json_handbook_team" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/handbook_team_table.json"),
                "json_item" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/item_table.json"),
                "json_medal" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/medal_table.json"),
                "json_mission" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/mission_table.json"),
                "json_open_server" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/open_server_table.json"),
                "json_player_avatar" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/player_avatar_table.json"),
                "json_range" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/range_table.json"),
                "json_replicate" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/replicate_table.json"),
                "json_retro" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/retro_table.json"),
                "json_roguelike" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/roguelike_table.json"),
                "json_roguelike_topic" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/roguelike_topic_table.json"),
                "json_sandbox_perm" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/sandbox_perm_table.json"),
                "json_sandbox" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/sandbox_table.json"),
                "json_shop_client" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/shop_client_table.json"),
                "json_skill" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/skill_table.json"),
                "json_skin" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/skin_table.json"),
                "json_stage" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/stage_table.json"),
                "json_story_review_meta" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/story_review_meta_table.json"),
                "json_story_review" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/story_review_table.json"),
                "json_story" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/story_table.json"),
                "json_tech_buff" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/tech_buff_table.json"),
                "json_tip" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/tip_table.json"),
                "json_token" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/token_table.json"),
                "json_uniequip" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/uniequip_table.json"),
                "json_zone" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/zone_table.json"),
                "json_enemy_database" : json_load("json/gamedata/ArknightsGameData/zh_CN/gamedata/levels/enemydata/enemy_database.json"),
                
                "json_activityEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/activity_table.json"),
                "json_audioEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/audio_data.json"),
                "json_battle_equipEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/battle_equip_table.json"),
                "json_buildingEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/building_data.json"),
                "json_campaignEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/campaign_table.json"),
                "json_chapterEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/chapter_table.json"),
                "json_characterEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/character_table.json"),
                "json_charmEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/charm_table.json"),
                "json_charwordEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/charword_table.json"),
                "json_char_metaEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/char_meta_table.json"),
                "json_char_patchEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/char_patch_table.json"),
                "json_checkinEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/checkin_table.json"),
                "json_climb_towerEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/climb_tower_table.json"),
                "json_clueEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/clue_data.json"),
                "json_crisisEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/crisis_table.json"),
                "json_crisis_v2EN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/crisis_v2_table.json"),
                "json_display_metaEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/display_meta_table.json"),
                "json_enemy_handbookEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/enemy_handbook_table.json"),
                "json_favorEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/favor_table.json"),
                "json_gachaEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/gacha_table.json"),
                "json_gamedataEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/gamedata_const.json"),
                "json_handbook_infoEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/handbook_info_table.json"),
                "json_handbookEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/handbook_table.json"),
                "json_handbook_teamEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/handbook_team_table.json"),
                "json_itemEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/item_table.json"),
                "json_medalEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/medal_table.json"),
                "json_missionEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/mission_table.json"),
                "json_open_serverEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/open_server_table.json"),
                "json_player_avatarEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/player_avatar_table.json"),
                "json_rangeEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/range_table.json"),
                "json_replicateEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/replicate_table.json"),
                "json_retroEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/retro_table.json"),
                "json_roguelikeEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/roguelike_table.json"),
                "json_roguelike_topicEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/roguelike_topic_table.json"),
                "json_sandbox_permEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/sandbox_perm_table.json"),
                "json_sandboxEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/sandbox_table.json"),
                "json_shop_clientEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/shop_client_table.json"),
                "json_skillEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/skill_table.json"),
                "json_skinEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/skin_table.json"),
                "json_stageEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/stage_table.json"),
                "json_story_review_metaEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/story_review_meta_table.json"),
                "json_story_reviewEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/story_review_table.json"),
                "json_storyEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/story_table.json"),
                "json_tech_buffEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/tech_buff_table.json"),
                "json_tipEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/tip_table.json"),
                "json_tokenEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/token_table.json"),
                "json_uniequipEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/uniequip_table.json"),
                "json_zoneEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/zone_table.json"),
                "json_enemy_databaseEN" : json_load("json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/levels/enemydata/enemy_database.json"),
                
                "json_named_effect" : json_load("json/named_effects.json"),
                "json_dict" : json_load("py/dict.json")
        }

DB = load_json()

################################################################################################################################################################################################################################################
# Util
################################################################################################################################################################################################################################################
def list_to_array(LIST : list) -> list :
    return [elem for elem in LIST if elem not in [f'\n{"-"*80}\n', ""]]

def join_and(text_list : list | set) -> str :
    return_text = " and ".join(text_list)
    if len(text_list) >= 3:
        return_text = return_text.replace(" and ", ", ", len(text_list) - 2)
    return return_text

def falsy_compare(a, b) -> bool:
    return not bool(a) and not bool(b) or a == b

def decimal_format(dec : float) -> str:
    if int(dec) != dec and len(str(dec).split(".")[-1]) > 1:
        return f'{dec:.2f}'
    elif int(dec) != dec and len(str(dec).split(".")[-1]) == 1:
        return f'{dec:.1f}'
    else:
        return f'{dec:.0f}'

################################################################################################################################################################################################################################################
# Old Script
################################################################################################################################################################################################################################################
def skin_lister(show : bool = False) :
    '''
        list all skin name
    '''
    skin_list = []

    for skin in DB["json_skin"]["charSkins"]:
        if skin.find("char_") == 0 : 
            if skin.find("@") != -1:
                new_skin = skin.replace("@","_")
            else:
                new_skin = skin.replace("#","_")
            #print(new_skin)
            skin_list.append(new_skin)

    skin_list.sort(key = lambda skin : (int(skin.split("_")[1]) , skin.split("_")[3]))

    script_result("\n".join(skin_list))

def skill_icon_lister(show : bool = False):
    '''
        list all skill id
    '''
    skill_list = []

    for skill in DB["json_skill"]:
        if skill.find("sktok") != 0:
            if DB["json_skill"][skill]["iconId"]:
                skill_icon = f'skill_icon_{DB["json_skill"][skill]["iconId"]}.png'
            else : skill_icon = f'skill_icon_{skill}.png'
        
            skill_list.append(skill_icon)   

    skill_list = sorted(list(set(skill_list)))

    with open("py/script compare.txt","r") as filepath:
        for text in filepath:
            if text.strip() in skill_list :
                print(text)
                skill_list.remove(text.strip())

    script_result("\n".join(skill_list))

def ops_e2_talent(show : bool = False):
    '''
        fetch e2 talent both p1 and talent potential
    '''
    new_mod = [["Ines"]]

    #print(DB["json_character"].keys())
    #DB["json_character"][char]["appellation"]
    char_dict = {char:(DB["json_characterEN"][char]["talents"] if char in DB["json_characterEN"] else DB["json_character"][char]["talents"]) for char in DB["json_character"] if DB["json_character"][char]["appellation"] in [mod[0] for mod in new_mod]}

    for char,talents in char_dict.items():
        char_dict[char] = [[{("upgradeDescription" if x == "description" else x):talent["candidates"][i][x] for x in ["name", "description", "blackboard"]} for i in ([-1] if talent["candidates"][-1]["requiredPotentialRank"] == 0 else [-2,-1])] for talent in talents]
    script_result(char_dict)

def term_kw(show : bool = False):
    term_list = []
    for term in DB["json_named_effect"]["termDescriptionDict"]:
        if term[0:2] == "ba":
            term_detail = DB["json_named_effect"]["termDescriptionDict"][term]
            term_list.append(term_detail["termId"]+"\t"+term_detail["termName"]+"\t"+term_detail["description"])
    
    script_result("\n".join(term_list))

def stage_kill_test(show : bool = False):
    IGNORED = {"enemy_10082_mpweak","enemy_10072_mpprhd"}
    test = {"all":{}, "filtered_start":{},"filtered_end":{}, "enemies":{"KILL":0, "NORMAL":[], "ELITE":[], "BOSS":[], "Extra":[]}}
    times = 0
    enemies = {"KILL":{}, "Extra":{}}
    count = [0,0]
    stage_path = r'json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\obt\training\level_training_26.json'
    stage_key = stage_path.split("\\")[-1].replace("level_", "").replace(".json", "").replace("training","tr")
    script_json = json_load(stage_path)

    stages_json = json_load(r'test\stage.json')

    def enemy_motion_search(key):
        for data in DB["json_enemy_database"]["enemies"]:
            if data["Key"] == key:
                return data["Value"][0]["enemyData"]["motion"]["m_value"]

    def enemy_ref():
        temp = {}
        for enemy_data in script_json.get("enemyDbRefs", []):
            if enemy_data["overwrittenData"] and enemy_data["overwrittenData"]["prefabKey"]["m_defined"]:
                temp[enemy_data["id"]] = enemy_data["overwrittenData"]["prefabKey"]["m_value"]
            else :
                temp[enemy_data["id"]] = enemy_data["id"]
        return temp

    enemy_ref_json = enemy_ref()
    print(enemy_ref_json)

    height = len(script_json["mapData"]["map"])
    width = len(script_json["mapData"]["map"][0])
    for wave in script_json.get("waves",[]):
        times += wave["preDelay"] + wave["postDelay"]
        for fragment in wave.get("fragments",[]):
            times += fragment["preDelay"]
            for action in fragment.get("actions",[]):
                times += action["preDelay"]
                routes = script_json["routes"][action["routeIndex"]]
                currroute = {
                                "actionType"        : action["actionType"],
                                "key"               : action["key"],
                                "count"             : action["count"],
                                "startPosition"     : routes["startPosition"],
                                "TEST_start"        : script_json["mapData"]["map"][-routes["startPosition"]["row"]-1][routes["startPosition"]["col"]],
                                "TEST_tile_start"   : script_json["mapData"]["tiles"][script_json["mapData"]["map"][-routes["startPosition"]["row"]-1][routes["startPosition"]["col"]]]["tileKey"],
                                "endPosition"       : routes["endPosition"],
                                "TEST_end"          : script_json["mapData"]["map"][-routes["endPosition"]["row"]-1][routes["endPosition"]["col"]],
                                "TEST_tile_end"     : script_json["mapData"]["tiles"][script_json["mapData"]["map"][-routes["endPosition"]["row"]-1][routes["endPosition"]["col"]]]["tileKey"],
                                "checkpoints"       : routes["checkpoints"]
                            }
                test["all"][action["routeIndex"]] = currroute
                # Is enemy // Spawning // not mechanic enemy
                if action["key"].split("_")[0] == "enemy" and action["actionType"] == "SPAWN" and action["key"] not in IGNORED:
                    #from Red box // or // prespawn
                    if script_json["mapData"]["tiles"][script_json["mapData"]["map"][-routes["startPosition"]["row"]-1][routes["startPosition"]["col"]]]["tileKey"] == "tile_start" or times == 0: 
                        test["filtered_start"][action["routeIndex"]] = currroute
                        enemies["KILL"][enemy_ref_json[action["key"]]] = enemies["KILL"].get(enemy_ref_json[action["key"]], 0) + action["count"]
                        count[0] += action["count"]
                    #Go to Red box // #legal spawn movement
                    elif script_json["mapData"]["tiles"][script_json["mapData"]["map"][-routes["endPosition"]["row"]-1][routes["endPosition"]["col"]]]["tileKey"] == "tile_end":# and enemy_motion_search(action["key"]) == routes["motionMode"]:
                        test["filtered_end"][action["routeIndex"]] = currroute
                        enemies["Extra"][enemy_ref_json[action["key"]]] = enemies["Extra"].get(enemy_ref_json[action["key"]], 0) + action["count"]
                        count[1] += action["count"]

    for enemy in enemies["KILL"].keys():
        test["enemies"]["KILL"] += enemies["KILL"][enemy]
        test["enemies"][DB["json_enemy_handbook"]["enemyData"][enemy]["enemyLevel"]].append([enemy, DB["json_enemy_handbook"]["enemyData"][enemy]["name"], DB["json_enemy_handbookEN"]["enemyData"][enemy]["name"] if enemy in DB["json_enemy_handbookEN"]["enemyData"].keys() else "" , enemies["KILL"][enemy]])

    for enemy in enemies["Extra"].keys():
        test["enemies"]["Extra"].append([enemy, DB["json_enemy_handbook"]["enemyData"][enemy]["name"], DB["json_enemy_handbookEN"]["enemyData"][enemy]["name"] if enemy in DB["json_enemy_handbookEN"]["enemyData"].keys() else "" , enemies["Extra"][enemy]])

    print(f'\n# {stage_key} ({stages_json["stages"][stage_key]["code"]})\nMAP Height : {height}, MAP Width : {width}')
    print("Enemy count = ", count[0], "### More suspect = ", count[1])
    script_result(test)

def stage_kills(stage_paths = [], show : bool = False): #need check for drop in like kevin
    IGNORED = {"enemy_10082_mpweak", "enemy_10072_mpprhd", "enemy_3009_mpprss"} # square / Hand / EYESOFPRIESTESS
    result_json = {}
    result_text = []
    for stage_path in stage_paths if stage_paths else [r'json\gamedata\ArknightsGameData_YoStar\en_US\gamedata\levels\obt\campaign\level_camp_03.json']: #[rf'json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\obt\main\level_main_15-{i+1:02}.json' for i in range(18)] + [r'json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\obt\training\level_training_26.json'] + [rf'json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\obt\hard\level_hard_15-{i+1:02}.json' for i in range(4)]:
        temp = {"KILL":0, "NORMAL":[], "ELITE":[], "BOSS":[], "Extra":[], "Extra_details":[]}
        times = 0
        enemies = {"KILL":{}, "Extra":{}}
        count = [0,0]
        stage_key = stage_path.split("\\")[-1].replace("level_", "").replace(".json", "").replace("training","tr")
        script_json = json_load(stage_path)

        stages_json = json_load(r'test\stage.json')

        def enemy_count(key):
            for data in DB["json_enemy_database"]["enemies"]:
                if data["Key"] == key:
                    return data["Value"][0]["enemyData"]["notCountInTotal"]["m_value"]

        def enemy_ref():
            temp = {}
            for enemy_data in script_json.get("enemyDbRefs", []):
                if enemy_data["overwrittenData"] and enemy_data["overwrittenData"]["prefabKey"]["m_defined"]:
                    temp[enemy_data["id"]] = enemy_data["overwrittenData"]["prefabKey"]["m_value"]
                else :
                    temp[enemy_data["id"]] = enemy_data["id"]
            return temp

        enemy_ref_json = enemy_ref()

        height = len(script_json["mapData"]["map"])
        width = len(script_json["mapData"]["map"][0])
        for wave in script_json.get("waves",[]):
            times += wave["preDelay"] + wave["postDelay"]
            for fragment in wave.get("fragments",[]):
                times += fragment["preDelay"]
                for action in fragment.get("actions",[]):
                    if action["hiddenGroup"] and action["hiddenGroup"] != "group1": continue
                    if action["actionType"] == "SPAWN": times += action["preDelay"]
                    routes = script_json["routes"][action["routeIndex"]]
                    currroute = {
                                                                    "actionType"        : action["actionType"],
                                                                    "key"               : action["key"],
                                                                    "count"             : action["count"],
                                                                    "hiddenGroup"       : action["hiddenGroup"],
                                                                    "routeIndex"        : action["routeIndex"],
                                                                    "startPosition"     : routes["startPosition"],
                                                                    "TEST_start"        : script_json["mapData"]["map"][-routes["startPosition"]["row"]-1][routes["startPosition"]["col"]],
                                                                    "TEST_tile_start"   : script_json["mapData"]["tiles"][script_json["mapData"]["map"][-routes["startPosition"]["row"]-1][routes["startPosition"]["col"]]]["tileKey"],
                                                                    "endPosition"       : routes["endPosition"],
                                                                    "TEST_end"          : script_json["mapData"]["map"][-routes["endPosition"]["row"]-1][routes["endPosition"]["col"]],
                                                                    "TEST_tile_end"     : script_json["mapData"]["tiles"][script_json["mapData"]["map"][-routes["endPosition"]["row"]-1][routes["endPosition"]["col"]]]["tileKey"],
                                                                    "checkpoints"       : routes["checkpoints"]
                                                                }
                    # Is enemy // Spawning // not mechanic enemy
                    if action["key"].split("_")[0] == "enemy" and action["actionType"] == "SPAWN" and action["key"] not in IGNORED:
                        #from Red box // or // prespawn
                        if script_json["mapData"]["tiles"][script_json["mapData"]["map"][-routes["startPosition"]["row"]-1][routes["startPosition"]["col"]]]["tileKey"] in ["tile_start", "tile_flystart"] or times == 0: 
                            enemies["KILL"][enemy_ref_json[action["key"]]] = enemies["KILL"].get(enemy_ref_json[action["key"]], 0) + action["count"]
                            count[0] += action["count"]
                        #Go to Red box // #legal spawn movement
                        elif script_json["mapData"]["tiles"][script_json["mapData"]["map"][-routes["endPosition"]["row"]-1][routes["endPosition"]["col"]]]["tileKey"] == "tile_end":# and enemy_motion_search(action["key"]) == routes["motionMode"]:
                            temp["Extra_details"].append(currroute)
                            enemies["Extra"][enemy_ref_json[action["key"]]] = enemies["Extra"].get(enemy_ref_json[action["key"]], 0) + action["count"]
                            count[1] += action["count"]

        for enemy in enemies["KILL"].keys():
            temp["KILL"] += enemies["KILL"][enemy]
            temp[DB["json_enemy_handbook"]["enemyData"][enemy]["enemyLevel"]].append([enemy, DB["json_enemy_handbook"]["enemyData"][enemy]["name"], DB["json_enemy_handbookEN"]["enemyData"][enemy]["name"] if enemy in DB["json_enemy_handbookEN"]["enemyData"].keys() else "" , enemies["KILL"][enemy]])

        for enemy in enemies["Extra"].keys():
            temp["Extra"].append([enemy, DB["json_enemy_handbook"]["enemyData"][enemy]["name"], DB["json_enemy_handbookEN"]["enemyData"][enemy]["name"] if enemy in DB["json_enemy_handbookEN"]["enemyData"].keys() else "" , enemies["Extra"][enemy]])

        print(f'\n# {stage_key} ({stages_json["stages"][stage_key]["code"]})\nMAP Height : {height}, MAP Width : {width}')
        print("Enemy count = ", count[0], "### More suspect = ", count[1])
        result_json[f'{stage_key} ({stages_json["stages"][stage_key]["code"]})'] = temp
    
    #script_result(result_json)
    
    for stage in result_json.keys():
        result_text.append(f'\n{"-"*80}\n\n# {stage}\n')
        result_text.append(f'\tKill counter : {result_json[stage]["KILL"]}\n')
        for level in ["NORMAL", "ELITE", "BOSS"]:
            if result_json[stage][level]:
                result_text.append(f'\t{level}')
                for enemy in result_json[stage][level]:
                    result_text.append(f'\t{enemy[3]:3} X {enemy[0]:25}\t{enemy[1]:30}\t{enemy[2]}')
        if result_json[stage]["Extra"]:
            result_text.append("\n\tExtra")
            for enemy in result_json[stage]["Extra"]:
                result_text.append(f'\t{enemy[3]:3} X {enemy[0]:25}\t{enemy[1]:30}\t{enemy[2]}')
        
    #script_result(("\n").join(result_text), show)
    
    if stage_paths:
        return result_json

def infinity_skill(show : bool = False):
    infinity = []
    exclude = ["skchr_typhon_2", "skchr_thorns_3", "skchr_buildr_2"]
    bypass = ["skchr_swire2_1", "skchr_swire2_2", "skchr_marcil_2"]
    skill_CN = DB["json_skill"]
    skill_EN = DB["json_skillEN"]
    text_to_find = ["Can switch between the default state and the following state", 
                    "Can switch between the original state and the following state",
                    "Can switch between the initial state and the following state",
                    "Can switch between initial state and the following state:",
                    "Unlimited duration, can manually deactivate skill",
                    "Unlimited duration", 
                    "Infinite duration",
                    "Manually Bypass",
                    "持续时间无限"]
    
    i_range = range(len(text_to_find))
    temp = [[] for i in i_range]
    
    for skill in skill_EN:
        if skill.find("skchr") == -1 and skill.find("skcom") == -1 or skill in exclude:
            continue
        #print(skill, skill.find("skchar") != -1, skill_EN[skill]["levels"][0]["description"])
        if skill in bypass:
            temp[len(text_to_find) - 2].append(skill)
            infinity.append(skill)
            continue
        if skill_EN[skill]["levels"][0]["description"]:
            for txt in range(len(text_to_find) - 2):
                if skill_EN[skill]["levels"][0]["description"].find(text_to_find[txt]) != -1:
                    temp[txt].append(skill)
                    infinity.append(skill)
                    break
    
    infinity.append(f'\n{"-" * 80}\n')
    
    for skill in skill_CN:
        if skill.find("skchr") == -1 and skill.find("skcom") == -1:
            continue
        #print(skill, skill.find("skchar") != -1, skill_CN[skill]["levels"][0]["description"])
        if skill in infinity + exclude:
            #print(skill,"DUPE key")
            continue
        if skill_CN[skill]["levels"][0]["description"] and skill_CN[skill]["levels"][0]["description"].find("持续时间无限") != -1:
            temp[len(text_to_find) - 1].append(skill)
            infinity.append(skill)
    
    print("\nSkills :\n", list_to_array(infinity))
    print("\nOperators :\n", sorted(set([skill.split("_")[1] for skill in list_to_array(infinity)])))
    for i in i_range:
        if temp[i]:
            print("\n# ", text_to_find[i],"\n",temp[i])
    
    script_result(infinity)

################################################################################################################################################################################################################################################
# DB Keys
################################################################################################################################################################################################################################################

#'json_activity', 'json_audio', 'json_battle_equip', 'json_building', 'json_campaign', 'json_chapter', 'json_character', 'json_charm',
#'json_charword', 'json_char_meta', 'json_char_patch', 'json_checkin', 'json_climb_tower', 'json_clue', 'json_crisis', 'json_crisis_v2',
#'json_display_meta', 'json_enemy_handbook', 'json_favor', 'json_gacha', 'json_gamedata', 'json_handbook_info', 'json_handbook', 'json_handbook_team',
#'json_item', 'json_medal', 'json_mission', 'json_open_server', 'json_player_avatar', 'json_range', 'json_replicate', 'json_retro', 'json_roguelike',
#'json_roguelike_topic', 'json_sandbox_perm', 'json_sandbox', 'json_shop_client', 'json_skill', 'json_skin', 'json_stage', 'json_story_review_meta',
#'json_story_review', 'json_story', 'json_tech_buff', 'json_tip', 'json_token', 'json_uniequip', 'json_zone', 'json_enemy_database'

# EN

################################################################################################################################################################################################################################################
# Script Playground
################################################################################################################################################################################################################################################

def char_name(show : bool = False):
    temp = {}
    DB_CN : dict = DB["json_character"]
    DB_CN.update(DB["json_char_patch"]["patchChars"])
    
    DB_EN : dict = DB["json_characterEN"]
    DB_EN.update(DB["json_char_patchEN"]["patchChars"])
    
    DB_JP : dict = json_load("json/gamedata/ArknightsGameData_YoStar/ja_JP/gamedata/excel/character_table.json")
    DB_JP.update(json_load("json/gamedata/ArknightsGameData_YoStar/ja_JP/gamedata/excel/char_patch_table.json")["patchChars"])
    
    DB_KR : dict = json_load("json/gamedata/ArknightsGameData_YoStar/ko_KR/gamedata/excel/character_table.json")
    DB_KR.update(json_load("json/gamedata/ArknightsGameData_YoStar/ko_KR/gamedata/excel/char_patch_table.json")["patchChars"])
    
    SUBCLASS    : dict = DB["json_uniequipEN"]["subProfDict"]
    
    SUBCLASS_CN : dict = {"counsellor" : "Strategist"}
    
    skip_key    : list = ["name", "appellation"]
    skip        : dict = dict.fromkeys(skip_key, "")
    for key in DB_CN.keys():
        if key.startswith("trap_"):
            continue
        else :
            char_class = DB_CN.get(key, skip)["profession"]
            char_sub_class : str = DB_CN.get(key, skip)["subProfessionId"]
            temp[key] = {
                                            "rarity":   DB_CN.get(key, skip)["rarity"][-1],
                                            "CN"    :   DB_CN.get(key, skip)["name"].strip(),
                                            "EN"    :   f'\'{wiki_story(DB_EN.get(key, skip)["name"]).strip()}',
                                            "JP"    :   DB_JP.get(key, skip)["name"].strip(),
                                            "KR"    :   f'\'{wiki_story(DB_KR.get(key, skip)["name"]).strip()}',
                                            "RU"    :   DB_EN.get(key, skip)["appellation"].strip(),
                                            "class" :   CLASS_PARSE_EN.get(char_class, "Token"),
                                            "sub"   :   SUBCLASS[char_sub_class]["subProfessionName"] if char_sub_class in SUBCLASS.keys() else SUBCLASS_CN.get(char_sub_class, char_sub_class.capitalize())
                                        }
    df_key = ["key"]
    for key in temp.keys():
        df_key += list(temp[key].keys())
        break
    
    printr("df_key", df_key)
    #exit()
    
    df_list = [[] for _ in range(len(df_key))]
    for char in sorted(temp.keys()):
        for key in df_key:
            if key != "key":
                df_list[df_key.index(key)].append(temp[char][key])
            else:
                df_list[0].append(char)
    dataframe = {key:df_list[df_key.index(key)] for key in df_key}
    df = pd.DataFrame(data = dataframe)
    with pd.ExcelWriter("py/script.xlsx") as writer:
        df.to_excel(writer, sheet_name = "Detail", index = False)
    
    script_result(temp, show)

#char_name(False)

def cc_risk(show : bool = False):
    runes = {}
    
    getinfo_path = r'C:\Users\computer\Downloads\getinfo-1.json'
    getinfo_json = json.load(open(getinfo_path, 'r'))
    
    mapDetailDataMap = getinfo_json["info"]["mapDetailDataMap"]
    for map in mapDetailDataMap.keys():
        for rune in mapDetailDataMap[map]["runeDataMap"].keys():
            rune_data = mapDetailDataMap[map]["runeDataMap"][rune]
            runes[rune_data["runeName"]] = rune_data["runeIcon"].split("g_", 1)[-1]
    
    runes_result = {k:runes[k] for k in sorted(runes.keys())}
    script_result(runes_result, show)
#cc_risk(True)

# ig 1 stage description - https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/en/gamedata/excel/stage_table.json
def ig1_stages():
    ig_data = {}
    get_data = json.load(open(r'py\temp_stage.json', 'r', encoding="utf-8"))
    for stage_key in get_data["stages"].keys():
        if stage_key.find("act1multi") != -1:
            ig_data[get_data["stages"][stage_key]["code"]] = {"name" : get_data["stages"][stage_key]["name"], "stage_desc" : get_data["stages"][stage_key]["description"],}
    script_result(ig_data, True, key_sort = True, forced_txt = True, no_tab=True)
    
# ig 1 mission - https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/en/gamedata/excel/activity_table.json
def ig1_mission():
    ig_mission = {}
    ig_mission_txt = []
    items = {"act1multi_token_cap" : "Participation Certification S1"}
    get_data = json.load(open(r'py\temp_activity.json', 'r', encoding="utf-8"))
    for misson_data in get_data["missionData"]:
        if misson_data["missionGroup"] == "act1multi":
            title_id    =   get_data["activity"]["MULTIPLAY_V3"]["act1multi"]["missionTitleDict"][misson_data["id"]]
            title_name  =   get_data["activity"]["MULTIPLAY_V3"]["act1multi"]["titleDataDict"][title_id]["titleDesc"]
            title_pos   =   "back" if get_data["activity"]["MULTIPLAY_V3"]["act1multi"]["titleDataDict"][title_id]["isBack"] else "front"
            ig_mission[misson_data["sortId"]] = {
                                                    "id"            : misson_data["id"],
                                                    "description"   : misson_data["description"],
                                                    "rewards"       : "\n".join([f'{items.get(reward["id"], reward["id"])}, {reward["count"]}' for reward in misson_data["rewards"]]),
                                                    "title"         : title_name,
                                                    "title_pos"     : title_pos,
                                                }
            ig_mission_txt.append([f'{{{{Event mission cell|mission={misson_data["description"]}.|currency={"\n".join([f'{items.get(reward["id"], reward["id"])},{reward["count"]}' for reward in misson_data["rewards"]])}|igtitle={title_name}, {title_pos}}}}}', misson_data["sortId"]])
    #printr(len(ig_mission.keys()))
    #printr(ig_mission_txt)
    script_result({key:ig_mission[key] for key in sorted(ig_mission.keys(), key = lambda k : int(k))}, True)
    script_result([text[0] for text in sorted(ig_mission_txt, key = lambda mission : int(mission[1]))])

#ig1_mission()

def navbox_list(item_list : list):
    printr(f'{"\n".join([f'*[[{item}]]' for item in sorted(item_list)])}')

#navbox_list(["Facility Builder", "Expert Facility Builder", "Collapsed Junk Pile", "Construction Workshop", "Recuperation Pod", "Hydraulic Platform", "Concrete Roadblock", "Portable Exercise Rack",] + ["Cheerleader", "Protective Gear Giver", "Chaotic Fireworks", "Beastmode Energy Drink", "Soda Dispenser"])

def rename_enemies() -> str :
    with open("py/input_script.txt", 'r', encoding="utf-8") as file_text:
        text = "".join(file_text.readlines())
    
    ori_text = text
    rename_dict = {
                    "Befuddled Repair Assistant" : "Confused Maintenance Helper",
                    "Uncontrollable Repair Assistant" : "Rampaging Maintenance Helper",
                    "Iced Beverage Machine" : "Cold Drink Machine",
                    "Hot Beverage Machine" : "Hot Drink Machine",
                    "Foolproof Freight Carrier" : "Worry-Free Cargo Helper",
                    "Blastproof Freight Carrier" : "Blast-Proof Cargo Helper",
                    "Echo of the Frozen Monstrosity" : "Frozen Monstrosity's Echo",
                    "Beta Food Delivery Terminal" : "Mockup Auto Meal Distributor",
                    "Food Delivery Terminal Prototype" : "Prototype Auto Meal Distributor",
                    "Solid Originium Colossus" : "Solidified Originium Colossus",
                    "Stable Crystallized Sarkaz Caster" : "Stable Sarkaz Caster Crystal",
                    "Active Crystallized Sarkaz Caster" : "Active Sarkaz Caster Crystal",
                    "Static Illusion α" : "Static Oneiros α",
                    "Static Illusion β" : "Static Oneiros β ",
                    "Translation Base α" : "Decode Basis α",
                    "Translation Base β" : "Decode Basis β",
                    "Weakened Node" : "Weakening Node",
                    }

    for name_before, name_after  in rename_dict.items():
        text = text.replace(name_before, name_after)
        
    if text == ori_text:
        printr(f'Text {R}not{RE} changed')
    else:
        printr(f'Text has been {G}changed')
    script_result(text, show = (text != ori_text))
    
#rename_enemies()

def stage_desc(stage_name : str|list) -> NoneType :
    stage_result = {}
    if isinstance(stage_name, str):
        stage_name = [stage_name]
    stage_temp = json_load(r"py\temp_stage.json", temp=True)["stages"]
    for stage in stage_temp.keys():
        if set([stage.find(name) for name in stage_name]) != {-1}:
            stage_result[stage] = {
                                        "levelId"   : stage_temp[stage]["levelId"],
                                        "zoneId"    : stage_temp[stage]["zoneId"],
                                        "code"      : stage_temp[stage]["code"],
                                        "name"      : stage_temp[stage]["name"],
                                        "description": wiki_stage(stage_temp[stage]["description"]),
            }
    script_result(stage_result, forced_txt=True, show=True)

#stage_desc("hard_15")

def map_grid(grid_value : str) -> NoneType :
    def get_grid(coord : str):
        X = coord.split(",")[0]
        Y = coord.split(",")[1]
        return f'{{{{Pos|{chr(ord("A") + int(X))}{int(Y) + 1}}}}}'
    
    grid_list = grid_value.replace("(", "").replace(")", "").split("|")
    printr(join_and(sorted([get_grid(coord) for coord in grid_list])))
#map_grid("(4,1)|(4,10)")

def input_script(script : Literal["txt", "json"] = "txt"):
    if script == "txt":
        with open("py/input_script.txt", 'r', encoding="utf-8") as file_text:
            text = "".join(file_text.readlines())
        return text
    else:
        return json_load("py/input_script.json", temp=True)

#print(wiki_story(input_script(), join_str="\n"))
#temp_script = input_script("json")
#temp_out = {}
#for stage in temp_script.keys():
#    temp_out[stage] = {"runes" : temp_script[stage]["runes"], "globalBuffs" : temp_script[stage]["globalBuffs"]}
#script_result(temp_out)

#printr(f'{30.100010000000:.0%}')

def enemy_wave_csv():
    all_stage_dict = {}
    #all_stage = glob.glob(r'C:/Github/AN-EN-Tags/json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\obt\main\*16-*')
    all_stage = glob.glob(r'C:/Github/AN-EN-Tags/json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\activities\act46side\*')
    for stage in all_stage:
        stage_id = stage.split("\\")[-1].split(".json")[0]
        stage_json = json_load(stage, temp=True)
        all_stage_dict[stage_id] = {
                                        "options"       : stage_json["options"],
                                        "runes"         : stage_json["runes"],
                                        "globalBuffs"   : stage_json["globalBuffs"],
                                        "branches"      : stage_json["branches"],
                                    }
        stage_waves = []
        for wave in stage_json["waves"]:
            curr_wave = {"advancedWaveTag" : wave["advancedWaveTag"]}
            curr_fragment = []
            for fragment in wave["fragments"]:
                curr_action = []
                spawn_key = ""
                for action in fragment["actions"]:
                    if action["randomSpawnGroupKey"] and action["randomSpawnGroupPackKey"]:
                        spawn_key = action["randomSpawnGroupKey"]
                    elif not action["randomSpawnGroupKey"] and not action["randomSpawnGroupPackKey"]:
                        spawn_key = ""
                    action_detail = {
                                    "actionType"                : action["actionType"],
                                    "key"                       : action["key"],
                                    "count"                     : action["count"],
                                    "preDelay"                  : action["preDelay"],
                                    "interval"                  : action["interval"],
                                    "hiddenGroup"               : action["hiddenGroup"],
                                    "randomSpawnGroupKey"       : spawn_key if spawn_key else action["randomSpawnGroupKey"],
                                    "randomSpawnGroupPackKey"   : action["randomSpawnGroupPackKey"],
                                    "weight"                    : action["weight"],
                                }
                    curr_action.append(action_detail)
                curr_fragment.append(curr_action)
            curr_wave["fragments"] = curr_fragment
            stage_waves.append(curr_wave)
        all_stage_dict[stage_id]["waves"] = stage_waves
    
    script_result(all_stage_dict)
    
    # txt
    script_txt = []
    for stage in all_stage_dict:
        script_txt.append(f'\n{stage}')
        script_txt.append(f'{"wave":>5}{"frag":>5}{"action":>10}{"group":^8}{"GroupKey":<10}{"GroupPack":<10}{"key":^20}{"count":<6}{"preDelay":>10}{"interval":>10}{"weight":<6}')
        for i in range(len(all_stage_dict[stage]["waves"])):
            for j in range(len(all_stage_dict[stage]["waves"][i]["fragments"])):
                for action in all_stage_dict[stage]["waves"][i]["fragments"][j]:
                    hiddenGroup             = action["hiddenGroup"] or ""
                    randomSpawnGroupKey     = action["randomSpawnGroupKey"] or ""
                    randomSpawnGroupPackKey = action["randomSpawnGroupPackKey"] or ""
                    script_txt.append(f'{i:^5}{j:^5}{action["actionType"].split("_")[0]:<10}{hiddenGroup:<8}{randomSpawnGroupKey:^10}{randomSpawnGroupPackKey:^10}{action["key"]:<20}{action["count"]:>6}{action["preDelay"]:^10}{action["interval"]:^10}{action["weight"]:>6}')
    #script_result(script_txt, True)
    
    #csv
    script_txt = []
    script_txt.append("stage|wave|frag|action|group|GroupKey|GroupPack|key|name|ID|Class|count|preDelay|interval|weight")
    for stage in all_stage_dict:
        for i in range(len(all_stage_dict[stage]["waves"])):
            for j in range(len(all_stage_dict[stage]["waves"][i]["fragments"])):
                for action in all_stage_dict[stage]["waves"][i]["fragments"][j]:
                    hiddenGroup             = action["hiddenGroup"] or "-"
                    randomSpawnGroupKey     = action["randomSpawnGroupKey"] or "-"
                    randomSpawnGroupPackKey = action["randomSpawnGroupPackKey"] or "-"
                    try :
                        key_name    = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["name"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else (DB["json_characterEN"][action["key"].split("#")[0]]["name"] if action["key"].startswith(("char", "token", "trap")) else action["key"])
                        key_id      = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else "-"
                        key_class   = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else "-"
                    except KeyError:
                        key_name    = f'{DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["name"]}({action["key"]})' if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else (f'{DB["json_character"][action["key"].split("#")[0]]["name"]}({action["key"]})' if action["key"].startswith(("char", "token", "trap")) else action["key"])
                        key_id      = DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else "-"
                        key_class   = DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else "-"
                    script_txt.append(f'{stage}|{i}|{j}|{action["actionType"].split("_")[0]}|{hiddenGroup}|{randomSpawnGroupKey}|{randomSpawnGroupPackKey}|{action["key"]}|{key_name}|{key_id}|{key_class}|{action["count"]}|{action["preDelay"]}|{action["interval"]}|{action["weight"]}')
    if all_stage_dict[stage]["branches"]:
        for branch in all_stage_dict[stage]["branches"]:
            for k in range(len(all_stage_dict[stage]["branches"]["phases"])):
                for action in range(len(all_stage_dict[stage]["branches"]["phases"][k]["action"])):
                    hiddenGroup             = f'{branch} | {action["hiddenGroup"]}' if action["hiddenGroup"] else branch
                    randomSpawnGroupKey     = action["randomSpawnGroupKey"] or "-"
                    randomSpawnGroupPackKey = action["randomSpawnGroupPackKey"] or "-"
                    try :
                        key_name    = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["name"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else (DB["json_characterEN"][action["key"].split("#")[0]]["name"] if action["key"].startswith(("char", "token", "trap")) else action["key"])
                        key_id      = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else "-"
                        key_class   = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else "-"
                    except KeyError:
                        key_name    = f'{DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["name"]}({action["key"]})' if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else (f'{DB["json_character"][action["key"].split("#")[0]]["name"]}({action["key"]})' if action["key"].startswith(("char", "token", "trap")) else action["key"])
                        key_id      = DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else "-"
                        key_class   = DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else "-"
                    script_txt.append(f'{stage}|{i}|{j}|{action["actionType"].split("_")[0]}|{hiddenGroup}|{randomSpawnGroupKey}|{randomSpawnGroupPackKey}|{action["key"]}|{key_name}|{key_id}|{key_class}|{action["count"]}|{action["preDelay"]}|{action["interval"]}|{action["weight"]}')
    script_result(script_txt, True)
    
enemy_wave_csv()

#printr(bin(639), bin(96), bool("1"), bool("0"))

def editor_trim():
    temp_editor = []
    with open("editor.txt", "r", encoding="utf-8") as editor_file:
        editor_line = editor_file.readlines()
        for line in editor_line:
            if not line.startswith(("[")):
                temp_editor.append(line)
            elif line.startswith(("[name=")):
                temp_editor.append(re.sub(r'^\[name="(.+?|)"\](.+?)$', r'\1\t\2', line))
            elif line.startswith(("[Decision(options=")):
                temp_editor.append(f'Doctor\t{" / ".join(re.match(r'^\[Decision\(options="(.+?)".+?$', line).group(1).split(";"))}')
            elif line.startswith(("[Dialog(head=")):
                char_id = re.match(r'^\[Dialog\(head="(.+?|)".+?\](.+?)$',line).group(1)
                char_name = DB["json_characterEN"][char_id]["name"] if char_id in DB["json_characterEN"] else DB["json_character"][char_id]["appellation"]
                temp_editor.append(re.sub(r'^\[Dialog\(head="(.+?|)".+?\](.+?)$', rf'{char_name}\t\2', line))
    with open("editor.txt", "w", encoding="utf-8") as editor_file:
        editor_file.write("\n".join(temp_editor).replace(" ", " ").replace("’", "'").replace("’", "'"))

#editor_trim()

def crimson_plays():
    plays_list = []
    plays_json = input_script("json")
    for play in plays_json:
        play_name = replace_apos_between(plays_json[play]["name"])
        prev_play_name = play_name.split("Crimson ")[-1]
        prev_play_link = f'{wiki_trim(prev_play_name, False)}|{prev_play_name}' if wiki_trim(prev_play_name, False) != prev_play_name else prev_play_name
        play_article_desc = f"'''{play_name}''' is a [[Play#Crimson Troupe Plays|Crimson Troupe Play]] variant of [[{prev_play_link}]] in [[Phantom & Crimson Solitaire]]."
        play_article = f'''
                        {{{{Item infobox
                        |name = {wiki_trim(plays_json[play]["name"], False)}
                        |title = {play_name}
                        |type = [[Phantom & Crimson Solitaire]] [[Play]]}}}}
                        {play_article_desc}

                        {{{{Item description|{wiki_story(plays_json[play]["usage"])}|{wiki_story(plays_json[play]["description"])}}}}}

                        ==Effect==
                        {{{{Stub}}}}

                        {{{{IS items}}}}
                        [[Category:Plays]]
                        '''.replace("                        ","")
        play_module = f'["{wiki_trim(plays_json[play]["name"], False)}"]={{name="{wiki_trim(plays_json[play]["name"], False).replace('"','\\"')}", title="{play_name}", use="{wiki_story(plays_json[play]["usage"])}", desc="{wiki_story(plays_json[play]["description"])}"}}'
                        
        plays_list.append(play_module)
    script_result(plays_list, True)
#crimson_plays()

def nation_track():
    tracker = {}
    #character_table = json_load(r"py\character_table.json", temp=True)
    character_table = DB["json_characterEN"]
    for char in character_table:
        if not [x for x in character_table[char]["mainPower"].values() if x]:
            continue
        else:
            tracker[char] = {
                                "main"      : character_table[char]["mainPower"],
                                "hidden"    : character_table[char]["subPower"],
                            }
    tracker = {k:tracker[k] for k in sorted(tracker.keys())}
    script_result(tracker, True,)
#nation_track()

def hot_diff():
    new_hot = {abInfos["name"]:abInfos for abInfos in json_load(r"py\hot_update_list (23-07-05-12-45-41-2d576e).json", True)["abInfos"]}
    old_hot = {abInfos["name"]:abInfos for abInfos in json_load(r"py\hot_update_list (23-06-25-13-09-13-327c56).json", True)["abInfos"]}
    diff_hot = {"key" : []}
    '''
    for abInfos in new_hot:
        if abInfos not in old_hot or new_hot[abInfos]["md5"] != old_hot[abInfos]["md5"]:
            diff_hot["key"].append(abInfos)
            diff_hot[abInfos]   = new_hot[abInfos]
    '''
    for abInfos in old_hot:
        if abInfos not in new_hot or new_hot[abInfos]["md5"] != old_hot[abInfos]["md5"]:
            diff_hot["key"].append(abInfos)
            diff_hot[abInfos]   = old_hot[abInfos]
    
    script_result(diff_hot, True)
#hot_diff()