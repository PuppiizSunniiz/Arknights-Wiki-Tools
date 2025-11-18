
import re
from Wiki_OOP.char_data import Character_Database
from Wiki_OOP.enemy_data import Enemy_Database
from Wiki_OOP.item_data import Item_Database
from pyFunction import B, G, RE, Y, blackboard_format, printc, printr, script_result
from pyFunction_Wiki import load_json, mini_blackboard, wiki_story, wiki_text

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
            #self.modeDataDict           = AC_DATA_MODE()
            self.baseRewardDataList     = AC_DATA_BASEREWARD(self.seasonData)
            self.bandData               = AC_DATA_BAND(self.seasonData, self.autoChessData)
            #self.charChessDataDict      = AC_DATA_CHESS()
            #self.shopLevelDataDict      = AC_DATA_SHOP()
            #self.trapChessDataDict      = AC_DATA_TRAP()
            #self.stageDatasDict         = AC_DATA_STAGE()
            #self.battleDataDict         = AC_DATA_BATTLE()
            self.bondInfoDict           = AC_DATA_BOND(self.seasonData)

class AC_DATA_BAND:
    def __init__(self, data_season, data_ac):
        self.data : dict = bandData(data_season, data_ac)
    
    def toCSV(self, separator : str = "|"):
        csv_header = ["ID", "Name", "HP", "Effect", "Condition"]
        csv_result = [separator.join(csv_header)]
        for band in self.data:
            band_data : dict = self.data[band]
            band_name       = band_data.get("band_name")
            band_hp         = band_data.get("band_hp") 
            band_effect     = band_data.get("band_effect")
            band_cond       = band_data.get("band_cond")
            band_result     = [band, band_name, str(band_hp), band_effect, band_cond]
            csv_result.append(separator.join(band_result))
        script_result(csv_result, True)
    
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
        csv_header = ["Round", "Item ID", "Item Name", "Count", "Daily Point"]
        csv_result = [separator.join(csv_header)]
        for round in self.data:
            reward_data : dict = self.data[round]
            reward_item         = reward_data.get("item_id")
            reward_item_name    = reward_data.get("item_name")
            reward_count        = reward_data.get("item_count") 
            reward_point        = reward_data.get("daily_point")
            reward_result       = [str(round), reward_item, reward_item_name, str(reward_count), str(reward_point)]
            csv_result.append(separator.join(reward_result))
        script_result(csv_result, True)

class AC_DATA_BOND():
    def __init__(self, data_season):
        self.data   = bondInfo(data_season)
    
    def toCSV(self, separator : str = "|"):
        csv_header = ["ID", "Name", "Active Type", "Active Count", "Full Desc", "Stack Desc"]
        csv_result = [separator.join(csv_header)]
        for bond in self.data:
            bond_data : dict = self.data[bond]
            bond_name       = bond_data.get("bond_name")
            bond_type       = bond_data.get("bond_activeType") 
            bond_count      = bond_data.get("bond_activeCount")
            bond_full_desc  = bond_data.get("bond_desc")
            bond_stack_desc = bond_data.get("bond_stackdesc")
            bond_result     = [bond, bond_name, bond_type, str(bond_count), bond_full_desc, bond_stack_desc]
            csv_result.append(separator.join(bond_result))
        script_result(csv_result, True)
            

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

def bondInfo(data_season : dict) -> dict:
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
                base_value = blackboard_format(params[key][base_param], pattern[1])
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
                                "bond_descParamBaseList"        : bond_data["descParamBaseList"],
                                "bond_descParamPerStackList"    : bond_data["descParamPerStackList"],
                                "bond_noStack"                  : bond_data["noStack"],
                            }
    return bond_dict

ENEMY_DATA      = Enemy_Database().DB
ITEM_DATA       = Item_Database()
CHARACTER_DATA  = Character_Database()

ac_data         = AC_DATA("act1autochess")

#ac_data.bandData.toCSV()
#ac_data.bandData.toWIKI()
#ac_data.baseRewardDataList.toCSV()
#ac_data.bondInfoDict.toCSV("!")