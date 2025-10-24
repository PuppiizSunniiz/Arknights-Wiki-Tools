import json
import re
from typing import Literal

import requests
from pyFunction import B, R, RE, Y, json_load, printr, script_result
from pyFunction_Wiki import load_json, wiki_story

used_json = [
                "json_charword",
                "json_charwordEN",
            ]
DB = load_json(used_json)

DB["json_charwordEN"] = json_load(r"py\input_script.json", True)
#DB["json_charwordEN"] = json.loads(requests.get("https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/en/gamedata/excel/charword_table.json").text)

DEFAULT = {1: 'Appointed as Assistant', 2: 'Talk 1', 3: 'Talk 2', 4: 'Talk 3', 5: 'Talk after Promotion 1', 6: 'Talk after Promotion 2', 7: 'Talk after Trust Increase 1', 8: 'Talk after Trust Increase 2', 9: 'Talk after Trust Increase 3', 10: 'Idle', 11: 'Onboard', 12: 'Watching Battle Record', 13: 'Promotion 1', 14: 'Promotion 2', 17: 'Added to Squad', 18: 'Appointed as Squad Leader', 19: 'Depart', 20: 'Begin Operation', 21: 'Selecting Operator 1', 22: 'Selecting Operator 2', 23: 'Deployment 1', 24: 'Deployment 2', 25: 'In Battle 1', 26: 'In Battle 2', 27: 'In Battle 3', 28: 'In Battle 4', 29: '4-star Result', 30: '3-star Result', 31: 'Sub 3-star Result', 32: 'Operation Failure', 33: 'Assigned to Facility', 34: 'Tap', 36: 'Trust Tap', 37: 'Title', 38: "New Year's blessing", 42: 'Greeting', 43: 'Birthday', 44: 'Anniversary Celebration'}

DIALOGUE_CELL_SORT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 42, 37, 44, 38, 43]
DIALOGUE_CELL_SORT_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 42, 43, 44]

def wiki_operator_dialogue(operator_list : list[str] | str, server : Literal["CN", "EN"] = "EN", dialogue_cell : Literal[1, "1", 2, "2"] = 1):
    if isinstance(operator_list, str):
        operator_list = [operator_list.replace("@", "_")]
    else:
        operator_list = [operator.replace("@", "_") for operator in operator_list]
        
    article_writer = []
    charword_table_json = DB["json_charwordEN"] if server == "EN" else DB["json_charword"]
    if dialogue_cell in [1, "1"]:
        sort_list = DIALOGUE_CELL_SORT
        mode = 1
    elif dialogue_cell in [2, "2"]:
        sort_list = DIALOGUE_CELL_SORT_2
        mode = 2
    else:
        printr(f'{Y}How did you come here . . . {R}B A K A ! ! !{RE} ({B}dialogue_cell{RE} = {R}{dialogue_cell}{RE})')
        exit()
        
    for operator_id in operator_list:
        dialogue_dict = {}
        
        for dialogue_key in charword_table_json["charWords"]:
            if re.match(rf'{operator_id}_CN_\d\d\d', dialogue_key):
                voiceIndex  = charword_table_json["charWords"][dialogue_key]["voiceIndex"]
                #voiceTitle  = charword_table_json["charWords"][dialogue_key]["voiceTitle"]
                voiceText   = charword_table_json["charWords"][dialogue_key]["voiceText"]
                dialogue_dict[voiceIndex] = wiki_story(voiceText)
        if dialogue_dict:
            #article_writer.append(f'\n{operator_id}\n{{{{Operator tab}}}}\n{{{{Operator dialogue head}}}}')
            article_writer.append(f'{{{{Operator tab}}}}\n{{{{Operator dialogue head}}}}')
            for i in range(len(sort_list)):
                if sort_list[i] in dialogue_dict:
                    cell_template       = "Operator dialogue cell2" if mode == 2 else "Operator dialogue cell"
                    dialogue_no         = i + 1 if mode == 1 else sort_list[i]
                    dialogue_desc       = dialogue_dict[sort_list[i]].replace("*", "&ast;") if dialogue_dict[sort_list[i]].startswith("*") else (dialogue_dict[sort_list[i]] if sort_list[i] != 37 else (f'|dialogue=\'\'[[Arknights]].\'\'' if mode == 2 else ""))
                    dialogue_outfit     = f'|outfit={outfit}' if outfit else ""
                    dialogue_jp         = "|jp=true" if jp else ""
                    dialogue_cn         = "|cn=true" if cn else ""
                    dialogue_en         = "|en=true" if en and sort_list[i] != 43 else ""
                    dialogue_kr         = "|kr=true" if kr and sort_list[i] != 43 else ""
                    dialogue_other      = f'|otherlang={otherlang}' if otherlang else ""
                    dialogue_dialect    = f'|dialect={dialect}' if dialect else ""
                    article_writer.append(f'{{{{{cell_template}|no={dialogue_no}{f'|dialogue={dialogue_desc}'}{dialogue_outfit}{dialogue_jp}{dialogue_cn}{dialogue_dialect}{dialogue_en}{dialogue_kr}{dialogue_other}}}}}')
                
    if article_writer:
        article_writer.append("{{Table end}}")
        script_result(article_writer, True)

'''
    "skinWords": [
        "char_003_kalts_boc#6",             #kal
        "char_1012_skadi2_iteration#2",     #skya
        "char_1016_agoat2_epoque#34",       #eyja
        "char_1032_excu2_sale#12",          #excu
        "char_1035_wisdel_sale#14",         #wis
        "char_113_cqbw_epoque#7",           #w
        "char_2024_chyue_cfa#1",            #K
        "char_245_cello_sale#12",           #tutu
        "char_249_mlyss_boc#8",             #mumu
        "char_4064_mlynar_epoque#28",       #uncle
        "char_472_pasngr_epoque#17"         #pass
    ],
'''

jp = True   # True False
cn = True   # True False
en = True   # True False
kr = True   # True False
otherlang = ""  #IT RU etc.
dialect = "Cantonese"
outfit = ""

OP_DIALOGUE_LIST    = "char_136_hsguma"
dialogue_cell       = 1

wiki_operator_dialogue(operator_list = OP_DIALOGUE_LIST, dialogue_cell = dialogue_cell)

#https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/en/gamedata/excel/charword_table.json
#https://arknights.wiki.gg/wiki/Caper/Dialogue#cite_ref-1
#   (^\{\{Operator dialogue cell\|.+?)\}\}$
#   $1|jp=true|cn=true|en=true|kr=true}}