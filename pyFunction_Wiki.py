import re
from types import NoneType

from pyFunction import R, RE, Y, decimal_format, json_load, printr

CLASS_PARSE_EN : dict[str, str] = {
                                    "MEDIC"   : "Medic",          "WARRIOR"   : "Guard",
                                    "SPECIAL" : "Specialist",     "SNIPER"    : "Sniper",
                                    "PIONEER" : "Vanguard",       "CASTER"    : "Caster",
                                    "SUPPORT" : "Supporter",      "TANK"      : "Defender"
                                }


CLASS_PARSE_CN : dict[str, str] = {
                                    'SNIPER' :"狙击", 'PIONEER':"先锋", 'TANK'   :"重装",  'MEDIC'   :"医疗",
                                    'SUPPORT':"辅助", 'SPECIAL':"特种", 'WARRIOR':"近卫",  'CASTER'  :"术师"
                                }

def load_json(json_load_list : str | list = []) -> dict :
    '''
        json_activity, json_audio, json_battle_equip, json_building, json_campaign, json_chapter, json_character, json_charm, json_charword, json_char_meta, json_char_patch, json_checkin, json_climb_tower, json_clue, json_crisis, json_crisis_v2, json_display_meta, json_enemy_handbook, json_favor, json_gacha, json_gamedata, json_handbook_info, json_handbook, json_handbook_team, json_item, json_medal, json_mission, json_open_server, json_player_avatar, json_range, json_replicate, json_retro, json_roguelike, json_roguelike_topic, json_sandbox_perm, json_sandbox, json_shop_client, json_skill, json_skin, json_stage, json_story_review_meta, json_story_review, json_story, json_tech_buff, json_tip, json_token, json_uniequip, json_zone, json_enemy_database,
        
        json_activityEN, json_audioEN, json_battle_equipEN, json_buildingEN, json_campaignEN, json_chapterEN, json_characterEN, json_charmEN, json_charwordEN, json_char_metaEN, json_char_patchEN, json_checkinEN, json_climb_towerEN, json_clueEN, json_crisisEN, json_crisis_v2EN, json_display_metaEN, json_enemy_handbookEN, json_favorEN, json_gachaEN, json_gamedataEN, json_handbook_infoEN, json_handbookEN, json_handbook_teamEN, json_itemEN, json_medalEN, json_missionEN, json_open_serverEN, json_player_avatarEN, json_rangeEN, json_replicateEN, json_retroEN, json_roguelikeEN, json_roguelike_topicEN, json_sandbox_permEN, json_sandboxEN, json_shop_clientEN, json_skillEN, json_skinEN, json_stageEN, json_story_review_metaEN, json_story_reviewEN, json_storyEN, json_tech_buffEN, json_tipEN, json_tokenEN, json_uniequipEN, json_zoneEN, json_enemy_databaseEN, 
        
        json_named_effect, json_dict
    '''
    if isinstance(json_load_list, str):
        json_load_list = [json_load_list]
    
    json_list = {
                    "json_activity" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/activity_table.json",
                    "json_audio" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/audio_data.json",
                    "json_battle_equip" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/battle_equip_table.json",
                    "json_building" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/building_data.json",
                    "json_campaign" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/campaign_table.json",
                    "json_chapter" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/chapter_table.json",
                    "json_character" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/character_table.json",
                    "json_charm" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/charm_table.json",
                    "json_charword" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/charword_table.json",
                    "json_char_meta" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/char_meta_table.json",
                    "json_char_patch" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/char_patch_table.json",
                    "json_checkin" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/checkin_table.json",
                    "json_climb_tower" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/climb_tower_table.json",
                    "json_clue" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/clue_data.json",
                    "json_crisis" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/crisis_table.json",
                    "json_crisis_v2" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/crisis_v2_table.json",
                    "json_display_meta" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/display_meta_table.json",
                    "json_enemy_handbook" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/enemy_handbook_table.json",
                    "json_favor" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/favor_table.json",
                    "json_gacha" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/gacha_table.json",
                    "json_gamedata" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/gamedata_const.json",
                    "json_handbook_info" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/handbook_info_table.json",
                    "json_handbook" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/handbook_table.json",
                    "json_handbook_team" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/handbook_team_table.json",
                    "json_item" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/item_table.json",
                    "json_medal" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/medal_table.json",
                    "json_mission" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/mission_table.json",
                    "json_open_server" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/open_server_table.json",
                    "json_player_avatar" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/player_avatar_table.json",
                    "json_range" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/range_table.json",
                    "json_replicate" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/replicate_table.json",
                    "json_retro" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/retro_table.json",
                    "json_roguelike" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/roguelike_table.json",
                    "json_roguelike_topic" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/roguelike_topic_table.json",
                    "json_sandbox_perm" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/sandbox_perm_table.json",
                    "json_sandbox" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/sandbox_table.json",
                    "json_shop_client" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/shop_client_table.json",
                    "json_skill" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/skill_table.json",
                    "json_skin" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/skin_table.json",
                    "json_stage" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/stage_table.json",
                    "json_story_review_meta" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/story_review_meta_table.json",
                    "json_story_review" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/story_review_table.json",
                    "json_story" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/story_table.json",
                    "json_tech_buff" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/tech_buff_table.json",
                    "json_tip" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/tip_table.json",
                    "json_token" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/token_table.json",
                    "json_uniequip" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/uniequip_table.json",
                    "json_zone" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/excel/zone_table.json",
                    "json_enemy_database" : "json/gamedata/ArknightsGameData/zh_CN/gamedata/levels/enemydata/enemy_database.json",
                    
                    "json_activityEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/activity_table.json",
                    "json_audioEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/audio_data.json",
                    "json_battle_equipEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/battle_equip_table.json",
                    "json_buildingEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/building_data.json",
                    "json_campaignEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/campaign_table.json",
                    "json_chapterEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/chapter_table.json",
                    "json_characterEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/character_table.json",
                    "json_charmEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/charm_table.json",
                    "json_charwordEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/charword_table.json",
                    "json_char_metaEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/char_meta_table.json",
                    "json_char_patchEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/char_patch_table.json",
                    "json_checkinEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/checkin_table.json",
                    "json_climb_towerEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/climb_tower_table.json",
                    "json_clueEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/clue_data.json",
                    "json_crisisEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/crisis_table.json",
                    "json_crisis_v2EN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/crisis_v2_table.json",
                    "json_display_metaEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/display_meta_table.json",
                    "json_enemy_handbookEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/enemy_handbook_table.json",
                    "json_favorEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/favor_table.json",
                    "json_gachaEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/gacha_table.json",
                    "json_gamedataEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/gamedata_const.json",
                    "json_handbook_infoEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/handbook_info_table.json",
                    "json_handbookEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/handbook_table.json",
                    "json_handbook_teamEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/handbook_team_table.json",
                    "json_itemEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/item_table.json",
                    "json_medalEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/medal_table.json",
                    "json_missionEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/mission_table.json",
                    "json_open_serverEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/open_server_table.json",
                    "json_player_avatarEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/player_avatar_table.json",
                    "json_rangeEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/range_table.json",
                    "json_replicateEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/replicate_table.json",
                    "json_retroEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/retro_table.json",
                    "json_roguelikeEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/roguelike_table.json",
                    "json_roguelike_topicEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/roguelike_topic_table.json",
                    "json_sandbox_permEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/sandbox_perm_table.json",
                    "json_sandboxEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/sandbox_table.json",
                    "json_shop_clientEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/shop_client_table.json",
                    "json_skillEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/skill_table.json",
                    "json_skinEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/skin_table.json",
                    "json_stageEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/stage_table.json",
                    "json_story_review_metaEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/story_review_meta_table.json",
                    "json_story_reviewEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/story_review_table.json",
                    "json_storyEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/story_table.json",
                    "json_tech_buffEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/tech_buff_table.json",
                    "json_tipEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/tip_table.json",
                    "json_tokenEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/token_table.json",
                    "json_uniequipEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/uniequip_table.json",
                    "json_zoneEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/excel/zone_table.json",
                    "json_enemy_databaseEN" : "json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/levels/enemydata/enemy_database.json",
                    
                    "json_named_effect" : "json/named_effects.json",
                    "json_dict" : "py/dict.json"
                }
    return {new_json:json_load(json_list[new_json]) for new_json in json_load_list}

def wiki_trim(text : str, replace_all : bool = True) -> str:
    if replace_all:
        return replace_apos_between(text).replace("'", "").replace('"', "").replace("?", "")
    else:
        return replace_apos_between(text).replace('"', "").replace("?", "")

def wiki_text(candidate : tuple[str, list] | str) -> str:
    '''
    candidate type:
        - for blackboard text -> tuple[str, list]
            ex. <@ba.kw>{atk:0%}</>
        - for non blackboard text -> str
            ex. talent <@ba.vup>+5%</>
    '''
    
    def kw_matching(desc : str, isBB : bool = False, blackboard : list = []) -> str:
        kw_match = re.search(r'<@(?:ba|cc)\.([\.\w\d]+)>((?:<(?!(?:@|\$)(?:cc|ba)\.\1).*?<\/>)*.*?)<\/>', desc)
        if kw_match:
            match_desc = blackboarding(blackboard, kw_match.group(2)) if isBB else kw_match.group(2)
            sub_desc = re.sub(r'<@(?:ba|cc)\.([\.\w\d]+)>((?:<(?!(?:@|\$)(?:cc|ba)\.\1).*?<\/>)*.*?)<\/>', rf'{{{{Color|{match_desc}|{kw_match.group(1).replace("v","")}}}}}', desc, 1)
            return kw_matching(sub_desc, isBB, blackboard)
        else:
            return desc
    
    def ba_matching(desc : str) -> str:
        ba_match = re.search(r'<\$(ba\.[^>]*)>([^<]*)<\/>', desc)
        if ba_match:
            term_name = DB["json_gamedataEN"]["termDescriptionDict"].get(ba_match.group(1), DB["json_gamedata"]["termDescriptionDict"][ba_match.group(1)])["termName"]
            wording = ba_match.group(2).replace("[", "").replace("]", "")
            if term_name == wording:
                sub_desc = re.sub(r'<\$(ba\.[^>]*)>([^<]*)<\/>', rf'{{{{G|{wording}}}}}', desc, 1)
                return ba_matching(sub_desc)
            else:
                sub_desc = re.sub(r'<\$(ba\.[^>]*)>([^<]*)<\/>', rf'{{{{G|{term_name}|{wording}}}}}', desc, 1)
                return ba_matching(sub_desc)
        return desc
    
    def cc_matching(desc : str) -> str:
        cc_match = re.search(r'<\$(cc\.[^>]*)>([^<]*)<\/>', desc)
        if cc_match:
            term_name = DB["json_gamedataEN"]["termDescriptionDict"].get(cc_match.group(1), DB["json_gamedata"]["termDescriptionDict"][cc_match.group(1)])["termName"]
            sub_desc = re.sub(r'<\$(cc\.[^>]*)>([^<]*)<\/>', rf'{{{{G|{term_name}|{cc_match.group(2)}}}}}', desc, 1)
            return cc_matching(sub_desc)
        else:
            return desc
    
    isBB = isinstance(candidate, tuple)
    
    DB = load_json(["json_gamedata", "json_gamedataEN"])
    desc = candidate[0] if isBB else candidate
    blackboard = candidate[1] if isBB else []

    desc = kw_matching(desc, isBB, blackboard)
    desc = ba_matching(desc)
    desc = cc_matching(desc)

    return desc.strip()

def replace_apos_between(part : str) -> str:
    ############################################################################################################################################
    # Find with Regex ON (.*)
    #   too strict : ^(|.+?[\. (?:|<br\/>|<br>)])(?<!')'(?!em[ \.]|n[ \.]|tis|twas|twere|<br\/>|<br>)([^' ].+?[^']*)(?<!')'(?!')(?:( |\?|!|\.|,|<br\/>|<br>|\|)(.+?|)|)$
    #   too greedy : (^|[\s\.\|=;]|<br>|<br\/>)'(?!em[ \.]|n[ \.]|tis|twas|twere|<br\/>|<br>)([^' ].+?[^']*)'([!,&\.\s\?\]]|<br\/>|<br>|\||$)
    #   
    ############################################################################################################################################
    # Replace
    #   $1"$2"$3$4
    #   $1"$2"$3
    ############################################################################################################################################
    # Test Case
    #   # Apply
    #   Strange, why does Dr. Kal'tsit keeps telling me to 'be nice to patients'? She's been doing it ever since I got here.
    #   {{Operator dialogue cell|no=3|dialogue='April'? 'April' is a song about spring. The lyrics describe the feeling of lying on the grass on a warm spring day, looking up at the sky and letting your mind wander. Wanna hear it, Doctor? I'm sure you'll love it.}}
    #   
    #   # Ignore
    #   Your average doctor's biggest concern is keeping herself safe. Mine, on the other hand... it's getting my patients to stop being scared of me.
    #
    #   # Mix
    #   I was in the Convalescent Garden, and I saw the plant almanac Perfumer's compiling. Lots of gaps, no way to fill them in as of yet. See, a good plant hunter fills the blanks with their 'prey.' A great plant hunter not only does that, they also get the author to leave them plenty more new blanks.
    #
    ############################################################################################################################################
    #apos_match = r"^(|.+?[\. (?:|<br\/>|<br>)])(?<!')'(?!em[ \.]|n[ \.]|tis|twas|twere|<br\/>|<br>)([^' ].+?[^']*)(?<!')'(?!')(?:( |\?|!|\.|,|<br\/>|<br>|\|)(.+?|)|)$"
    apos_match = r"(^|[\s\.\|=;]|<br>|<br\/>)'(?!em[ \.]|n[ \.]|tis|twas|twere|<br\/>|<br>)([^' ].+?[^']*)'([!,&\.\s\?\]]|<br\/>|<br>|\||$)"
    between_match = re.search(apos_match, part) 
    if between_match:
        #new_part = re.sub(apos_match, r'\1"\2"\3\4', part)
        new_part = re.sub(apos_match, r'\1"\2"\3', part)
        return replace_apos_between(new_part)
    else:
        return part

def wiki_cleanup(txt :str, all_clean : bool) -> str:
    clean_sheet = {
                    r'( ?\\n ?| ?\n ?)' : "<br/>",
                    r'(’)'              : "'",
                    r'(。)'             : ".",
                    r'(…)'              : "...",
                    r'，'               : ", ",
                    r'(“|”)'            : "\"",
                    r'【'               : " [",
                    r'】'               : "] ",
                    r'（'               : " (",
                    r'）'               : ") ",
                    r'？'               : "? ",
                    r'！'               : "!",
                    r'(\t|\\t)'         : " ",
                    r'[  ]+'            : " ",
                    r' +, '             : ", "
                }
    
    more_sheet = {
                    r'––'               : "&mdash;",
                    r'·'                : "&bull;",
                    #r'-'                : "&dash;",
                    r'–'                : "&ndash;",
                    r'—'                : "&mdash;",
                }

    for pattern, repl in clean_sheet.items():
        txt = re.sub(pattern, repl, txt)
    
    if all_clean:
        for pattern, repl in more_sheet.items():
            txt = re.sub(pattern, repl, txt)
    
    return txt #.replace(" <br/>", "<br/>")

def wiki_story_color(desc : str) -> str:
    color_match = r'<color=#(.+?)>(.+?)<\/color>'
    if re.match(color_match, desc):
        desc = re.sub(color_match, r'{{Color|\2|code=\1}}', desc)
        return wiki_story_color(desc)
    else:
        return desc

def wiki_story(story : str|list[str], newline : str = "\n", join_str : str = "<br/>", clean_all : bool = True) -> str:
    if isinstance(story, list):
        story = newline.join(story)
    desc_list = story.split(newline)
    for i in range(len(desc_list)):
        desc = desc_list[i]
        # Clean-up
        desc = wiki_cleanup(desc, clean_all)
        # Between
        desc = replace_apos_between(desc)
        # Start - End
        desc = re.sub(r"^'(.+?)'$", r'"\1"', desc)
        # Start -
        desc = re.sub(r"^'(.+?)([^'])$", r'"\1\2', desc)
        # - End
        desc = re.sub(r"^([^'])(.+?)'$", r'\1\2"', desc)
        # Color
        desc = wiki_story_color(desc)
        # Font I B
        desc = re.sub(r"<i>(.+?)</i>", r"''\1''", desc)
        desc = re.sub(r"<b>(.+?)</b>", r"'''\1'''", desc)
        desc_list[i] = desc.strip()
    return join_str.join(desc_list).replace(" <br/>", "<br/>")

def wiki_stage(stage_desc : str, newline : str = "\n", join_str : str = "<br/>") -> str:
    stage_desc = wiki_story(stage_desc, "\n", "\n")
    # Stage Item
    stage_desc = re.sub(r"<@lv.item><(.+?)>( |)</>", r"'''<[[\1]]>'''\2", stage_desc)
    # Rem
    stage_desc = re.sub(r"<@lv.rem>(.+?)</>", r"{{Color|\1|rem}}", stage_desc)
    return join_str.join(stage_desc)
    

def blackboarding(blackboard : list, desc : str):
    blackboard_match = re.match(r'(\+|-|)\{([^\{\}:]*)(?::([^\{\}:]*)|)\}', desc)
    #printr(blackboard_match, desc)
    if not blackboard_match:
        return desc
    match_symbol = blackboard_match.group(1)
    match_bbkey = blackboard_match.group(2)
    match_format = blackboard_match.group(3)
    #if match_format == "0%": match_format = ".0%"
    #printr(f'"{match_symbol}" "{match_bbkey}" "{match_format}"')
    if blackboard_match:
        for bb in blackboard:
            if bb["key"] == match_bbkey:
                #printr(match_bbkey, bb["valueStr"], bb["value"], match_format)
                return re.sub(r'(\+|-|)\{([^\{\}:]*)(?::([^\{\}:]*)|)\}', f'{match_symbol}{bb["valueStr"] if bb["valueStr"] else (f'{bb["value"]:.{match_format}}' if match_format else f'{decimal_format(bb["value"])}')}', desc)

def spType(sp_type : str|int):
    match sp_type:
        case "INCREASE_WITH_TIME":
            return "auto"
        case "INCREASE_WHEN_ATTACK": 
            return "offensive"
        case "INCREASE_WHEN_TAKEN_DAMAGE": 
            return "defensive"
        case 8: 
            return "auto"
        case _:
            return sp_type

def range_template(range_id : str|NoneType) -> str:
    if isinstance(range_id, NoneType):
        return ""
    
    json_range = load_json("json_range")["json_range"]
    
    if range_id not in json_range.keys():
        printr(f'Range {Y}{range_id} {R}not{RE} found')
        return ""

    temp = [[grid["col"],grid["row"]] for grid in json_range[range_id]["grids"]]
    
    max_x = max([x[0] for x in temp])
    min_x = min([x[0] for x in temp] + [0])
    max_y = max([y[1] for y in temp])
    min_y = min([y[1] for y in temp] + [0])
    
    range_array=[["p" for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]

    for col, row in temp:
        if [col, row] == [0,0]:
            range_array[row + max_y][col + abs(min(0, min_x))]="s"
        else:
            range_array[row + max_y][col + abs(min(0, min_x))]="r"
    
    if len(range_array) == 1 :
        return f'{{{{ranges|{"|".join(range_array[0])}}}}}'
    else:
        return f'{{{{Range container|{"".join([f'{{{{ranges|{"|".join(range_array[row])}}}}}' for row in range(len(range_array))])}}}}}'