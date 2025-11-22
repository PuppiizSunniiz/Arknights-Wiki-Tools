
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

class SP_DATA:
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
            self.baseRewardDataList     = SP_DATA_BASEREWARD(self.seasonData)
            self.bandData               = SP_DATA_BAND(self.seasonData, self.autoChessData)
            self.bondInfoDict           = SP_DATA_BOND(self.seasonData, self.autoChessData)
            self.garrisonDataDict       = SP_DATA_GARRISON(self.seasonData)
            self.milestoneList          = SP_DATA_MILESTONE(self.seasonData, season)
            self.FactorInfo             = SP_DATA_FACTOR(self.seasonData)
            self.shopCharChessInfo      = SP_DATA_CHESSINFO(self.seasonData)
            self.cultivateEffectList    = SP_DATA_CULTIVATE(self.seasonData, self.autoChessData)
            
            self.charChessDataDict      = SP_DATA_CHARCHESS(self.seasonData)
            self.trapChessDataDict      = SP_DATA_TRAP(self.seasonData)
            
            self.bossInfoDict           = SP_DATA_BOSS(self.seasonData, self.autoChessData)
            
            #self.modeDataDict           = SP_DATA_MODE()
            #self.shopLevelDataDict      = SP_DATA_SHOP()
            #self.stageDatasDict         = SP_DATA_STAGE()
            #self.battleDataDict         = SP_DATA_BATTLE()
            #self.specialEnemyInfoDict   = SP_DATA_SPECENEMY()
            #self.enemyInfoDict          = SP_DATA_ENEMIES()
    
    def toCSV(self, file_type : Literal["csv", "txt", "xlsx"] = "xlsx"):
        for key in self.__dict__.keys():
            if hasattr(getattr(self, key), "toCSV"):
                printr(key, hasattr(getattr(self, key), "toCSV"))
                getattr(self, key).toCSV(main = "SP_DATA", file_type = file_type)

class SP_DATA_BAND:
    def __init__(self, data_season, data_ac):
        self.classname = "bandData"
        self.data, self.keys = bandData(data_season, data_ac)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)
    
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

class SP_DATA_BASEREWARD():
    def __init__(self, data_season):
        self.classname = "baseRewardData"
        self.data, self.keys = baseRewardData(data_season)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)

class SP_DATA_BOND():
    def __init__(self, data_season, data_ac):
        self.classname = "bondInfo"
        self.data, self.keys = bondInfo(data_season, data_ac)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)

class SP_DATA_GARRISON():
    def __init__(self, data_season):
        self.classname = "garrisonData"
        self.data, self.keys = garrisonData(data_season)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)

class SP_DATA_MILESTONE():
    def __init__(self, data_season, season):
        if len(DB["json_activity"]["activityItems"][season]) != 1 :
            printr(f'Multiple milestone token detected : {Y}{DB["json_activity"]["activityItems"][season]}')
            exit()
        else :
            self.classname          = "milestoneList"
            self.token              = DB["json_activity"]["activityItems"][season][0]
            self.tokenname          = ITEM_DATA.getname(self.token)
            self.data, self.keys    = milestoneList(data_season, self.token, self.tokenname)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)

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

class SP_DATA_FACTOR():
    def __init__(self, data_season):
        self.classname = "FactorInfo"
        self.data, self.keys = FactorInfo(data_season)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)

class SP_DATA_CHESSINFO():
    def __init__(self, data_season):
        self.classname = "ChessInfo"
        self.data, self.keys = ChessInfo(data_season)
        self.basedata   = self.data["base"]
        self.golddata   = self.data["gold"]

    def toCSV(self, main : str = "", mode : Literal["base", "gold"] = "base", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        if main:
            DictToCSV(self.data["base"], self, main = main, separator = separator, sheet_name = "ChessInfo_b", file_type = file_type)
            DictToCSV(self.data["gold"], self, main = main, separator = separator, sheet_name = "ChessInfo_g", file_type = file_type)
        else:
            DictToCSV(self.data[mode], self, main = main, separator = separator, file_type = file_type)
    
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

class SP_DATA_CHARCHESS():
    def __init__(self, data_season):
        self.classname = "charChessData"
        self.data, self.keys = charChessData(data_season)
        self.data_a = {k:v for k,v in self.data.items() if k.endswith("a")}

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data_a, self, main = main, separator = separator, file_type = file_type)

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

class SP_DATA_CULTIVATE():
    def __init__(self, data_season, data_ac):
        self.classname = "cultivateEffect"
        self.data, self.keys = cultivateEffect(data_season, data_ac)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)

class SP_DATA_TRAP():
    def __init__(self, data_season):
        self.classname = "trapChessData"
        self.data, self.keys = trapChessData(data_season)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)

class SP_DATA_BOSS():
    def __init__(self, data_season, data_ac):
        self.classname = "bossInfoDict"
        self.data, self.keys = bossInfoDict(data_season, data_ac)

    def toCSV(self, main : str = "", separator : str = "|", file_type : Literal["csv", "txt", "xlsx"] = "txt"):
        DictToCSV(self.data, self, main = main, separator = separator, file_type = file_type)

def bandData(data_season : dict, data_ac : dict) -> dict:
    bands_data = {}
    data_key = []
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
        if not data_key:
            data_key = list(bands_data[band])
    return bands_data, data_key

def baseRewardData(data_season : dict) -> dict:
    reward_data = {}
    data_key = []
    for reward in data_season["baseRewardDataList"]:
        round = reward["round"]
        reward_data[round] = {
                                            "round"         : round,
                                            "item_id"       : ITEM_DATA.getname(reward["item"]["id"]),
                                            "item_name"     : reward["item"]["id"],
                                            "item_count"    : reward["item"]["count"],
                                            "daily_point"   : reward["dailyMissionPoint"],
                                        }
        if not data_key:
            data_key = list(reward_data[round])
    return reward_data, data_key

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
    data_key = []
    for bond in data_season["bondInfoDict"]:
        bond_data = data_season["bondInfoDict"][bond]
        bond_stackdesc = bondStackdesc(bond_data["effectId"], bond_data["descParamBaseList"], bond_data["descParamPerStackList"])
        bond_dict[bond] = {
                                "bond_id"                       : bond,
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
        if not data_key:
            data_key = list(bond_dict[bond].keys())
    return bond_dict, data_key

def garrisonData(data_season : dict) -> dict:
    garrison_dict = {}
    data_key = []
    for garrison in data_season["garrisonDataDict"]:
        garrison_data = data_season["garrisonDataDict"][garrison]
        garrison_dict[garrison] = {
                                        "garrison_id"           : garrison,
                                        "garrison_desc"         : garrison_data["garrisonDesc"],
                                        "garrison_type"         : garrison_data["eventType"],
                                        "garrison_typedesc"     : garrison_data["eventTypeDesc"],
                                        "garrison_typeicon"     : garrison_data["eventTypeIcon"],
                                        "garrison_typesicon"    : garrison_data["eventTypeSmallIcon"],
                                        "garrison_effecttype"   : garrison_data["effectType"],
                                    }
        if not data_key:
            data_key = list(garrison_dict[garrison].keys())
    return sorted_dict_key(garrison_dict), data_key

def milestoneList(data_season : dict, token_id : str, token_name) -> dict:
    milestone_dict = {}
    data_key = []
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
                                            "milestone_Lvl"             : milestone_Lvl,
                                            "milestone_tokenID"         : token_id,
                                            "milestone_tokenName"       : token_name,
                                            "milestone_tokenNum"        : token_Num,
                                            "milestone_rewardID"        : reward_ID,
                                            "milestone_rewardiconId"    : reward_iconId,
                                            "milestone_rewardName"      : reward_Name,
                                            "milestone_rewardCount"     : reward_Count,
                                            "milestone_rewardType"      : reward_Type,
                                        }
        if not data_key:
            data_key = list(milestone_dict[milestone_Lvl].keys())
    return milestone_dict, data_key

def FactorInfo(data_season : dict) -> dict:
    factor_dict = {}
    data_key = []
    for factor in data_season["modeFactorInfo"]:
        factor_dict[factor] = {
                                        "Mode" : factor,
                                        "Factor" : data_season["modeFactorInfo"][factor],
                                    }
        if not data_key:
            data_key = list(factor_dict[factor].keys())
    
    for factor in data_season["difficultyFactorInfo"]:
        if factor in factor_dict:
            printr(f'There dupe Factor in between {G}Mode{RE} and {B}Difficulty{RE} somehow : {factor}')
            exit()
        else:
            factor_dict[factor] = {
                                        "Mode" : factor,
                                        "Factor" : data_season["difficultyFactorInfo"][factor],
                                    }
    return factor_dict, data_key

def ChessInfo(data_seaon : dict) -> dict:
    chess_info = {"base" : {}, "gold" : {}}
    elite_info = {"base" : 0, "gold" : 1}
    data_key = []
    for level in data_seaon["shopCharChessInfoData"]:
        level_data = data_seaon["shopCharChessInfoData"][level]
        for elite in ["base", "gold"]:
            chess_info[elite][level] = {
                                            "chess_elite"       : elite,
                                            "chess_level"       : level,
                                            "evolvePhase"       : level_data[elite_info[elite]]["evolvePhase"],
                                            "charLevel"         : level_data[elite_info[elite]]["charLevel"],
                                            "skillLevel"        : level_data[elite_info[elite]]["skillLevel"],
                                            "favorPoint"        : level_data[elite_info[elite]]["favorPoint"],
                                            "equipLevel"        : level_data[elite_info[elite]]["equipLevel"],
                                            "purchasePrice"     : level_data[elite_info[elite]]["purchasePrice"],
                                            "chessSoldPrice"    : level_data[elite_info[elite]]["chessSoldPrice"],
                                            "eliteIconId"       : level_data[elite_info[elite]]["eliteIconId"],
            }
        if not data_key:
            data_key = list(chess_info[elite][level].keys())
    return chess_info, data_key

def cultivateEffect(data_season : dict, data_ac : dict) -> dict:
    effect_data = {}
    data_key = []
    for effect in data_ac["cultivateEffectList"]:
        effectId = effect["effectId"]
        effect_data[effectId] = {
                                    "effectId"      : effectId,
                                    "evolvePhase"   : effect["evolvePhase"],
                                    "charLevel"     : effect["charLevel"],
                                    "atkPer"        : effect["atkPer"],
                                    "defPer"        : effect["defPer"],
                                    "hpPer"         : effect["hpPer"],
                                    "effectName"    : data_season["effectInfoDataDict"][effectId]["effectName"],
                                    "effectDesc"    : data_season["effectInfoDataDict"][effectId]["effectDesc"],
        }
        if not data_key:
            data_key = list(effect_data[effectId].keys())
    return sorted_dict_key(effect_data), data_key

def charChessData(data_season : dict) -> dict:
    charChess_dict = {}
    data_key = []
    for char in data_season["charShopChessDatas"]:
        char_data       = data_season["charShopChessDatas"][char]
        char_data_dict  = data_season["charChessDataDict"]
        char_b          = char_data["goldenChessId"]
        notDIY          = char_data["chessType"] != "DIY"
        for key in [char, char_b] :
            charChess_dict[key] = {
                                        "chessId"                   : char,
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
            if not data_key:
                data_key = list(charChess_dict[key].keys())
    return sorted_dict_key(charChess_dict), data_key

def trapChessData(data_season : dict) -> dict:
    trap_dict = {}
    data_key = []
    for trap in data_season["trapChessDataDict"]:
        trap_data   = data_season["trapChessDataDict"][trap]
        base_trap   = data_season["chessNormalIdLookupDict"][trap]
        trap_shop   = data_season["trapShopChessDatas"][base_trap]["hideInShop"]
        effect_data = data_season["effectInfoDataDict"]
        effect_id   = trap_data["effectId"]
        trap_dict[trap] = {
                                "trapId"        : trap,
                                "charId"        : trap_data["charId"],
                                "purchasePrice" : trap_data["purchasePrice"],
                                "hideInShop"    : trap_shop or "-",
                                "effectId"      : effect_id,
                                "giveBondId"    : trap_data["giveBondId"] or "-",
                                "givePowerId"   : trap_data["givePowerId"] or "-",
                                "canGiveBond"   : trap_data["canGiveBond"] or "-",
                                "itemType"      : trap_data["itemType"],
                                "effectName"    : effect_data[effect_id]["effectName"],
                                "effectDesc"    : effect_data[effect_id]["effectDesc"],
                            }
        if not data_key:
            data_key = list(trap_dict[trap].keys())
    return sorted_dict_key(trap_dict, lambda x : x.split("_")[2] + x.split("_")[4] + x.split("_")[3]), data_key

def bossInfoDict(data_season : dict, data_ac : dict) -> dict:
    boss_info = {}
    data_key = []
    for boss in data_season["bossInfoDict"]:
        boss_info[boss] = {
                                "bossId"            : boss,
                                "bossdatabaseID"    : data_ac["bossInfoDict"][boss]["enemyId"],
                                "bossHandbookID"    : data_ac["bossInfoDict"][boss]["handbookEnemyId"],
                                "bloodPoint"        : data_season["bossInfoDict"][boss]["bloodPoint"],
                                "bloodPointNormal"  : data_season["bossInfoDict"][boss]["bloodPointNormal"],
                                "bloodPointHard"    : data_season["bossInfoDict"][boss]["bloodPointHard"],
                                "isHidingBoss"      : data_season["bossInfoDict"][boss]["isHidingBoss"] or "-",
        }
        if not data_key:
            data_key = list(boss_info[boss].keys())
    return boss_info, data_key

ENEMY_DATA      = Enemy_Database().DB
ITEM_DATA       = Item_Database()
CHARACTER_DATA  = Character_Database()
SKIN_DATA       = Skin_Database()
DISPLAY_DATA    = Display_Database()

SP_DATA         = SP_DATA("act1autochess")

SP_DATA.toCSV("xlsx")

###### Graveyard ######
'''#SP_DATA.bandData.toCSV()
#SP_DATA.bandData.toWIKI()
#SP_DATA.baseRewardDataList.toCSV()
#SP_DATA.bondInfoDict.toCSV(separator = "!")
#SP_DATA.garrisonDataDict.toCSV()
#SP_DATA.milestoneList.toCSV()
#SP_DATA.milestoneList.toWIKI()
#SP_DATA.FactorInfo.toCSV()
#SP_DATA.shopCharChessInfo.toCSV("base")
#SP_DATA.shopCharChessInfo.toCSV("gold")
#SP_DATA.shopCharChessInfo.toWIKI()
#SP_DATA.cultivateEffectList.toCSV()
#SP_DATA.charChessDataDict.toCSV()
#SP_DATA.charChessDataDict.toWIKI()
#SP_DATA.trapChessDataDict.toCSV()
#SP_DATA.bossInfoDict.toCSV()'''