
import re
from typing import Literal
from Wiki_OOP.char_data import Character_Database
from Wiki_OOP.display_data import Display_Database
from Wiki_OOP.enemy_data import Enemy_Database
from Wiki_OOP.item_data import Item_Database
from Wiki_OOP.skin_data import Skin_Database
from pyFunction import B, G, RE, Y, DictToCSV, blackboard_format, printc, printr, script_result, sorted_dict_key
from pyFunction_Wiki import load_json, mini_blackboard, wiki_elite_lv_parse, wiki_reward_lister, wiki_story, wiki_text

DB = load_json(all_json = True)

class AC_DATA:
    def __init__(self, season = ""):
        self.data : dict            = DB["json_activity"]["activity"]["AUTOCHESS_SEASON"]
        self.autoChessData : dict   = DB["json_activity"]["autoChessData"]
        if "AUTOCHESS_SEASON" in DB["json_activityEN"]["activity"]:
            self.data.update(DB["json_activityEN"]["activity"]["AUTOCHESS_SEASON"])
            self.autoChessData.update(DB["json_activityEN"]["autoChessData"])
        self.season         = list(self.data.keys())
        if not season:
            printr(f'{Y}Season not provide{RE} (current season : {B}{self.season}{RE})')
            exit()
        else:
            self.seasonData             = self.data[season]
            self.baseRewardDataList     = AC_DATA_BASEREWARD(self.seasonData)
            self.bandData               = AC_DATA_BAND(self.seasonData, self.autoChessData)
            self.bondInfoDict           = AC_DATA_BOND(self.seasonData, self.autoChessData)
            self.garrisonDataDict       = AC_DATA_GARRISON(self.seasonData)
            self.milestoneList          = AC_DATA_MILESTONE(self.seasonData, season)
            self.FactorInfo             = AC_DATA_FACTOR(self.seasonData)
            self.shopCharChessInfo      = AC_DATA_CHESSINFO(self.seasonData)
            self.cultivateEffectList    = AC_DATA_CULTIVATE(self.seasonData, self.autoChessData)
            
            self.charChessDataDict      = AC_DATA_CHARCHESS(self.seasonData)
            self.trapChessDataDict      = AC_DATA_TRAP(self.seasonData)
            
            
            
            
            #self.modeDataDict           = AC_DATA_MODE()
            #self.shopLevelDataDict      = AC_DATA_SHOP()
            #self.stageDatasDict         = AC_DATA_STAGE()
            #self.battleDataDict         = AC_DATA_BATTLE()
            #self.bossInfoDict           = AC_DATA_BOSS()
            #self.specialEnemyInfoDict   = AC_DATA_SPECENEMY()
            #self.enemyInfoDict          = AC_DATA_ENEMIES()
class AC_DATA_BAND:
    def __init__(self, data_season, data_ac):
        self.data : dict = bandData(data_season, data_ac)
    
    def toCSV(self, separator : str = "|"):
        csv_header  = ["ID", "Name", "HP", "Effect", "Condition"]
        csv_key     = ["band_name", "band_hp", "band_effect", "band_cond"]
        DictToCSV(self.data, csv_header, csv_key, separator)
    
    def toWIKI(self):
        wiki_result = []
        for band in self.data:
            band_data : dict = self.data[band]
            band_name       = band_data.get("band_name")
            band_hp         = band_data.get("band_hp") 
            band_effect     = band_data.get("band_effect")
            band_cond       = band_data.get("band_cond")
            wiki_result.append(f'''{{{{SP Strategies cell
                                |name = {band_name}
                                |initiator = 
                                |hp = {band_hp}
                                |effect = {band_effect}
                                |cond = {band_cond}}}}}'''.replace("                                ", ""))
        script_result(wiki_result, True)

class AC_DATA_BASEREWARD():
    def __init__(self, data_season):
        self.data   = baseRewardData(data_season)
    
    def toCSV(self, separator : str = "|"):
        csv_header  = ["Round", "Item ID", "Item Name", "Count", "Daily Point"]
        csv_key     = ["item_id", "item_name", "item_count", "daily_point"]
        DictToCSV(self.data, csv_header, csv_key, separator)

class AC_DATA_BOND():
    def __init__(self, data_season, data_ac):
        self.data   = bondInfo(data_season, data_ac)
    
    def toCSV(self, separator : str = "|"):
        csv_header  = ["ID", "Name", "Active Type", "Active Count", "Power List", "Full Desc", "Stack Desc"]
        csv_key     = ["bond_name", "bond_activeType", "bond_activeCount", "bond_powerIdList", "bond_desc", "bond_stackdesc"]
        DictToCSV(self.data, csv_header, csv_key, separator)

class AC_DATA_GARRISON():
    def __init__(self, data_season):
        self.data   = sorted_dict_key(garrisonData(data_season))
    
    def toCSV(self, separator : str = "|"):
        csv_header  = ["ID", "Type", "Icon", "S.Icon", "TypeDesc", "effectType", "Desc"]
        csv_key     = ["garrison_type", "garrison_typeicon", "garrison_typesicon", "garrison_typedesc", "garrison_effecttype", "garrison_desc"]
        DictToCSV(self.data, csv_header, csv_key, separator)

class AC_DATA_MILESTONE():
    def __init__(self, data_season, season):
        if len(DB["json_activity"]["activityItems"][season]) != 1 :
            printr(f'Multiple milestone token detected : {Y}{DB["json_activity"]["activityItems"][season]}')
            exit()
        else :
            self.token      = DB["json_activity"]["activityItems"][season][0]
            self.tokenname  = ITEM_DATA.getname(self.token)
            self.data       = milestoneList(data_season, self.token, self.tokenname)
        
    def toCSV(self, separator : str = "|"):
        csv_header  = ["Level", "Milestone", "M.Icon", "M.Num", "Reward", "Name", "Icon ID", "Count", "Type"]
        csv_key     = ["milestone_tokenID", "milestone_tokenName", "milestone_tokenNum", "milestone_rewardID", "milestone_rewardName", "milestone_rewardiconId", "milestone_rewardCount", "milestone_rewardType"]
        DictToCSV(self.data, csv_header, csv_key, separator)

    def toWIKI(self):
        wiki_result = ['''{{Season tab|mode=sp}}
                            A list of milestone rewards the Stronghold Protocol event, raised through {{I|Stronghold Credits|g=0}} accumulation.

                            The Stronghold Credit rewards can be claimed until ''To be Added''.

                            {{Milestone head|ms=Stronghold Credits}}'''.replace("                            ", "")
                        ]
        for milestone in self.data:
            milestone_data : dict = self.data[milestone]
            milestone_tokenNum      = milestone_data.get("milestone_tokenNum")
            milestone_rewardName    = milestone_data.get("milestone_rewardName") 
            milestone_rewardCount   = milestone_data.get("milestone_rewardCount")
            milestone_rewardType    = milestone_data.get("milestone_rewardType")
            milestone_reward        = wiki_reward_lister(milestone_rewardName, milestone_rewardCount, milestone_rewardType)
            wiki_result.append(f'{{{{Milestone cell|level={milestone}|milestone=Stronghold Credits, {milestone_tokenNum}|{milestone_reward}}}}}')
        wiki_result.append('''{{Table end}}

                                [[Category:Stronghold Protocol milestones]]'''.replace("                                ", ""))
        script_result(wiki_result, True)

class AC_DATA_FACTOR():
    def __init__(self, data_season):
        self.data       = FactorInfo(data_season)
    
    def toCSV(self, separator : str = "|"):
        csv_header  = ["Mode", "Factor"]
        DictToCSV(self.data, csv_header, separator = separator, use_key = True)

class AC_DATA_CHESSINFO():
    def __init__(self, data_season):
        self.data       = ChessInfo(data_season)
        self.basedata   = self.data["base"]
        self.golddata   = self.data["gold"]
    
    def toCSV(self, mode : Literal["base", "gold"] = "base", separator : str = "|"):
        csv_header  = ["Level", "evolvePhase", "charLevel", "skillLevel", "favorPoint", "equipLevel", "purchasePrice", "chessSoldPrice", "eliteIconId"]
        csv_keys    = ["evolvePhase", "charLevel", "skillLevel", "favorPoint", "equipLevel", "purchasePrice", "chessSoldPrice", "eliteIconId"]
        DictToCSV(self.data[mode], csv_header, csv_keys, separator)
    
    def toWIKI(self):
        def level_lister(data):
            level_list = []
            for level in data:
                level_data  = data[level]
                level_elite = level_data["evolvePhase"]
                level_level = level_data["charLevel"]
                level_skill = level_data["skillLevel"]
                level_mod   = level_data["equipLevel"]
                level_list.append(f'''|t{level} lv = {wiki_elite_lv_parse(level_elite, level_level)}
                                        |t{level} sklv = {level_skill}{f'\n|t{level} modst = {level_mod}' if level_mod else ""}'''.replace("                                        ", "").replace("\n\n", "\n"))
            return level_list
        
        wiki_result = ["<tabber>Regular={{SP Operator tiers"]
        wiki_result += level_lister(self.basedata)
        wiki_result.append("}}|-|Elite={{SP Operator tiers")
        wiki_result += level_lister(self.golddata)
        wiki_result.append("}}</tabber>")
        script_result(wiki_result, True)

    '''
    <tabber>Regular={{SP Operator tiers
|t1 lv = 40
|t1 sklv = 4
|t2 lv = 1,10
|t2 sklv = 4
|t3 lv = 1,40
|t3 sklv = 4
|t4 lv = 1,70
|t4 sklv = 4
|t5 lv = 2,1
|t5 sklv = 4
|t6 lv = 2,30
|t6 sklv = 4
}}|-|Elite={{SP Operator tiers
|t1 lv = 1,70
|t1 sklv = 7
|t2 lv = 2,40
|t2 sklv = 7
|t2 modst = 1
|t3 lv = 2,50
|t3 sklv = 7
|t3 modst = 2
|t4 lv = 2,60
|t4 sklv = 7
|t4 modst = 2
|t5 lv = 2,70
|t5 sklv = 7
|t5 modst = 2
|t6 lv = 2,90
|t6 sklv = 10
|t6 modst = 3
}}</tabber>
    '''

class AC_DATA_CHARCHESS():
    def __init__(self, data_season):
        self.data   = charChessData(data_season)
        self.data_a = {k:v for k,v in self.data.items() if k.endswith("a")}
    
    def toCSV(self, separator : str = "|"):
        csv_header  = ["ID", "chessType", "chessLevel", "charId", "charname", "backupCharId", "backupcharname", "bondIds", "garrisonIds", "garrisonIds_gold", "backupgarrisonIds", "backupgarrisonIds_gold"]
        csv_keys    = ["chessType", "chessLevel", "charId", "charname", "backupCharId", "backupcharname", "bondIds", "garrisonIds", "garrisonIds_gold", "backupgarrisonIds", "backupgarrisonIds_gold"]
        DictToCSV(self.data_a, csv_header, csv_keys, separator)

    def toWIKI(self):
        def chess_lister(data : dict, mode : Literal["main", "reserved"]):
            chess_list = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
            for chess in data:
                chess_data  = data[chess]
                chessLevel  = chess_data["chessLevel"]
                charname    = chess_data["charname"] if mode == "main" else chess_data["backupcharname"]
                if charname:
                    chess_list[chessLevel].append(charname)
                
            return [f'|t{k} ops = {", ".join(chess_list[k])}' for k in chess_list]
        
        wiki_result = ["<tabber>Main={{SP roster"]
        wiki_result += chess_lister(self.data_a, "main")
        wiki_result.append("}}|-|Reserved={{SP roster")
        wiki_result += chess_lister(self.data_a, "reserved")
        wiki_result.append("}}</tabber>")
        script_result(wiki_result, True)

class AC_DATA_CULTIVATE():
    def __init__(self, data_season, data_ac):
        self.data       = cultivateEffect(data_season, data_ac)
    
    def toCSV(self, separator : str = "|"):
        csv_header  = ["ID", "evolvePhase", "charLevel", "atkPer", "defPer", "hpPer", "effectName", "effectDesc"]
        csv_keys    = ["evolvePhase", "charLevel", "atkPer", "defPer", "hpPer", "effectName", "effectDesc"]
        DictToCSV(self.data, csv_header, csv_keys, separator)

class AC_DATA_TRAP():
    def __init__(self, data_season):
        self.data   = trapChessData(data_season)
    
    def toCSV(self, separator : str = "|"):
        csv_header  = ["ID", "charId", "purchasePrice", "hideInShop", "effectId", "giveBondId", "givePowerId", "canGiveBond", "itemType", "effectName", "effectDesc"]
        csv_keys    = ["charId", "purchasePrice", "hideInShop", "effectId", "giveBondId", "givePowerId", "canGiveBond", "itemType", "effectName", "effectDesc"]
        DictToCSV(self.data, csv_header, csv_keys, separator)

def bandData(data_season : dict, data_ac : dict) -> dict:
    bands_data = {}
    for band in data_season["bandDataListDict"]:
        band_season_data : dict = data_season["bandDataListDict"][band]
        band_data_dict : dict   = data_ac["bandDataDict"][band]
        bands_data[band] = {
                                "band_id"         : band, 
                                "band_name"       : band_data_dict.get("bandName", band), 
                                "band_icon"       : band_data_dict.get("bandIconId", band), 
                                "band_initiator"  : "", 
                                "band_hp"         : band_season_data.get("totalHp"), 
                                "band_effect"     : band_season_data.get("bandDesc"), 
                                "band_cond"       : band_data_dict.get("unlockDesc", "") or "",  
                            }
    return bands_data

def baseRewardData(data_season : dict) -> dict:
    reward_data = {}
    for reward in data_season["baseRewardDataList"]:
        reward_data[reward["round"]] = {
                                            "item_id"       : ITEM_DATA.getname(reward["item"]["id"]),
                                            "item_name"     : reward["item"]["id"],
                                            "item_count"    : reward["item"]["count"],
                                            "daily_point"   : reward["dailyMissionPoint"],
                                        }
    return reward_data

def bondInfo(data_season : dict, data_ac : dict) -> dict:
    def mini_params(params : list):
        params_dict = {}
        for param in params:
            key = param["key"]
            params_dict[key] = mini_blackboard(param["blackboard"])
        return params_dict
        
    def param_sub(group1 , ParamBase, ParamPerStack, params):
        pattern = group1.split(":")
        base_param = ParamBase[int(pattern[0])]
        base_value = ""
        stack_param = ParamPerStack[int(pattern[0])]
        stack_value = ""
        for key in params:
            if base_param in params[key] and stack_param in params[key]:
                base_value  = blackboard_format(params[key][base_param], pattern[1])
                stack_value = blackboard_format(params[key][stack_param], pattern[1])
                break
            elif base_param in params[key] and stack_param in params[key]:
                printr(f'There\'re some glitch in The Matrix : {Y}{params[key]}{RE} ({G}{base_param}{RE}/{B}{stack_param}{RE})')
                exit()
            
        return f'{base_value} (+{stack_value} per stack)'
    
    def bondStackdesc(effectId, ParamBase, ParamPerStack):
        desc    = data_season["effectInfoDataDict"][effectId]["effectDesc"]
        params  = mini_params(data_season["effectBuffInfoDataDict"][effectId])
        
        if len(ParamBase) != len(ParamPerStack):
            printr(f'{Y}Unequal parameter length ParamBase:ParamPerStack = {len(ParamBase)}:{len(ParamPerStack)}')
            exit()
        
        while re.search(r'{.+?}', desc):
            #printc(effectId, desc)
            desc = re.sub(r'{(.+?)}', lambda x : param_sub(x.group(1), ParamBase, ParamPerStack, params), desc, 1)
        
        return wiki_text(desc)
    
    bond_dict = {}
    for bond in data_season["bondInfoDict"]:
        bond_data = data_season["bondInfoDict"][bond]
        bond_stackdesc = bondStackdesc(bond_data["effectId"], bond_data["descParamBaseList"], bond_data["descParamPerStackList"])
        bond_dict[bond] = {
                                "bond_name"                     : bond_data["name"],
                                "bond_desc"                     : wiki_text(bond_data["desc"]),
                                "bond_stackdesc"                : bond_stackdesc,
                                "bond_iconId"                   : bond_data["iconId"],
                                "bond_activeCount"              : bond_data["activeCount"],
                                "bond_effectId"                 : bond_data["effectId"],
                                "bond_activeType"               : bond_data["activeType"],
                                "bond_isActiveInDeck"           : bond_data["isActiveInDeck"],
                                "bond_powerIdList"              : ", ".join(data_ac["bondInfoDict"][bond]["powerIdList"]),
                                "bond_descParamBaseList"        : bond_data["descParamBaseList"],
                                "bond_descParamPerStackList"    : bond_data["descParamPerStackList"],
                                "bond_noStack"                  : bond_data["noStack"],
                            }
    return bond_dict

def garrisonData(data_season : dict) -> dict:
    garrison_dict = {}
    for garrison in data_season["garrisonDataDict"]:
        garrison_data = data_season["garrisonDataDict"][garrison]
        garrison_dict[garrison] = {
                                        "garrison_desc"         : garrison_data["garrisonDesc"],
                                        "garrison_type"         : garrison_data["eventType"],
                                        "garrison_typedesc"     : garrison_data["eventTypeDesc"],
                                        "garrison_typeicon"     : garrison_data["eventTypeIcon"],
                                        "garrison_typesicon"    : garrison_data["eventTypeSmallIcon"],
                                        "garrison_effecttype"   : garrison_data["effectType"],
                                    }
    return garrison_dict

def milestoneList(data_season : dict, token_id : str, token_name) -> dict:
    milestone_dict = {}
    for milestone in data_season["milestoneList"]:
        milestone_Lvl    = milestone["milestoneLvl"]
        token_Num        = milestone["tokenNum"]
        reward_ID        = milestone["rewardItem"]["id"]
        reward_Type      = milestone["rewardItem"]["type"]
        reward_Count     = milestone["rewardItem"]["count"]
        match reward_Type:
            case "CHAR_SKIN":
                reward_Name     = SKIN_DATA.getname(reward_ID)
                reward_iconId   = reward_ID
            case "PLAYER_AVATAR":
                reward_Name     = DISPLAY_DATA.getname(reward_ID)
                reward_iconId   = reward_ID
            case _:
                reward_Name     = ITEM_DATA.getname(reward_ID)
                reward_iconId   = ITEM_DATA.geticonId(reward_ID)
        
        milestone_dict[milestone_Lvl] = {
                                            "milestone_tokenID"         : token_id,
                                            "milestone_tokenName"       : token_name,
                                            "milestone_tokenNum"        : token_Num,
                                            "milestone_rewardID"        : reward_ID,
                                            "milestone_rewardiconId"    : reward_iconId,
                                            "milestone_rewardName"      : reward_Name,
                                            "milestone_rewardCount"     : reward_Count,
                                            "milestone_rewardType"      : reward_Type,
                                        }
    return milestone_dict

def FactorInfo(data_season : dict) -> dict:
    factor_dict = {}
    for factor in data_season["modeFactorInfo"]:
        factor_dict[factor] = data_season["modeFactorInfo"][factor]
    
    for factor in data_season["difficultyFactorInfo"]:
        if factor in factor_dict:
            printr(f'There dupe Factor in between {G}Mode{RE} and {B}Difficulty{RE} somehow : {factor}')
            exit()
        else:
            factor_dict[factor] = data_season["difficultyFactorInfo"][factor]
    return factor_dict

def ChessInfo(data_seaon : dict) -> dict:
    chess_info = {"base" : {}, "gold" : {}}
    for level in data_seaon["shopCharChessInfoData"]:
        level_data = data_seaon["shopCharChessInfoData"][level]
        chess_info["base"][level] = {
                                        "evolvePhase"       : level_data[0]["evolvePhase"],
                                        "charLevel"         : level_data[0]["charLevel"],
                                        "skillLevel"        : level_data[0]["skillLevel"],
                                        "favorPoint"        : level_data[0]["favorPoint"],
                                        "equipLevel"        : level_data[0]["equipLevel"],
                                        "purchasePrice"     : level_data[0]["purchasePrice"],
                                        "chessSoldPrice"    : level_data[0]["chessSoldPrice"],
                                        "eliteIconId"       : level_data[0]["eliteIconId"],
        }
        chess_info["gold"][level] = {
                                        "evolvePhase"       : level_data[1]["evolvePhase"],
                                        "charLevel"         : level_data[1]["charLevel"],
                                        "skillLevel"        : level_data[1]["skillLevel"],
                                        "favorPoint"        : level_data[1]["favorPoint"],
                                        "equipLevel"        : level_data[1]["equipLevel"],
                                        "purchasePrice"     : level_data[1]["purchasePrice"],
                                        "chessSoldPrice"    : level_data[1]["chessSoldPrice"],
                                        "eliteIconId"       : level_data[1]["eliteIconId"],
        }
    return chess_info

def cultivateEffect(data_season : dict, data_ac : dict) -> dict:
    effect_data = {}
    for effect in data_ac["cultivateEffectList"]:
        effectId = effect["effectId"]
        effect_data[effectId] = {
                                    "evolvePhase"   : effect["evolvePhase"],
                                    "charLevel"     : effect["charLevel"],
                                    "atkPer"        : effect["atkPer"],
                                    "defPer"        : effect["defPer"],
                                    "hpPer"         : effect["hpPer"],
                                    "effectName"    : data_season["effectInfoDataDict"][effectId]["effectName"],
                                    "effectDesc"    : data_season["effectInfoDataDict"][effectId]["effectDesc"],
        }
    
    return sorted_dict_key(effect_data)

def charChessData(data_season : dict) -> dict:
    charChess_dict = {}
    for char in data_season["charShopChessDatas"]:
        char_data       = data_season["charShopChessDatas"][char]
        char_data_dict  = data_season["charChessDataDict"]
        char_b          = char_data["goldenChessId"]
        notDIY          = char_data["chessType"] != "DIY"
        for key in [char, char_b] :
            charChess_dict[key] = {
                                        "chessType"                 : char_data["chessType"],
                                        "chessLevel"                : char_data["chessLevel"],
                                        "charId"                    : char_data["charId"],
                                        "charname"                  : CHARACTER_DATA.getname(char_data["charId"]) if notDIY else "",
                                        "backupCharId"              : char_data["backupCharId"],
                                        "backupcharname"            : CHARACTER_DATA.getname(char_data["backupCharId"]) if notDIY else "",
                                        "bondIds"                   : ", ".join(char_data_dict[char]["bondIds"]) if notDIY else "",
                                        "garrisonIds"               : char_data_dict[char]["garrisonIds"][0] if notDIY else "",
                                        "garrisonIds_gold"          : char_data_dict[char_b]["garrisonIds"][0] if notDIY else "",
                                        "backupgarrisonIds"         : char_data_dict[char]["garrisonIds"][-1] if notDIY else "",
                                        "backupgarrisonIds_gold"    : char_data_dict[char_b]["garrisonIds"][-1] if notDIY else "",
                                    }
    return sorted_dict_key(charChess_dict)

def trapChessData(data_season : dict) -> dict:
    trap_dict = {}
    for trap in data_season["trapChessDataDict"]:
        trap_data   = data_season["trapChessDataDict"][trap]
        base_trap   = data_season["chessNormalIdLookupDict"][trap]
        trap_shop   = data_season["trapShopChessDatas"][base_trap]["hideInShop"]
        effect_data = data_season["effectInfoDataDict"]
        effect_id   = trap_data["effectId"]
        trap_dict[trap] = {
                                "charId"        : trap_data["charId"],
                                "purchasePrice" : trap_data["purchasePrice"],
                                "hideInShop"    : trap_shop  or "-",
                                "effectId"      : effect_id,
                                "giveBondId"    : trap_data["giveBondId"] or "-",
                                "givePowerId"   : trap_data["givePowerId"] or "-",
                                "canGiveBond"   : trap_data["canGiveBond"] or "-",
                                "itemType"      : trap_data["itemType"],
                                "effectName"    : effect_data[effect_id]["effectName"],
                                "effectDesc"    : effect_data[effect_id]["effectDesc"],
                            }
    return sorted_dict_key(trap_dict, lambda x : x.split("_")[2] + x.split("_")[4] + x.split("_")[3])

ENEMY_DATA      = Enemy_Database().DB
ITEM_DATA       = Item_Database()
CHARACTER_DATA  = Character_Database()
SKIN_DATA       = Skin_Database()
DISPLAY_DATA    = Display_Database()

ac_data         = AC_DATA("act1autochess")

#ac_data.bandData.toCSV()
#ac_data.bandData.toWIKI()
#ac_data.baseRewardDataList.toCSV()
#ac_data.bondInfoDict.toCSV("!")
#ac_data.garrisonDataDict.toCSV()
#ac_data.milestoneList.toCSV()
#ac_data.milestoneList.toWIKI()
#ac_data.FactorInfo.toCSV()
#ac_data.shopCharChessInfo.toCSV("base")
#ac_data.shopCharChessInfo.toCSV("gold")
#ac_data.shopCharChessInfo.toWIKI()
#ac_data.cultivateEffectList.toCSV()
#ac_data.charChessDataDict.toCSV()
#ac_data.charChessDataDict.toWIKI()
#ac_data.trapChessDataDict.toCSV()