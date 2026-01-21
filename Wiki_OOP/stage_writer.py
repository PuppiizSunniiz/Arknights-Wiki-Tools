import re
from typing import Literal

from Wiki_OOP.stage_data import get_stage_data
from pyFunction import printr, valid_filename
from pyFunction_Wiki import wiki_story

class Stage_Writer():
    def __init__(self):
        pass
    

def stage_desc(desc : str):
    desc_replace_dict = {
        r'<@rolv\.rem>(.+?)<\/>'    : "{{Color|{0}|rolv}}",
        r'<@lv\.item>(.+?)<\/>'     : "{0}"
    }
    desc = wiki_story(desc)
    for desc_key, desc_replace in desc_replace_dict.items():
        if re.search(desc_key, desc):
            #printr(desc_key, desc_replace)
            desc = re.sub(desc_key, desc_replace.replace("{0}", r'\1'), desc)
    return re.sub(r'<([^/]+?)>', r"'''<[[\1]]>'''", desc.replace("\n", "<br/>"))

def is_stage_writer(stage_id : str, stage_dict : dict, hard_id : str, theme : str, theme_name : str):
    ignored_group = {
                        "6" : ["copper_b", "copper_d", "copper_r"] # Feet, mini boss, tongbao
                    }
    def is_stage_info():
        floor_string = re.match(r'ro(?:\d+)_n_(\d+)_\d+', stage_id)
        stage_floor = floor_string.group(1) if floor_string else ""
        return f'''{{{{IS operation info
                        |code = {stage_code}
                        {f'|name = {valid_filename(stage_name)}\n|title = {stage_name}' if valid_filename(stage_name) != stage_name else f'|name = {stage_name}'}
                        |theme = {theme_name}
                        |floor = {stage_floor}
                        |encounter =
                        |recreation =
                        |dreadful foe = {"true" if stage_dict["stage"][stage_id]["isBoss"] else "false"}
                        |prophecy =
                        |faceoff =
                        |pathfinder =
                        |event =
                        |desc = {stage_desc(stage_dict["stage"][stage_id]["description"])}
                        |note = 
                        }}}}'''.replace("                        ", "").replace("\n\n", "\n")
    def is_stage_data(curr_id : str, isHard : bool = False):
        #print(curr_id, ignored_group.get(theme, []))
        curr_data = get_stage_data(stage_dict["stage"][stage_id]["levelId"], isHard, ignored_group = ignored_group.get(theme, []))
        return f'''{{{{IS operation data
                        |cond = {stage_desc(stage_dict["stage"][curr_id]["eliteDesc"]) if isHard else ""}
                        |theme = {theme}
                        |unit limit = {curr_data["unit_limit"]}
                        |dp = {curr_data["dp"]}
                        |enemies = {curr_data["enemies"]}
                        |deployable = 
                        |static =
                        |terrain =
                        |addendum =
                        |normal = {curr_data["normal"]}
                        |elite = {curr_data["elite"]}
                        |boss = {curr_data["boss"]}
                        |eaddendum = 
                        }}}}'''.replace("                        ", "")

    stage_code = stage_dict["stage"][stage_id]["code"]
    stage_name = stage_dict["stage"][stage_id]["name"]
    
    if hard_id:
        stage_article = [f'# {stage_id}/{hard_id} | {stage_name}', is_stage_info(), "<tabber>", "Normal=", is_stage_data(stage_id), "|-|Emergency=", is_stage_data(hard_id, True), "</tabber>"]
    else:
        stage_article = [f'# {stage_id} | {stage_name}', is_stage_info(), is_stage_data(stage_id)]
    return stage_article
