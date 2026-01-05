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

IG_MODE : dict[str, str] = {
                                "NORMAL"    : "Regular Events", 
                                "FOOTBALL"  : "Positional Football",
                                "DEFENCE"   : "Bastion Defense",
                            }

IG_DIFF : dict[str, str] = {
                                "TRAINING"      : "Training Grounds", 
                                "ORDINARY"      : "Beginner",
                                "DIFFICULTY"    : "Advanced",
                                "EXTREMELY"     : "Expert",
                            }

######## TL ########

ENEMY_NAMES_TL = {
                    "enemy_2101_dyspll" : "Talisman",
                    "enemy_2102_dytmbr" : "Shadow Scholar",
                    "enemy_2103_dykens" : "Bottle Swordsman",
                    "enemy_2104_dycast" : "Mirror Tianshi",
                    "enemy_2105_dyrnge" : "Pseudomut",
                    "enemy_2106_dyremy" : "Strange Gourd",
                    "enemy_2122_dybgzd" : "Liang",
                    "enemy_2107_dycant" : "Can Doe",
                    
                    "enemy_2108_dypryg" : "Dusk Beauty",
                    "enemy_2109_dypry2" : "Lady of the Twin Moons",
                    "enemy_2114_dylbgg" : "Jade Twin-Swords",
                    "enemy_2112_dyhlgy" : "Crimson Crescent Blade",
                    "enemy_2110_dyyrzf" : "Ash Spear",
                    "enemy_2115_dylbg2" : "Lord Zhaolie",
                    "enemy_2113_dyhlg2" : "Lord Wenheng",
                    "enemy_2111_dyyrz2" : "Lord Huan",
                    "enemy_2116_dyyysg" : "Revered Grandmaster",
                    "enemy_2117_dyyys2" : "Grand Duke",
                    "enemy_2118_dylbhm" : "Yi",
                    "enemy_2119_dyshhj" : "'Sui'",
                    "enemy_2119_dyshhj_2" : "'Body of Sui'",
                    "enemy_2120_dywqgs" : "'Wang'",
                    
                }
ITEM_NAMES_TL = {
                    "act46side_token_detector"  : "Multipurpose Snow Detector",
                    "act47side_token_bottle"    : "Sky Respiratory Tube"
                }
PART_NAMES_TL = {
                    #act46side
                    "圣巡之旅"  : "Holy Tour",
                    "变革之路"  : "Path of Change",
                    "喀兰之心"  : "Heart of Karlan",
                    
                    #act47side
                    "天空生活展会" : "Sky Living Expo",
                    "逃离哥伦比亚" : "Escape from Columbia",
                    
                    #act48side
                    "神殿仪式" : "Temple Ceremony",
                    "街头戏剧" : "Street Theater",
                }
TOKEN_NAMES_TL = {
                    "trap_223_dynbox"   : "Magic Gourd",
                    "trap_224_dyrbox"   : "Iron Gourd",
                    "trap_225_dysbox"   : "Strange Gourd",
                    "trap_222_rgdysm"   : "Statuegeist",
                    "trap_251_buftrp"   : "Artifact Center",
                    "trap_226_dychss"   : "Flaw",
                    "trap_238_dydfst"   : "Candle Stand",
                    "trap_239_dyffgd"   : "Face to Face",
                    "trap_240_dyffdd"   : "Face to Face",
                    "token_10053_radian_tower3" : "Center",
}
SKILL_NAMES_TL = {}