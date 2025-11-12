import json
import re
from typing import Any, Literal

import requests
from pyFunction import printr, script_result
from pyFunction_Wiki import load_json, replace_apos_between, wiki_story

used_json = "json_medalEN"

DB = load_json(used_json)

def medal_article(medal_id : str, group_type : Literal["activityMedal", "rogueMedal"] = "activityMedal"):
    def wikitrim_method(desc : str, Event_name : str = "") -> str:
        if desc:
            trim_desc = re.sub("^During the event (.+?), ", "", desc)
            return replace_apos_between(trim_desc[0].upper() + trim_desc[1:])
        else:
            return f'Awarded once all other {Event_name if Event_name else "{{Color|Event name goes here|code=f00}}"} medals are obtained.'
    
    medal_dict = {}
    medal_text = []
    medal_rarity_dict = {"T3" : "gold", "T2" : "silver", "T1" : "bronze"}
    Event_name = ""
    
    get_data = DB["json_medalEN"]
    #get_data = json.load(open(r'py\temp_medal.json', 'r', encoding="utf-8"))
    #get_data = json.loads(requests.get(r'https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/en/gamedata/excel/medal_table.json').text)
    #printr(get_data)
    
    #medal_group
    for group in get_data["medalTypeData"][group_type]["groupData"]:
        if group["medalId"][0].find(medal_id) != -1:
            group_title = group["groupName"]
            group_set   = group["groupName"].replace("#", "")
            group_desc  = group["groupDesc"]
            Event_name  = group_title.replace(" Engraved Medal Set", "")
            medal_text.append(f'''{{{{Medal head
                                    |titlecolor = 
                                    {f'|title = {group_title}' if group_title != group_set else ""}
                                    |set = {group_set}
                                    |desc = {wiki_story(group_desc)}}}}}'''.replace("                                    ", "").replace("\n\n", "\n"))
            break
    
    #medal_piece list
    for medal in get_data["medalList"]:
        if medal["medalId"].find(medal_id) != -1:
            if medal.get("originMedal", ""):
                medal_dict[medal["slotId"]].update({"trim" : wikitrim_method(medal.get("getMethod", ""), Event_name)})
            else :
                medal_dict[medal["slotId"]] = {
                                                "id"            : medal["medalId"],
                                                "name"          : medal["medalName"],
                                                "rarity"        : medal["rarity"],
                                                "getMethod"     : wikitrim_method(medal.get("getMethod", ""), Event_name),
                                                "description"   : replace_apos_between(medal["description"])
                                            }
    sort_medal_dict : dict[str, Any] = {key:medal_dict[key] for key in sorted(medal_dict.keys(), key = lambda k : int(k))}
    #script_result(sort_medal_dict, True)
    
    #medal_piece write
    for key in sort_medal_dict.keys():
        medal_name  = sort_medal_dict[key]["name"]
        medal_title = medal_name
        if re.match(r'^\'(.+?)\'$', medal_name):
            medal_name = re.sub(r'^\'(.+?)\'$', r'\1', medal_name)
            medal_title = f'"{medal_name}"'
        if medal_name.find(":") != -1:
            medal_name = medal_name.replace(":", "")
        medal_type  = medal_rarity_dict[sort_medal_dict[key]["rarity"]]
        medal_get   = sort_medal_dict[key]["getMethod"]
        medal_trim  = sort_medal_dict[key].get("trim", False)
        medal_desc  = sort_medal_dict[key]["description"].replace("\n", "<br/>")
        medal_text.append(f'{{{{Medal cell|name={medal_name}{f'|title={medal_title}' if medal_title != medal_name else ""}|type={medal_type}|desc={medal_desc}|cond={medal_get}{f'|trim={medal_trim}' if medal_trim else ""}}}}}')
        #printr(medal_text)
    
    if Event_name:
        medal_text.append("{{Table end}}\n{{Medal sets}}")
    script_result(medal_text, True)
    
medal_article("medal_activity_act1break", group_type = "activityMedal")