
import re
from Wiki_pyFunction import load_json, wiki_text
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
        temp_base_skill.setdefault(json_buff[skill]["roomType"], {})
        if json_buff[skill]["buffName"] not in temp_base_skill[json_buff[skill]["roomType"]].keys():
            temp_base_skill[json_buff[skill]["roomType"]][json_buff[skill]["buffName"]] = f'{{{{Base skill cell|id={skill}|name={riic_name_trim(json_buff[skill]["buffName"])}|icon=Skill-{"_".join(json_buff[skill]["skillIcon"].split("_")[1:])}.png|desc={wiki_text(json_buff[skill]["description"])}}}}}'

    for key in temp_base_skill.keys():
        printr(key)
        sort_key = lambda x : x.replace("'", "").replace(".", "").replace(" ", "").replace("·", "").replace("Æ", "ae").lower()
        keys = sorted(temp_base_skill[key].keys(), key = sort_key)
        temp_base_skill[key] = {riic_name_trim(k):temp_base_skill[key][k] for k in keys}

    return {k:temp_base_skill[k] for k in sorted(temp_base_skill.keys())}

if __name__ == "__main__":
    show = False
    wiki_base_skill_json = wiki_base_skill()
    script_result(wiki_base_skill_json, show, forced_txt = True)
    script_result(wiki_base_skill_json, show)