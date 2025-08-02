
import re
from pyFunction_Wiki import load_json, wiki_text
from pyFunction import printr, script_result

used_json = [
                "json_buildingEN"
            ]
DB = load_json(used_json)

def riic_name_trim(name : str) -> str:
    name = re.sub(rf"^([^']*|)'(.+?)'([^']*|)$", r'\1"\2"\3', name)
    return name.replace("·", " ").replace("  ", " ").strip()

def wiki_base_skill(show : bool = False):
    temp_base_skill = {}
    json_buff = DB["json_buildingEN"]["buffs"]
    for skill in json_buff.keys():
        riic_buff_name = riic_name_trim(json_buff[skill]["buffName"])
        riic_buff_room = json_buff[skill]["roomType"]
        riic_buff_icon = json_buff[skill]["skillIcon"]
        riic_buff_nameid = f'{riic_buff_name} - {riic_buff_icon}'
        
        temp_base_skill.setdefault(riic_buff_room, {}).setdefault(riic_buff_nameid,{}).setdefault("id", []).append(skill)
        if "wikitext" not in temp_base_skill[riic_buff_room][riic_buff_nameid].keys():
            temp_base_skill[riic_buff_room][riic_buff_nameid]["name"] = riic_buff_name
            temp_base_skill[riic_buff_room][riic_buff_nameid]["wikitext"] = f'{{{{Base skill cell|id=|name={riic_buff_name}|icon=Skill-{"_".join(riic_buff_icon.split("_")[1:])}.png|desc={wiki_text(json_buff[skill]["description"])}}}}}'
    result_base_skill = {}
    for key in temp_base_skill.keys():
        printr(key)
        sort_key = lambda x : x.replace("'", "").replace("\"", "").replace(".", "").replace(" ", "").replace("·", "").replace("Æ", "ae").lower()
        sort_id = lambda x : x.replace("[", "").replace("]", "").lower()
        keys = sorted(temp_base_skill[key].keys(), key = sort_key)
        result_base_skill[key] = {k:temp_base_skill[key][k]["wikitext"].replace("|id=|", f'|id={", ".join(sorted(temp_base_skill[key][k]["id"], key = sort_id))}|') for k in keys}

    return {k:result_base_skill[k] for k in sorted(result_base_skill.keys())}

if __name__ == "__main__":
    show = True
    wiki_base_skill_json = wiki_base_skill()
    script_result(wiki_base_skill_json, show, forced_txt = True, txt_nokey = True, no_tab = True)
    #script_result(wiki_base_skill_json, show)