import re
from pyFunction import json_load, printc, printr, script_result
from pyFunction_Wiki import wiki_story, wiki_text

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

get_type_list = ["TRADE",]
get_item_list = []

eventType_dict = {"base" : {}, "sky" : {}}

enter_choiceScenes = []
enter_endingDetailList= []
choice_funcIconId = []

for choiceScene in choiceScenes:
    if re.match(r'scene_ro5_.+?_enter', choiceScene):
        enter_choiceScenes.append(choiceScene)

for endingDetail in endingDetailList:
    if endingDetail.get("choiceSceneId") and re.match(r'scene_ro5_.+?_enter', endingDetail["choiceSceneId"]):
        enter_endingDetailList.append(endingDetail["choiceSceneId"])

for choice in choices:
    if choices[choice].get("displayData") and choices[choice]["displayData"].get("funcIconId"):
        choice_funcIconId.append(choices[choice]["displayData"]["funcIconId"])

#printc(enter_choiceScenes, set(enter_endingDetailList), [x for x in enter_choiceScenes if not x in set(enter_endingDetailList)])
#print(sorted(set(choice_funcIconId)))

def get_type(choice_data : dict):
    type_dict = {
                    #"initial_reward_shield"    : "Get Objective Shield",
                    #"initial_reward_unknown"   : "Unknown",
                    #"initial_reward_gold"      : "Get Ingot",
                    
                    "adventure"         : "Dispatch",
                    "battle"            : "Battle",
                    "candle_duel"       : "Pathfinder Duel",
                    "copper"            : "Get Tongbao",
                    "copper_drop"       : "Toss Tongbao",
                    "duel"              : "Face-Off IS6",
                    "gold"              : "Get Ingot",
                    "hp"                : "Get LP",
                    "hpmax"             : "Get LP",
                    "leave"             : "Leave",
                    "member"            : "Squad Size Up",
                    "population"        : "Get Hope",
                    "recruit"           : "Get Rec Voucher",
                    "relic"             : "Get Collectible",
                    "sacrifice"         : "Barter",
                    "sacrifice_copper"  : "Exchange Tongbao",
                    "shield"            : "Get Objective Shield",
                    "sp_zone_ap"        : "Get Candles",
                    "stashed_recruit"   : "Conserved Rec Voucher",
                    "teleport"          : "Secret Found",
                    "unknown"           : "Unknown",
                }

    #printc(choice_data["type"], choice_data["displayData"]["type"], choice_data["displayData"]["costHintType"], choice_data["displayData"]["effectHintType"], choice_data["displayData"])
    #exit()
    return type_dict.get(choice_data.get("icon"), "<!-- New Icon -->")

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

for floor in eventType_dict:
    for nodeType in eventType_dict[floor]:
        choiceScenes_list.append(f'# {eventType_dict[floor][nodeType]["name"]}')
        choiceScene_sorted = sorted(eventType_dict[floor][nodeType]["enter"], key = lambda x : wiki_story(choiceScenes[x]["title"]))
        for choiceScene in choiceScene_sorted:
            choiceScenes_dict[choiceScene] = choiceScenes[choiceScene]
            choiceScenes_list.append(f'''## {choiceScene}
                                        {{{{IS event start
                                        |title = {wiki_story(choiceScenes[choiceScene]["title"])}
                                        |image = {pic_archive[choiceScenes[choiceScene]["background"]]["desc"]}
                                        |intro = {wiki_text(choiceScenes[choiceScene]["description"])}
                                        |note = 
                                        }}}}'''.replace("                                        ", ""))
            for choice in choices:
                if re.match(rf'choice_ro5_{choiceScene.split("_")[2]}_.+?', choice):
                    choiceScenes_list.append(f'''{{{{IS decision
                                                |no = {choice.split("_")[-1]}
                                                |option = {choices[choice]["title"]}
                                                |item = {items[choices[choice]["displayData"]["itemId"]]["name"] if choices[choice]["displayData"].get("itemId") and choices[choice]["type"] in get_item_list else ""}
                                                {f'|type = {get_type(choices[choice])}' if choices[choice].get("icon") else ""}
                                                |desc = {wiki_text(choices[choice]["description"])}
                                                {f'|req = {wiki_text(choices[choice]["lockedCoverDesc"][1:-1])}' if choices[choice].get("lockedCoverDesc") else ""}
                                                |outcome = {wiki_text(choiceScenes[choices[choice]["nextSceneId"]]["description"]) if choices[choice].get("nextSceneId") else ""}
                                                |result = 
                                                }}}}'''.replace("                                                ", "").replace("\n\n", "\n"))
            choiceScenes_list.append("{{IS event end}}\n")
script_result(choiceScenes_list, True)