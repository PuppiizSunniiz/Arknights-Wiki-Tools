import json
import re
from typing import Any
from pyFunction import printr, script_result

def activity_medal(activity : str):
    def wikitrim_method(desc : str) -> str:
        trim_desc = desc.split(", ", 1)[-1]
        return trim_desc[0].upper() + trim_desc[1:]
    
    medal_dict = {}
    medal_text = []
    medal_rarity_dict = {"T3" : "gold", "T2" : "silver", "T1" : "bronze"}
    get_data = json.load(open(r'py\temp_medal.json', 'r', encoding="utf-8"))
    for medal in get_data["medalList"]:
        if medal["medalId"].find(activity) != -1:
            if medal.get("originMedal", ""):
                medal_dict[medal["slotId"]].update({"trim" : wikitrim_method(medal["getMethod"])})
            else :
                medal_dict[medal["slotId"]] = {
                                                "id"            : medal["medalId"],
                                                "name"          : medal["medalName"],
                                                "rarity"        : medal["rarity"],
                                                "getMethod"     : wikitrim_method(medal["getMethod"]),
                                                "description"   : medal["description"]
                                            }
    sort_medal_dict : dict[str, Any] = {key:medal_dict[key] for key in sorted(medal_dict.keys(), key = lambda k : int(k))}
    script_result(sort_medal_dict, True)
    
    #medal_group
    
    for key in sort_medal_dict.keys():
        medal_name  = sort_medal_dict[key]["name"]
        if re.match(r'^\'(.+?)\'$', medal_name):
            medal_name = re.sub(r'^\'(.+?)\'$', r'\1', medal_name)
            medal_name = f'{medal_name}|title="{medal_name}"'
        medal_type  = medal_rarity_dict[sort_medal_dict[key]["rarity"]]
        medal_get   = sort_medal_dict[key]["getMethod"]
        medal_trim  = sort_medal_dict[key].get("trim", False)
        medal_desc  = sort_medal_dict[key]["description"].replace("\n", "<br/>")
        medal_text.append(f'{{{{Medal cell|name={medal_name}|type={medal_type}|desc={medal_desc}|cond={medal_get}{f'|trim={medal_trim}' if medal_trim else ""}}}}}')
        printr(medal_text)
    script_result(medal_text, True)
    
#activity_medal("medal_stage_hard")