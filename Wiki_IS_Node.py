import json
import re
from typing import Literal
from pyFunction import B, R, RE, Y, json_load, printc, printr, script_result
from pyFunction_Wiki import wiki_story, wiki_text, wiki_trim

json_roguelike      = json_load(r'py\roguelike_topic_table.json', internal = True)
json_story_review   = json_load(r'py\story_review_meta_table.json', internal = True)


pic_archive         = json_story_review["actArchiveResData"]["pics"]

choices             = json_roguelike["details"]["rogue_5"]["choices"]
choiceScenes        = json_roguelike["details"]["rogue_5"]["choiceScenes"]
endingDetailList    = json_roguelike["details"]["rogue_5"]["endingDetailList"]
items               = json_roguelike["details"]["rogue_5"]["items"]

choiceScenes_dict = {}
choiceScenes_keys = []
choiceScenes_list = []
choiceScenes_used = []

get_type_list = ["TRADE",]
get_item_list = []

eventType_dict = {"base" : {}, "sky" : {}}

enter_choiceScenes = []
enter_endingDetailList = []
enter_non_ending = []
choice_funcIconId = []

skip_scene = ["startbuff"]

for choiceScene in choiceScenes:
    if re.match(r'scene_ro5_.+?_enter', choiceScene):
        enter_choiceScenes.append(choiceScene)

for endingDetail in endingDetailList:
    if endingDetail.get("choiceSceneId") and re.match(r'scene_ro5_.+?_enter', endingDetail["choiceSceneId"]):
        enter_endingDetailList.append(endingDetail["choiceSceneId"])

for choice in choices:
    if choices[choice].get("displayData") and choices[choice]["displayData"].get("funcIconId"):
        choice_funcIconId.append(choices[choice]["displayData"]["funcIconId"])

enter_non_ending = sorted([x for x in enter_choiceScenes if not x in set(enter_endingDetailList)], key = lambda y : wiki_trim(choiceScenes[y]["title"]))
#printc(enter_choiceScenes, set(enter_endingDetailList), enter_non_ending)
#printc(enter_choiceScenes, set(enter_endingDetailList), [x for x in enter_choiceScenes if not x in set(enter_endingDetailList)])
#print(sorted(set(choice_funcIconId)))
printc(sorted(set([choiceScenes[x]["title"] for x in enter_choiceScenes]), key = lambda y : wiki_trim(y).replace("'", "").replace("\"", "").replace(".", "").replace(" ", "").replace("·", "").replace("Æ", "ae").lower()))

def get_type(choice_data : dict):
    type_dict = {
                    #"initial_reward_shield"    : "Get Objective Shield",
                    #"initial_reward_unknown"   : "Unknown",
                    #"initial_reward_gold"      : "Get Ingot",
                    
                    "adventure"         : "Dispatch",
                    "battle"            : "Battle",
                    "candle_duel"       : "Challenge Candleholder",
                    "copper"            : "Get Tongbao",
                    "copper_drop"       : "Tongbao Toss",
                    "duel"              : "Face-Off 2",
                    "gold"              : "Get Ingot",
                    "hp"                : "Get LP",
                    "hpmax"             : "Get LP",
                    "leave"             : "Leave",
                    "member"            : "Squad Size Up",
                    "population"        : "Get Hope",
                    "recruit"           : "Get Rec Voucher",
                    "relic"             : "Get Collectible",
                    "sacrifice"         : "Barter",
                    "sacrifice_copper"  : "Tongbao Exchange",
                    "shield"            : "Get Objective Shield",
                    "sp_zone_ap"        : "Decide",
                    "stashed_recruit"   : "Use Conserved Voucher",
                    "teleport"          : "Secret Found",
                    "unknown"           : "Unknown",
                }
    #printc(choice_data["type"], choice_data["displayData"]["type"], choice_data["displayData"]["costHintType"], choice_data["displayData"]["effectHintType"], choice_data["displayData"])
    #exit()
    return type_dict.get(choice_data["displayData"].get("funcIconId"), "<!-- New Icon -->") if choice_data["displayData"].get("funcIconId") else ""

def choice_article(choiceScene : str):
    def scene_list(scene : str, mode : Literal["choice", "scene"]):
        match mode:
            case "choice":
                choice          = scene
                scene_option    = choices[choice]["title"]
                scene_item      = re.sub(r'^(Bal:|Flower:|Risk:)', "Tongbao-", items[choices[choice]["displayData"]["itemId"]]["name"], 1) if choices[choice].get("displayData") and choices[choice]["displayData"].get("itemId") and choices[choice]["displayData"].get("type") == "ITEM" else ""
                scene_type      = get_type(choices[choice])
                scene_desc      = wiki_text(choices[choice]["description"])
                scene_req       = wiki_text(choices[choice]["lockedCoverDesc"][1:-1]) if choices[choice].get("lockedCoverDesc") else ""
                scene_outcome   = wiki_story(choiceScenes[choices[choice]["nextSceneId"]]["description"]) if choices[choice].get("nextSceneId") else ""
                scene_result    = f'\n<!-- forceShowWhenOnlyLeave -->' if choices[choice]["forceShowWhenOnlyLeave"] else ""
            case "scene":
                scene_option    = ""
                scene_item      = ""
                scene_type      = ""
                scene_desc      = ""
                scene_req       = ""
                scene_outcome   = choiceScenes[scene]["description"]
                scene_result    = ""
            case _:
                printr(f'{Y}scene_list {RE}mode {R}ERROR !!! : mode = {B}{mode}')
            
        choiceScenes_list.append(f'''{{{{IS decision
                                        |no = {scene.split("_")[-1]}
                                        |option = {scene_option}
                                        |item = {scene_item}
                                        {f'|type = {scene_type}' if scene_type else ""}
                                        |desc = {scene_desc}
                                        {f'|req = {scene_req}' if scene_req else ""}
                                        |outcome = {scene_outcome}
                                        |result = {scene_result}
                                        }}}}'''.replace("                                        ", "").replace("\n\n", "\n"))
    
    isChoice    = False
    isScene     = False
    choiceScenes_used.append(choiceScene)
    choiceScenes_list.append(f'''## {choiceScene}
                                        {{{{IS event start
                                        |title = {wiki_text(choiceScenes[choiceScene]["title"])}
                                        |image = {pic_archive[choiceScenes[choiceScene]["background"]]["desc"]}
                                        |intro = {wiki_story(choiceScenes[choiceScene]["description"])}
                                        |note = 
                                        }}}}'''.replace("                                        ", ""))
    
    for choice in choices:
        if re.match(rf'choice_{"_".join(choiceScene.split("_")[1:3])}_.+?', choice):
            isChoice = True
            if choices[choice].get("nextSceneId"):
                choiceScenes_used.append(choices[choice]["nextSceneId"])
            scene_list(choice, "choice")
        elif isChoice:
            break
    
    for scene in choiceScenes:
        if re.match(rf'{"_".join(choiceScene.rsplit("_", 1)[0])}_.+?', scene) and scene not in choiceScenes_used:
            isScene = True
            scene_list(scene, "scene")
        elif isScene:
            break
        
    choiceScenes_list.append("{{IS event end}}\n")

def wiki_is_node():
    for endingDetail in endingDetailList:
        if not endingDetail.get("choiceSceneId"):
            continue
        if endingDetail.get("spZoneEvtType"):
            spZoneEvtType = endingDetail["spZoneEvtType"]
            eventType_dict["sky"].setdefault(spZoneEvtType, {}).setdefault("name", json_roguelike["modules"]["rogue_5"]["sky"]["nodeData"][spZoneEvtType]["name"])
            if "enter" not in eventType_dict["sky"][spZoneEvtType]:
                eventType_dict["sky"][spZoneEvtType]["enter"] = []
            eventType_dict["sky"][spZoneEvtType]["enter"].append(endingDetail["choiceSceneId"])
        elif endingDetail.get("eventType"):
            eventType = endingDetail["eventType"]
            eventType_dict["base"].setdefault(eventType, {}).setdefault("name", json_roguelike["details"]["rogue_5"]["nodeTypeData"][eventType]["name"])
            if "enter" not in eventType_dict["base"][eventType]:
                eventType_dict["base"][eventType]["enter"] = []
            eventType_dict["base"][eventType]["enter"].append(endingDetail["choiceSceneId"])

    '''
    for choiceScene in choiceScenes:
        if re.match(r'scene_ro5.+?_enter', choiceScene) and choiceScenes[choiceScene].get("background"):
            choiceScenes_keys.append((choiceScene, choiceScenes[choiceScene]["title"]))
    '''
    # Ending list
    for floor in eventType_dict:
        if ALL: break
        for nodeType in eventType_dict[floor]:
            choiceScenes_list.append(f'# {eventType_dict[floor][nodeType]["name"]}')
            choiceScene_sorted = sorted(eventType_dict[floor][nodeType]["enter"], key = lambda x : wiki_trim(choiceScenes[x]["title"]))
            for choiceScene in choiceScene_sorted:
                choiceScenes_dict[choiceScene] = choiceScenes[choiceScene]
                choice_article(choiceScene)

    #The Rest
    choiceScenes_list.append("# Non-Ending list\n")
    for enterScene in enter_non_ending:
        if ALL: break
        isEnter = False
        #printr(enterScene)
        if enterScene.split("_")[2] in skip_scene:
            continue
        else:
            choice_article(enterScene)
    
    if ALL:
        choiceScenes_list.append("# All Node\n")
        for enterScene in enter_choiceScenes:
            if enterScene.split("_")[2] in skip_scene:
                continue
            else:
                choice_article(enterScene)
    
    return choiceScenes_list

ALL = True

script_result(wiki_is_node(), True)