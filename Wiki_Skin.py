from typing import Literal
from pyFunction import R, Y, join_and, json_load, printr, script_result
from pyFunction_Wiki import load_json, wiki_story

used_json = [
                "json_skin",
                "json_skinEN",
            ]
DB = load_json(used_json)

def wiki_skin(skin_list : list[str], lang = Literal["CN", "EN"], temp = False):
    if temp:
        skin_DB = json_load("py/temp_skin.json", True)["charSkins"]
    elif lang == "EN" :
        skin_DB = DB["json_skinEN"]["charSkins"]
    else:
        skin_DB = DB["json_skin"]["charSkins"]
    
    skin_article = []
    
    for skin in skin_list:
        skin_check = False
        for skin_id in skin_DB.keys():
            if skin_id.find("@") == -1:
                continue
            if skin_DB[skin_id]["displaySkin"]["skinName"] == skin:
                illustrator : str   = join_and(skin_DB[skin_id]["displaySkin"]["drawerList"])
                usage       : str   = skin_DB[skin_id]["displaySkin"]["usage"]
                quote       : str   = wiki_story(skin_DB[skin_id]["displaySkin"]["description"])
                series      : str   = wiki_story(skin_DB[skin_id]["displaySkin"]["dialog"][:skin_DB[skin_id]["displaySkin"]["dialog"].find(skin) + len(skin) + 1].strip())
                desc        : str   = wiki_story(skin_DB[skin_id]["displaySkin"]["dialog"][skin_DB[skin_id]["displaySkin"]["dialog"].find(skin) + len(skin) + 1:].strip())
                
                skin_desc = f'''|name = {skin}
                                |illustrator = {illustrator}
                                |use = {usage}
                                |quote = {quote}
                                |series = {series}
                                |desc = {desc}\n
                                '''.replace("                                ", "")
                module_desc = f'use="{usage.replace('"', '\\"')}", quote="{quote.replace('"', '\\"')}", series="{series.replace('"', '\\"')}", desc="{desc.replace('"', '\\"')}"\n'
                skin_article.append(skin_desc + module_desc)
                skin_check = True
                break
        if not skin_check:
            printr(f'Skin {Y}{skin} {R}not found')
    
    script_result(skin_article, True)

skin_list : list[str] = ["Candy Strike"]
wiki_skin(skin_list, temp = True)