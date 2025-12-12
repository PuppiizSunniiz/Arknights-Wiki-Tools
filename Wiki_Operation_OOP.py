import re
from typing import Any, Literal
from Wiki_Dict import ENEMY_NAMES_TL, ITEM_NAMES_TL, SKILL_NAMES_TL, TOKEN_NAMES_TL, CLASS_PARSE_EN
from Wiki_OOP.enemy_data import Enemy_Database
from Wiki_OOP.stage_data import Stage_Database
from pyFunction_Wiki import load_json, replace_apos_between, wiki_story, wiki_trim
from pyFunction import B, G, R, RE, Y, decimal_format, falsy_compare, join_and, join_or, json_load, printc, printr, script_result

def wiki_operation(
                    event_id : str = "", 
                    event_type : Literal["episode", "intermezzo", "sidestory", "storycollection", "ig", "tn", "vb"] = "", 
                    event_name : str = "", 
                    year : str|int = ""
                    ):
    
    article_data = []
    ishard = False
    is6star = False
    
    '''
    big_data = wiki_enemies(event_code)
    big_data["enemies_stage"] = {}
    if event_type != "ig":
        for stage in big_data["stage"]:
            big_data["enemies_stage"][stage] = stage_kill_lister(big_data, stage)
    '''
    
    #script_result(big_data)
    #exit()
    # Stage article
    # - https://arknights.wiki.gg/wiki/Template:Operation_info/doc
    # - https://arknights.wiki.gg/wiki/Template:Operation_data/doc
    match event_type:
        case "ig" | "tn" | "vb":
            mode_info = event_type
            page_footer = "Seasonal game modes"
        case "sss":
            mode_info = event_type
            page_footer = "S3 operations"
        case "is":
            mode_info = event_type
            page_footer = f'IS{year} operations'
        case "intermezzo" | "sidestory" | "storycollection":
            mode_info = event_type
            page_footer = f'Y{year} event operations'
        case "episode":
            mode_info = event_type
            page_footer = "Main Theme operations"
        case _:
            mode_info = "sidestory"
            page_footer = f'Y{year} event operations'
    
    match event_type:
        case "is":
            theme_name = DB["json_roguelike_topic"][f'rogue_{year - 1}']["name"]
            for stage in STAGE["stage"]:
                if stage in STAGE["hard_dict"]:
                    continue
                hard_stage = STAGE["hard_dict"].get(stage, "")
                if hard_stage:
                    article_data += is_stage_writer(stage, STAGE, hard_stage, year, theme_name) + [f'{{{{{page_footer}}}}}']
                else:
                    article_data += is_stage_writer(stage, STAGE, year, theme_name) + [f'{{{{{page_footer}}}}}']
        case _ :
            pass
    
    '''
    for stage in big_data["stage"].keys():
        if mode_info == "sidestory":
            if stage.endswith(("#f#", "#s")): continue
            is6star = False
            ishard = False
            stage_info = stage_article_data(big_data, stage, "info")
            stage_data = stage_article_data(big_data, stage, "data")
            if big_data["stage_data"][stage]["sixStarStageId"]:
                is6star = True
                stage_data_6star = stage_article_data(big_data, stage, "data", "six")
                page_footer = "Main Theme operations"
            
            elif big_data["stage_data"][stage]["hardStagedId"]:
                ishard = True
                stage_data_hard = stage_article_data(big_data, stage, "data", "hard")
            
            if is6star:
                stage_article = [stage_article_writer(stage_info, "info"), "<tabber>", "Normal Mode=", stage_article_writer(stage_data, "data"), f'|-|{"Adverse Environment" if event_type == "episode" else "Challenge Mode"}=', stage_article_writer(stage_data_6star, "data", "Adverse"), "|-|Strategic Simulation=", stage_article_writer(stage_data_6star, "data", "Adverse", "simulation"), "</tabber>", f'{{{{{page_footer}}}}}']
            elif ishard:
                stage_article = [stage_article_writer(stage_info, "info"), "<tabber>", "Normal Mode=", stage_article_writer(stage_data, "data"), "|-|Challenge Mode=", stage_article_writer(stage_data_hard, "data"), "</tabber>", f'{{{{{page_footer}}}}}']
            else:
                stage_article = [stage_article_writer(stage_info, "info"), stage_article_writer(stage_data, "data"), f'{{{{{page_footer}}}}}']
            article_data += stage_article
        
        elif mode_info == "ig":
            stage_info = ig_article_data(big_data, stage)
            stage_article = [f'### {stage}', f'{{{{Construction}}}}', ig_article_writer(stage_info)]
            article_data += stage_article
        
        elif mode_info == "tn":
            tn_diff = ["Basic Trial", "Orientation Trial", "Spectacular Trial", "Ultimate Trial"]
            tn_stage_code_template = [f'{event_code}_0', f'{event_code}_tm0', f'{event_code}_ex0', f'{event_code}_fin0']
            tn_stage_count = len(list(set(big_data["zone"][f'{event_code}_zone1']["stages"])))
            for i in range(1, 1 + tn_stage_count):
                tn_wave_count = big_data["zone"][f'{event_code}_zone1']["stages"].count(f'TN-{i}')
                tn_reward = []
                for j in range(tn_wave_count):
                    tn_stage_code = f'{tn_stage_code_template[j]}{i}'
                    tn_article_data_dict = tn_article_data(big_data, tn_stage_code)
                    tn_reward.append(tn_article_data_dict["rewards"])
                    if j == 0 :
                        article_data += [f'TN-{i}', tn_article_writer(tn_article_data_dict, "info"), "<tabber> Basic Trial="]
                    else:
                        article_data += [f'|-|{tn_diff[j]}=']
                    
                    article_data += [tn_article_writer(tn_article_data_dict, "data")]
                
                article_data += ["</tabber>\n", tn_article_writer(tn_article_data(big_data, f'{tn_stage_code_template[1]}{i}'), "squad"), tn_article_writer(tn_reward, "rewards")]
            break
        
        elif mode_info == "vb":
            if stage.find("sp") != -1 :
                mode = "sp"
                #continue
            elif stage.find("_h") != -1 :
                mode = "hard"
                #continue
            else:
                mode = "core"
                #continue
            stage_info = vb_article_data(big_data, stage, mode)
            stage_article = [f'### {stage}', vb_article_writer(stage_info, mode), f'{{{{{page_footer}}}}}']
            article_data += stage_article

    # Enemies articles
    # - https://arknights.wiki.gg/wiki/Template:Enemy_infobox
    # - https://arknights.wiki.gg/wiki/Template:Appearances
    for enemy in big_data["enemies"]:
        #print(enemy)
        break
        enemy_article_writer(big_data["enemies"][enemy])
    #printc(sorted(data["enemies"].keys()))
    #script_result(big_data)
    #script_result(big_data["stage"])
    return article_data
    '''

event_id    = ""
# ['episode', 'intermezzo', 'sidestory', 'storycollection', 'ig', 'is', 'sss', 'tn', 'vb']
event_type  = "is"
event_name  = ""
year        = "5"

DB      = load_json(all_json = True)
ENEMY   = Enemy_Database().DB
STAGE   = Stage_Database().Lister(event_id, event_type, year)

script_result(STAGE, True)

#wiki_operation(event_id, event_type, event_name, year)