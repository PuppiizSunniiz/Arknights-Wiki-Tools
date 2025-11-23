from pyFunction_Wiki import load_json

used_json = [
                "json_uniequip",
                "json_uniequipEN"
            ]

DB = load_json(used_json)

DB_CN = DB["json_uniequip"]["subProfDict"]
DB_EN = DB["json_uniequipEN"]["subProfDict"]

######## CONST ########
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

subclass_temp = {
                    'counsellor': 'Strategist',
                    'mercenary': 'Mercenary'
                }

SUBCLASS_PARSE : dict[str, str] = {subclass:DB_EN[subclass]["subProfessionName"] if subclass in DB_EN else subclass_temp.get(subclass, f'{subclass.capitalize()}[PH]') for subclass in DB_CN}

######## TL ########

ENEMY_NAMES_TL = {

                }
ITEM_NAMES_TL = {
                    "act46side_token_detector"  : "Multipurpose Snow Detector",
                }
PART_NAMES_TL = {
                    "圣巡之旅"  : "Holy Tour",
                    "变革之路"  : "Path of Change",
                    "喀兰之心"  : "Heart of Karlan",
                }
TOKEN_NAMES_TL = {}
SKILL_NAMES_TL = {}