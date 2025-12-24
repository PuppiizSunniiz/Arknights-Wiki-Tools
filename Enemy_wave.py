import glob

from Wiki_Dict import ENEMY_NAMES_TL, TOKEN_NAMES_TL
from Wiki_OOP.char_data import Character_Database
from pyFunction import json_load, printr, script_result
from pyFunction_Wiki import grid_name, load_json

used_json = [
                "json_enemy_handbook",
                "json_enemy_handbookEN",
            ]

DB = load_json(used_json)
CHAR = Character_Database()

def enemy_wave_csv(all_stage : list):
    all_stage_dict = {}
    for stage in all_stage:
        if not stage.split("\\")[-1].startswith("level_"): continue
        stage_id = stage.split("\\")[-1].split(".json")[0]
        stage_json = json_load(stage, internal=True)
        printr(stage_id)
        all_stage_dict[stage_id] = {
                                        "options"       : stage_json["options"],
                                        "runes"         : stage_json.get("runes", None),
                                        "globalBuffs"   : stage_json.get("globalBuffs", None),
                                        "branches"      : stage_json.get("branches", None),
                                        "routes"        : stage_json["routes"],
                                        "extraRoutes"   : stage_json["extraRoutes"],
                                    }
        stage_waves = []
        for wave in stage_json["waves"]:
            curr_wave = {"advancedWaveTag" : wave.get("advancedWaveTag", None)}
            curr_fragment = []
            for fragment in wave["fragments"]:
                curr_action = []
                spawn_key = ""
                for action in fragment["actions"]:
                    hiddenGroup             = action.get("hiddenGroup", None)
                    randomSpawnGroupKey     = action.get("randomSpawnGroupKey", None)
                    randomSpawnGroupPackKey = action.get("randomSpawnGroupPackKey", None)
                    if randomSpawnGroupKey and randomSpawnGroupPackKey:
                        spawn_key = randomSpawnGroupKey
                    elif not randomSpawnGroupKey and not randomSpawnGroupPackKey:
                        spawn_key = ""
                    action_detail = {
                                    "actionType"                : action["actionType"],
                                    "key"                       : action["key"],
                                    "count"                     : action["count"],
                                    "preDelay"                  : action["preDelay"],
                                    "interval"                  : action["interval"],
                                    "hiddenGroup"               : hiddenGroup,
                                    "randomSpawnGroupKey"       : spawn_key if spawn_key else randomSpawnGroupKey,
                                    "randomSpawnGroupPackKey"   : randomSpawnGroupPackKey,
                                    "weight"                    : action["weight"],
                                    "routeIndex"                : action["routeIndex"],
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
    script_txt.append("stage|wave|frag|action|group|GroupKey|GroupPack|key|name|ID|Class|count|preDelay|interval|weight|route|start")
    for stage in all_stage_dict:
        for i in range(len(all_stage_dict[stage]["waves"])):
            for j in range(len(all_stage_dict[stage]["waves"][i]["fragments"])):
                for action in all_stage_dict[stage]["waves"][i]["fragments"][j]:
                    hiddenGroup             = action["hiddenGroup"] or "-"
                    randomSpawnGroupKey     = action["randomSpawnGroupKey"] or "-"
                    randomSpawnGroupPackKey = action["randomSpawnGroupPackKey"] or "-"
                    routeIndex              = action["routeIndex"]
                    startPosition           = grid_name(list(all_stage_dict[stage]["routes"][routeIndex]["startPosition"].values()))
                    try :
                        key_name    = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["name"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(action["key"].split("#")[0], TOKEN_NAMES_TL.get(action["key"].split("#")[0], CHAR.getname(action["key"].split("#")[0]) if action["key"].startswith(("char", "token", "trap")) else action["key"]))
                        key_id      = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].startswith("enemy") else "-"
                        key_class   = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].startswith("enemy") else "-"
                    except KeyError:
                        key_name    = f'{DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["name"]}({action["key"]})' if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else (f'{CHAR.getname(action["key"].split("#")[0])}({action["key"]})' if action["key"].startswith(("char", "token", "trap")) else action["key"])
                        key_id      = DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else "-"
                        key_class   = DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else "-"
                    script_txt.append(f'{stage}|{i}|{j}|{action["actionType"].split("_")[0]}|{hiddenGroup}|{randomSpawnGroupKey}|{randomSpawnGroupPackKey}|{action["key"]}|{key_name}|{key_id}|{key_class}|{action["count"]}|{action["preDelay"]}|{action["interval"]}|{action["weight"]}|{routeIndex}|{startPosition}')
    if all_stage_dict[stage]["branches"]:
        for branch in all_stage_dict[stage]["branches"]:
            for k in range(len(all_stage_dict[stage]["branches"][branch]["phases"])):
                for action in all_stage_dict[stage]["branches"][branch]["phases"][k]["actions"]:
                    hiddenGroup             = f'{branch} | {action["hiddenGroup"]}' if action["hiddenGroup"] else branch
                    randomSpawnGroupKey     = action["randomSpawnGroupKey"] or "-"
                    randomSpawnGroupPackKey = action["randomSpawnGroupPackKey"] or "-"
                    routeIndex              = action["routeIndex"]
                    startPosition           = grid_name(list(all_stage_dict[stage]["extraRoutes"][routeIndex]["startPosition"].values()))
                    try :
                        key_name    = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["name"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else ENEMY_NAMES_TL.get(action["key"].split("#")[0], TOKEN_NAMES_TL.get(action["key"].split("#")[0], CHAR.getname(action["key"].split("#")[0]) if action["key"].startswith(("char", "token", "trap")) else action["key"]))
                        key_id      = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].startswith("enemy") else "-"
                        key_class   = DB["json_enemy_handbookEN"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].split("#")[0] in DB["json_enemy_handbookEN"]["enemyData"] else DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].startswith("enemy") else "-"
                    except KeyError:
                        key_name    = f'{DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["name"]}({action["key"]})' if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else (f'{CHAR.getname(action["key"].split("#")[0])}({action["key"]})' if action["key"].startswith(("char", "token", "trap")) else action["key"])
                        key_id      = DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyIndex"] if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else "-"
                        key_class   = DB["json_enemy_handbook"]["enemyData"][action["key"].split("#")[0]]["enemyLevel"] if action["key"].split("#")[0] in DB["json_enemy_handbook"]["enemyData"] else "-"
                    script_txt.append(f'{stage}|{i}|{j}|{action["actionType"].split("_")[0]}|{hiddenGroup}|{randomSpawnGroupKey}|{randomSpawnGroupPackKey}|{action["key"]}|{key_name}|{key_id}|{key_class}|{action["count"]}|{action["preDelay"]}|{action["interval"]}|{action["weight"]}|{routeIndex}|{startPosition}')
    script_result(script_txt, True)

#all_stage = glob.glob(r'C:/Github/AN-EN-Tags/json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\obt\main\*16-*')
#all_stage = glob.glob(r'C:/Github/AN-EN-Tags/json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\activities\act2multi\**.json')
#all_stage = glob.glob(r'C:/Github/AN-EN-Tags/json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\obt\roguelike\ro4\**.json')
#all_stage = glob.glob(r'C:/Github/AN-EN-Tags/json\gamedata\ArknightsGameData\zh_CN\gamedata\levels\obt\roguelike\ro5\**.json')
all_stage = glob.glob(r'C:\Github\Arknights-Project\FBS\YoStar_out\level\**.json')

enemy_wave_csv(all_stage)