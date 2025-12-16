import re
from typing import Literal

from Wiki_OOP.stage_data import get_stage_data
from pyFunction import valid_filename

class Stage_Writer():
    def __init__(self):
        pass
    

def is_stage_writer(stage_id : str, stage_dict : dict, hard_id : str, theme : str, theme_name : str):
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
                        |event =
                        |desc = {stage_dict["stage"][stage_id]["description"]}
                        |note = }}}}'''.replace("                        ", "").replace("\n\n", "\n")
    def is_stage_data(curr_id : str, isHard : bool = False):
        print(curr_id)
        curr_data = get_stage_data(stage_dict["stage"][stage_id]["levelId"], isHard)
        return f'''{{{{IS operation data
                        |cond = {stage_dict["stage"][curr_id]["eliteDesc"] if isHard else ""}
                        |theme = {theme}
                        |unit limit = {curr_data["unit_limit"]}
                        |dp = {curr_data["dp"]}
                        |enemies = {curr_data["enemies"]}
                        |deployable = 
                        |static =
                        |terrain =
                        |addendum =
                        |normal =
                        |elite =
                        |boss =
                        |eaddendum = }}}}'''.replace("                        ", "")

    stage_code = stage_dict["stage"][stage_id]["code"]
    stage_name = stage_dict["stage"][stage_id]["name"]
    
    if hard_id:
        stage_article = [f'# {stage_id}/{hard_id} | {stage_name}', is_stage_info(), "<tabber>", "Normal=", is_stage_data(stage_id), "|-|Emergency=", is_stage_data(hard_id, True), "</tabber>"]
    else:
        stage_article = [f'# {stage_id} | {stage_name}', is_stage_info(), is_stage_data(stage_id)]
    return stage_article
