import json
import re

import requests
from Wiki_OOP.char_data import Character_Database
from Wiki_OOP.enemy_data import Enemy_Database
from pyFunction import B, G, json_load, printr, script_result, sorted_dict_key
from pyFunction_Wiki import load_json

used_json = [
                "json_charword",
                "json_charwordEN",
                "json_character",
                "json_characterEN",
                "json_char_patch",
                "json_char_patchEN",
            ]

DB = load_json(used_json)
DB["json_character"].update(DB["json_char_patch"]["patchChars"])
DB["json_characterEN"].update(DB["json_char_patchEN"]["patchChars"])

for ref in ["nation_track", "charWords_track", "enemy_track"]:
    DB[f'{ref}_old']    = json_load(f'tracker/ref/{ref}_old.json', True)
    DB[ref]             = json_load(f'tracker/ref/{ref}.json', True)

CN = json.loads(requests.get("https://ak-conf.hypergryph.com/config/prod/official/Android/version").text)["resVersion"]
EN = json.loads(requests.get("https://ark-us-static-online.yo-star.com/assetbundle/official/Android/version").text)["resVersion"]
CHAR = Character_Database()

def charWords_track():
    def get_char_id(char_str : str):
        return "_".join(char_str.split("#")[0].split("_")[0:3])
        
    if charWords_test: DB["json_charwordEN"] = json_load(r"py\charword_table.json", True, {"charWords" : {}, "voiceLangDict" : {}})
    
    dialogue_track : dict = DB["json_charword"]["charWords"]
    dialogue_track.update(DB["json_charwordEN"]["charWords"])

    dialogue_track = {k:dialogue_track[k]["voiceText"] for k in sorted(dialogue_track.keys())}
    
    skin_track : dict = DB["json_charword"]["voiceLangDict"]
    skin_track.update(DB["json_charwordEN"]["voiceLangDict"])
    
    skin_track = [k for k in sorted(skin_track.keys()) if re.match(r'char_\d+_[A-Za-z\d]+_[A-Za-z\d]+#\d+', k)]
    
    dialogue_diff   = {k:v for k, v in dialogue_track.items() if "dialogue_tracker" not in DB["charWords_track"] or k not in DB["charWords_track"]["dialogue_tracker"] or DB["charWords_track"]["dialogue_tracker"][k] != v}
    dialogue_diff   = {k:dialogue_diff[k] for k in sorted(dialogue_diff.keys(), key = lambda op: f'{CHAR.getrarity(get_char_id(op))} - {CHAR.getname(get_char_id(op))} - {op}')}
    skin_diff       = [k for k in skin_track if "skin_tracker" not in DB["charWords_track"] or k not in DB["charWords_track"]["skin_tracker"]]
    
    charWords_track_json    = {"CN" : CN, "EN" : EN, "dialogue_tracker" : dialogue_track, "skin_tracker": skin_track}
    charWords_diff_json     = {"CN" : CN, "EN" : EN, "dialogue_tracker" : dialogue_diff, "skin_tracker": skin_diff}
    
    if DB["charWords_track"] != charWords_track_json:
        if charWords_diff_json["dialogue_tracker"] != {} or charWords_diff_json["skin_tracker"] != {}:
            with open("tracker/charWords_diff.json", "w", encoding = "utf-8") as filepath :
                json.dump(charWords_diff_json, filepath, indent = 4, ensure_ascii = False)
        with open("tracker/ref/charWords_track_old.json", "w", encoding = "utf-8") as filepath :
            json.dump(DB["charWords_track"], filepath, indent = 4, ensure_ascii = False)
        with open("tracker/ref/charWords_track.json", "w", encoding = "utf-8") as filepath :
            json.dump(charWords_track_json, filepath, indent = 4, ensure_ascii = False)
    
def nationId_track():
    nation_track = {}

    if nationId_test:
        DB["json_character"] = json_load(r"py\character_table.json", True)
        DB["json_character"].update(DB["json_char_patch"]["patchChars"])

    for char_id in DB["json_character"].keys():
        if not [x for x in DB["json_character"][char_id]["mainPower"].values() if x]:
            continue
        else:
            nation_track[char_id] = {
                                    "main"      : DB["json_character"][char_id]["mainPower"],
                                    "hidden"    : DB["json_character"][char_id]["subPower"],
                                }

    nation_track        = {k:nation_track[k] for k in sorted(nation_track.keys())}
    nation_diff         = {k:v for k, v in nation_track.items() if "tracker" not in DB["nation_track"] or k not in DB["nation_track"]["tracker"] or DB["nation_track"]["tracker"][k] != v}
    
    nation_track_json   = {"CN" : CN, "EN" : EN, "tracker" : nation_track}
    nation_diff_json    = {"CN" : CN, "EN" : EN, "tracker" : nation_diff}
    if DB["nation_track"] != nation_track_json:
        with open("tracker/nation_diff.json", "w", encoding = "utf-8") as filepath :
                json.dump(nation_diff_json, filepath, indent = 4, ensure_ascii = False)
        with open("tracker/ref/nation_track_old.json", "w", encoding = "utf-8") as filepath :
            json.dump(DB["nation_track"], filepath, indent = 4, ensure_ascii = False)
        with open("tracker/ref/nation_track.json", "w", encoding = "utf-8") as filepath :
            json.dump(nation_track_json, filepath, indent = 4, ensure_ascii = False)

def enemyname_track():
    enemy_track         = sorted_dict_key(Enemy_Database().NAMES)
    enemy_diff          = {k:v for k, v in enemy_track.items() if "tracker" not in DB["enemy_track"] or k not in DB["enemy_track"]["tracker"] or DB["enemy_track"]["tracker"][k] != v}
    
    enemy_track_json    = {"CN" : CN, "EN" : EN, "tracker" : enemy_track}
    enemy_diff_json     = {"CN" : CN, "EN" : EN, "tracker" : enemy_diff}
    if DB["enemy_track"] != enemy_track_json:
        with open("tracker/enemy_diff.json", "w", encoding = "utf-8") as filepath :
                json.dump(enemy_diff_json, filepath, indent = 4, ensure_ascii = False)
        with open("tracker/ref/enemy_track_old.json", "w", encoding = "utf-8") as filepath :
            json.dump(DB["enemy_track"], filepath, indent = 4, ensure_ascii = False)
        with open("tracker/ref/enemy_track.json", "w", encoding = "utf-8") as filepath :
            json.dump(enemy_track_json, filepath, indent = 4, ensure_ascii = False)
    

charWords_test = False # True False
nationId_test = False # True False

if __name__ == "__main__":
    charWords_track()
    nationId_track()
    enemyname_track()
    printr(f'{B}Wiki_Text_tracker.py - {G}Completed !!!')