import json
import os
import re
import subprocess
from typing import Literal

import concurrent.futures
import requests
from pyFunction import B, R, RE, Y, json_load, printc, printr, script_result
from pyFunction_Wiki import load_json, wiki_story

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

# Manual
birthday_check      = json_load(r"C:\GitHub\AN-EN-Tags\temp\birthday_voicelines.json", temp=True)
#birthday_check      = json.loads(requests.get("https://raw.githubusercontent.com/PuppiizSunniiz/AN-EN-Tags/refs/heads/main/temp/birthday_voicelines.json").text)
combine_charword    = json_load(r"C:\GitHub\AN-EN-Tags\json/puppiiz/charword_table.json", temp=True)
#combine_charword    = json.loads(requests.get("https://raw.githubusercontent.com/PuppiizSunniiz/AN-EN-Tags/refs/heads/main/json/puppiiz/charword_table.json").text)

#DB["json_charwordEN"] = json_load(r"py\input_script.json", True)
#DB["json_charwordEN"] = json.loads(requests.get("https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/en/gamedata/excel/charword_table.json").text)

DEFAULT = {1: 'Appointed as Assistant', 2: 'Talk 1', 3: 'Talk 2', 4: 'Talk 3', 5: 'Talk after Promotion 1', 6: 'Talk after Promotion 2', 7: 'Talk after Trust Increase 1', 8: 'Talk after Trust Increase 2', 9: 'Talk after Trust Increase 3', 10: 'Idle', 11: 'Onboard', 12: 'Watching Battle Record', 13: 'Promotion 1', 14: 'Promotion 2', 17: 'Added to Squad', 18: 'Appointed as Squad Leader', 19: 'Depart', 20: 'Begin Operation', 21: 'Selecting Operator 1', 22: 'Selecting Operator 2', 23: 'Deployment 1', 24: 'Deployment 2', 25: 'In Battle 1', 26: 'In Battle 2', 27: 'In Battle 3', 28: 'In Battle 4', 29: '4-star Result', 30: '3-star Result', 31: 'Sub 3-star Result', 32: 'Operation Failure', 33: 'Assigned to Facility', 34: 'Tap', 36: 'Trust Tap', 37: 'Title', 38: "New Year's blessing", 42: 'Greeting', 43: 'Birthday', 44: 'Anniversary Celebration'}

DIALOGUE_CELL_SORT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 42, 37, 44, 38, 43]
DIALOGUE_CELL_SORT_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 42, 43, 44]

SERVER      = []
SERVER_DIR  = []

category = ""

def wiki_operator_dialogue(operator_list : list[str] | str, 
                           voice_data : list[str | bool], 
                           server : Literal["CN", "EN"] = "EN", 
                           force_server : bool = False,
                           dialogue_cell : Literal[1, "1", 2, "2"] = 1, 
                           audio : bool = False):
    
    if isinstance(operator_list, str):
        operator_real_id= operator_list.rsplit("_", 1)[0].split("#")[0] if operator_list.count("_") >= 3 else operator_list.split("#")[0]
        if force_server: server = "CN" if operator_real_id not in DB["json_characterEN"] else "EN"
        operator_name   = DB["json_characterEN"][operator_real_id]["name"] if operator_real_id in DB["json_characterEN"] else DB["json_character"][operator_real_id]["appellation"]
        operator_list   = [operator_list.replace("@", "_")]
    else:
        operator_name   = ""
        operator_list   = [operator.replace("@", "_") for operator in operator_list]
        
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
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = 6) as executor:
        futures  = []
        for operator_id in operator_list:
            dialogue_dict = {}
            
            crossover   = voice_data[0]
            jp          = voice_data[1] if manual else ("JP" in combine_charword["voiceLangDict"][operator_id])
            cn          = voice_data[2] if manual else ("CN_MANDARIN" in combine_charword["voiceLangDict"][operator_id])
            en          = voice_data[3] if manual else ("EN" in combine_charword["voiceLangDict"][operator_id])
            kr          = voice_data[4] if manual else ("KR" in combine_charword["voiceLangDict"][operator_id])
            otherlang_l = "" if manual else ([lang for lang in combine_charword["voiceLangDict"][operator_id] if lang not in ["CN_MANDARIN", "JP", "EN", "KR", "CN_TOPOLECT", "LINKAGE"]])
            otherlang   = lang_dict.get(otherlang_l[0], otherlang_l[0]) if otherlang_l else voice_data[5]
            dialect     = voice_data[6] if manual else (dialect_dict.get(operator_id, "Unknown") if "CN_TOPOLECT" in combine_charword["voiceLangDict"][operator_id] else "")
            outfit      = voice_data[7]
                
            for dialogue_key in charword_table_json["charWords"]:
                if re.match(rf'{operator_id}_CN_\d\d\d', dialogue_key):
                    voiceIndex  = charword_table_json["charWords"][dialogue_key]["voiceIndex"]
                    #voiceTitle  = charword_table_json["charWords"][dialogue_key]["voiceTitle"]
                    voiceText   = charword_table_json["charWords"][dialogue_key]["voiceText"]
                    dialogue_dict[voiceIndex] = wiki_story(voiceText) if server == "EN" else voiceText
            if dialogue_dict:
                if manual:
                    article_writer.append(f'\n{operator_id}\n{{{{Operator tab}}}}\n{{{{Operator dialogue head}}}}')
                else:
                    article_writer.append(f'{{{{Operator tab}}}}{f'\n{{{{Translation|article}}}}' if server == "CN" else ""}\n{{{{Operator dialogue head}}}}')
                for i in range(len(sort_list)):
                    if sort_list[i] in dialogue_dict:
                        cell_template       = "Operator dialogue cell2" if mode == 2 else "Operator dialogue cell"
                        dialogue_no         = i + 1 if mode == 1 else sort_list[i]
                        dialogue_desc       = f'|dialogue={dialogue_dict[sort_list[i]].replace("*", "&ast;")}' if dialogue_dict[sort_list[i]].startswith("**") else (f'|dialogue={dialogue_dict[sort_list[i]]}' if sort_list[i] != 37 else (f'|dialogue=\'\'[[Arknights]].\'\'' if mode == 2 else ""))
                        dialogue_outfit     = f'|outfit={outfit}' if outfit else ""
                        dialogue_jp         = "|jp=true" if jp else ""
                        dialogue_cn         = "|cn=true" if cn else ""
                        dialogue_en         = "|en=true" if (en and (sort_list[i] != 43) or (sort_list[i] == 43 and operator_id in birthday_check["EN"])) else ""
                        dialogue_kr         = "|kr=true" if (kr and (sort_list[i] != 43) or (sort_list[i] == 43 and operator_id in birthday_check["KR"])) else ""
                        dialogue_other      = f'|otherlang={otherlang}' if otherlang else ""
                        dialogue_dialect    = f'|dialect={dialect}' if dialect and cn else ""
                        if crossover:
                            article_writer.append(f'{{{{{cell_template}|no={dialogue_no}{dialogue_desc}|crossover=true}}}}')
                        else:
                            article_writer.append(f'{{{{{cell_template}|no={dialogue_no}{dialogue_desc}{dialogue_outfit}{dialogue_jp}{dialogue_cn}{dialogue_dialect}{dialogue_en}{dialogue_kr}{dialogue_other}}}}}')
                        if audio:
                            if crossover:
                                schedule_wiki_audio(executor, futures, no_in = sort_list[i], no_out = dialogue_no, dir_in = "", op_id = operator_id)
                            else:
                                if jp:
                                    schedule_wiki_audio(executor, futures, no_in = sort_list[i], no_out = dialogue_no, dir_in = "", name_out = "", op_id = operator_id)
                                if cn:
                                    schedule_wiki_audio(executor, futures, no_in = sort_list[i], no_out = dialogue_no, dir_in = "_cn", name_out = "-CN", op_id = operator_id)
                                if cn and dialect:
                                    schedule_wiki_audio(executor, futures, no_in = sort_list[i], no_out = dialogue_no, dir_in = "_custom", name_out = f'-CN-{dialect.capitalize()}', op_id = operator_id + "_cn_topolect")
                                if en:
                                    schedule_wiki_audio(executor, futures, no_in = sort_list[i], no_out = dialogue_no, dir_in = "_en", name_out = "-EN", op_id = operator_id)
                                if kr:
                                    schedule_wiki_audio(executor, futures, no_in = sort_list[i], no_out = dialogue_no, dir_in = "_kr", name_out = "-KR", op_id = operator_id)
                                if otherlang:
                                    if otherlang == "IT":
                                        schedule_wiki_audio(executor, futures, no_in = sort_list[i], no_out = dialogue_no, dir_in = "_custom", name_out = "-IT", op_id = operator_id + "_ita")
                                    else:
                                        schedule_wiki_audio(executor, futures, no_in = sort_list[i], no_out = dialogue_no, dir_in = "_custom", name_out = f'-{otherlang.upper()}', op_id = operator_id)

    if article_writer:
        article_writer.append(f'{{{{Table end}}}}{f'\n\n[[Category:Operator audio]]\n[[Category:{operator_name}]]' if audio_category and operator_name else ""}')
        script_result(article_writer, True)

def schedule_wiki_audio(executor, tasks, **kwargs):
    future = executor.submit(wiki_audio, **kwargs)
    tasks.append(future)

def wiki_audio(no_in : int, no_out : int, op_id : str, dir_in : str = "", name_out : str = "", ):
    op_real_id      = op_id.rsplit("_", op_id.count("_") - 2)[0].split("#")[0] if op_id.count("_") >= 3 else op_id.split("#")[0]
    op_real_name    = DB["json_characterEN"][op_real_id]["name"] if op_real_id in DB["json_characterEN"] else DB["json_character"][op_real_id]["appellation"]
    op_name         = f'{op_real_name}-{outfit}' if outfit else op_real_name
    input_file      = rf'E:\dyn\audio\sound_beta_2\voice{dir_in}\{op_id}\CN_{str(no_in).zfill(3)}.wav'
    output_file     = rf'E:\Wiki Audio\{op_real_id}\{op_name}-{str(no_out).zfill(3)}{name_out}.ogg'
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    #printc(op_id)
    #printc("input_file", input_file)
    #printc("output_file", output_file)
    
    cmd = [
                "ffmpeg", "-y",           # overwrite output if exists
                "-i", input_file,         # input file
                "-c:a", "libvorbis",      # use Vorbis codec (for .ogg)
                "-qscale:a", "5",         # quality 0–10 (6 = great for wiki)
                "-metadata", f'comment={name_out.replace("-", "", 1) if name_out else "JP"}',
                output_file
            ]
    subprocess.run(cmd, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)


dialect_dict = {
                "char_2014_nian"    : "Sichuanese",
                "char_2015_dusk"    : "Suzhounese",
                "char_2023_ling"    : "Guanzhonghua",
                "char_010_chen"     : "Cantonese",
                "char_1013_chen2"   : "Cantonese",
                "char_136_hsguma"   : "Cantonese",
                "char_455_nothin"   : "Nankinese",
                "char_241_panda"    : "Cheng-Yu",
                "char_308_swire"    : "Cantonese",
                "char_2024_chyue"   : "Wuhanese",
                "char_4080_lin"     : "Cantonese",
                "char_473_mberry"   : "Jinanhua",
                "char_383_snsant"   : "Hangzhouhua",
                "char_322_lmlee"    : "Cantonese",
                "char_226_hmau"     : "Cantonese",
                "char_225_haak"     : "Cantonese",
                "char_243_waaifu"   : "Cantonese",
                "char_1033_swire2"  : "Cantonese",
                "char_4121_zuole"   : "Henanese",
                "char_2025_shu"     : "Hokkien",
                "char_2026_yu"      : "Jinanhua",
                "char_1044_hsgma2"  : "Cantonese"
            }
lang_dict = {
                "ITA"   : "IT",
                "GER"   : "DE",
                "RUS"   : "RU",
                "FRE"   : "FR",
                "SPA"   : "ES",
}
'''
    char_2014_nian      Nian				        Sichuanese
    char_2015_dusk      Dusk				        Suzhounese
    char_2023_ling      Ling				        Guanzhonghua
    char_010_chen       Ch'en				        Cantonese
    char_1013_chen2     Ch'en the Holungday			Cantonese
    char_136_hsguma     Hoshiguma				    Cantonese
    char_455_nothin     Mr. Nothing				    Nankinese
    char_241_panda      FEater				        Cheng-Yu
    char_308_swire      Swire				        Cantonese
    char_2024_chyue     Chongyue				    Wuhanese
    char_4080_lin       Lin					        Cantonese
    char_473_mberry     Mulberry				    Jinanhua
    char_383_snsant     Snowsant				    Hangzhouhua
    char_322_lmlee      Lee					        Cantonese
    char_226_hmau       Hung				        Cantonese
    char_225_haak       Aak					        Cantonese
    char_243_waaifu     Waai Fu				        Cantonese
    char_1033_swire2    Swire the Elegant Wit		Cantonese
    char_4121_zuole     Zuo Le				        Henanese
    char_2025_shu       Shu					        Hokkien
    char_2026_yu        Yu					        Jinanhua
    char_1044_hsgma2    Hoshiguma the Breacher		Cantonese
'''
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
        char_1038_whitw2_sale#15            #dumbdumb
        "char_4134_cetsyr_epoque#50"        #Theresa
    ],
'''

crossover       = False  # True False
jp              = True  # True False
cn              = True  # True False
en              = True  # True False
kr              = True  # True False
otherlang       = ""    # DE FR IT RU etc.
dialect         = ""    # TBU
outfit          = ""
op_voice_data   = [crossover, jp, cn, en, kr, otherlang, dialect, outfit]

OP_DIALOGUE_LIST    = "char_388_mint"
dialogue_cell       = 1     # 1 2
server              = "EN"  # EN CN
force_server        = True
audio               = True  # True False
manual              = False  # True False
audio_category      = True

wiki_operator_dialogue(operator_list = OP_DIALOGUE_LIST, server = server, force_server = force_server, dialogue_cell = dialogue_cell, audio = audio, voice_data = op_voice_data)

#https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/en/gamedata/excel/charword_table.json
#https://arknights.wiki.gg/wiki/Caper/Dialogue#cite_ref-1
#   (^\{\{Operator dialogue cell\|.+?(?<!=true))\}\}$
#   $1|jp=true|cn=true|en=true|kr=true}}
#
#   {{Operator dialogue head|note='''CHY''' denotes the <u>Ch</u>eng-<u>Y</u>u Chinese dialect voiceline.}}
'''
    "char_204_platnm": {            Platinum    5
        "JP": "Ai Kayano"
    },
    "char_230_savage": {            Savage      5
        "JP": "Fujimura Ayumi"
    },
    "char_136_hsguma": {            Hoshi       6
        "CN_MANDARIN": "X. Chai"
    },
    "char_473_mberry": {            Mul         5
        "CN_MANDARIN": "X. Chai"
    },
    "char_144_red": {               Red         5
        "CN_MANDARIN": "X. Chai"
    },
    "char_103_angel": {             Exu         6
        "EN": "Leonora Haig"
    }
'''