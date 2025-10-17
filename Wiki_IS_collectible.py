import json
import requests
from pyFunction import printc, printr, script_result
from pyFunction_Wiki import load_json, wiki_story, wiki_trim

def wiki_is_collectible(rogue_ver : str, min_cap = "", max_cap = ""):
    used_json = [
                    "json_roguelike_topic"
                ]

    #DB = load_json(used_json)
    DB = {"json_roguelike_topic": json.loads(requests.get("https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/refs/heads/master/en/gamedata/excel/roguelike_topic_table.json").text)}

    rogue_ver = "rogue_" + rogue_ver
    DB_rogue = DB["json_roguelike_topic"]["details"][rogue_ver]

    Collectibles_sort_map   = []
    Collectibles_article    = []
    Collectibles_module     = []
    Collectibles_page       = []

    for collectible in DB_rogue["archiveComp"]["relic"]["relic"]:
        orderId = DB_rogue["archiveComp"]["relic"]["relic"][collectible]["orderId"]
        
        if (min_cap and min_cap > orderId) or (max_cap and orderId > max_cap):
            continue
        
        sort_key            = str(DB_rogue["archiveComp"]["relic"]["relic"][collectible]["relicGroupId"]).zfill(6) + str(DB_rogue["archiveComp"]["relic"]["relic"][collectible]["relicSortId"]).zfill(6)
        collectible_name    = DB_rogue["items"][collectible]["name"]
        collectible_title   = wiki_trim(DB_rogue["items"][collectible]["name"], False)
        isTitle             = wiki_trim(DB_rogue["items"][collectible]["name"], False) != DB_rogue["items"][collectible]["name"]
        collectible_rarity  = DB_rogue["items"][collectible]["rarity"].replace("_", "").lower()
        collectible_effect  = wiki_story(DB_rogue["items"][collectible]["usage"])
        collectible_desc    = wiki_story(DB_rogue["items"][collectible]["description"])
        collectible_cond    = wiki_story(DB_rogue["items"][collectible].get("unlockCondDesc", ""))
        collectible_obtain  = wiki_story(DB_rogue["items"][collectible].get("obtainApproach", ""))
        
        article = f'''{{{{Collectible cell
                    |no = {orderId}
                    |name = {collectible_title}
                    |rarity = {collectible_rarity}
                    |purchase = no
                    |effect = {collectible_effect}}}}}'''.replace("                    ", "")
                    
        module = f'["{collectible_name}"]={{name="{collectible_name}", {f'title="{collectible_title}", ' if isTitle else ""}num="{orderId}", qlt="{collectible_rarity}", use="{collectible_effect}", desc="{collectible_desc}"{f', cond="{collectible_cond}"' if collectible_cond else ""}}}'

        page = f'''{{{{Collectible infobox
                |name = {collectible_title}
                |image = {collectible_title}.png
                |no = {orderId}
                |rarity = {collectible_rarity}
                |purchase = no
                |theme = Phantom & Crimson Solitaire}}}}
                The \'\'\'{collectible_name}\'\'\' is a [[Collectible]] in [[Phantom & Crimson Solitaire]].

                {{{{Item description|{collectible_effect}|{collectible_desc}}}}}
                
                ==Effect==
                <!--{collectible_effect}-->

                ==How to obtain==
                <!--{collectible_obtain}, {collectible_cond}-->

                {{IS2 collectibles}}
                '''.replace("                ", "")
                
        Collectibles_sort_map.append(sort_key)
        Collectibles_article.append(article)
        Collectibles_module.append(module)
        Collectibles_page.append(page)
    
    sort_map = sorted(Collectibles_sort_map)
    sort_key = list(map(lambda x : sort_map.index(x), Collectibles_sort_map))

    Collectibles_article    = sorted(Collectibles_article, key=lambda x : sort_key[Collectibles_article.index(x)])
    Collectibles_module     = sorted(Collectibles_module, key=lambda x : sort_key[Collectibles_module.index(x)])
    Collectibles_page       = sorted(Collectibles_page, key=lambda x : sort_key[Collectibles_page.index(x)])
    script_result(Collectibles_article + Collectibles_module + Collectibles_page, True)

# write for working on IS#2 (rogue_1) for now might work on other
wiki_is_collectible("1", min_cap = "177", max_cap = "192")