
from pyFunction_Wiki import load_json, wiki_story, wiki_text
from pyFunction import decimal_format, printr, script_result


used_json = [
                "json_battle_equip",
                "json_battle_equipEN",
                "json_item",
                "json_itemEN",
                "json_uniequip",
                "json_uniequipEN",
            ]
DB = load_json(used_json)

temp_mod = {}
temp_mod_txt = ""
json_mod = DB["json_uniequip"]
json_modEN = DB["json_uniequipEN"]
json_battle_mod = DB["json_battle_equip"]
json_battle_modEN = DB["json_battle_equipEN"]
new_mod = []

def mod_trait_search(mod_battle_data : dict):
    phase = mod_battle_data["phases"][0]
    parts = [part for part in phase["parts"] if part["target"] in ["TRAIT", "TRAIT_DATA_ONLY", "DISPLAY"]  and not part["isToken"]]
    candidate = []
    if len(parts) != 1 :
        printr(f'part have problemo (length = {len(parts)}) : {parts}')
    else:
        candidate = [(candidate["additionalDescription"] or candidate["overrideDescripton"], candidate["blackboard"]) for candidate in parts[0]["overrideTraitDataBundle"]["candidates"] if (candidate["additionalDescription"] or candidate["overrideDescripton"])]

    if len(candidate) != 1 :
        printr(f'candidate have problemo (candidate = {len(parts)}) : {candidate}')
    else:
        return wiki_text(candidate[0])

def mod_talent_search(mod_battle_data : dict):
    temp_talent = {}
    for i in [1, 2]:
        phase = mod_battle_data["phases"][i]
        parts = [part for part in phase["parts"] if part["addOrOverrideTalentDataBundle"]["candidates"] and part["addOrOverrideTalentDataBundle"]["candidates"][0]["upgradeDescription"] and not part["isToken"]]
        candidate = ""
        if len(parts) != 1 :
            printr(f'part have problemo (length = {len(parts)}) : {parts}')
            exit()
        else:
            candidate = (parts[0]["addOrOverrideTalentDataBundle"]["candidates"][0]["upgradeDescription"], parts[0]["addOrOverrideTalentDataBundle"]["candidates"][0]["blackboard"])
            talent_name = parts[0]["addOrOverrideTalentDataBundle"]["candidates"][0]["name"]

        if not candidate :
            printr(f'candidate have problemo (candidate = {len(parts)}) : {candidate}')
        else:
            temp_talent[f'{i}_name'] = talent_name
            temp_talent[i] = wiki_text(candidate)
    return temp_talent

def mod_blackboard(mod_battle_data : dict):
    temp_blackboard = []
    for phase in mod_battle_data["phases"]:
        temp_blackboard.append({bb["key"]:decimal_format(bb["value"]) for bb in phase["attributeBlackboard"]})
    return temp_blackboard

def mod_mat(mod_itemCost : dict):
    temp_mat = []
    for level in mod_itemCost.keys():
        for mat in mod_itemCost[level]:
            if mat["type"] == "MATERIAL" and mat["id"].startswith("3"):
                temp_mat.append(DB["json_itemEN"]["items"][mat["id"]]["name"])
    return temp_mat

for mod in json_modEN["equipTrackDict"][-1]["trackList"]:
    if mod["type"] == "INITIAL":
        continue
    else:
        new_mod.append(mod["equipId"])

for mod_id in new_mod:
    temp_mod_txt += f'{"#" * 80}\n\n{wiki_story(json_modEN["equipDict"][mod_id]["uniEquipDesc"].replace("—", "&mdash;"), join_str = "\n<br/>")}\n\n'
    temp_mod[mod_id] = {
                            "name" : json_modEN["equipDict"][mod_id]["uniEquipName"],
                            "trait" : mod_trait_search(json_battle_modEN[mod_id]),
                            "talent" : mod_talent_search(json_battle_modEN[mod_id]),
                            "blackboard" : mod_blackboard(json_battle_modEN[mod_id]),
                            "mat" : mod_mat(json_modEN["equipDict"][mod_id]["itemCost"]),
                            "desc" : wiki_story(json_modEN["equipDict"][mod_id]["uniEquipDesc"].replace("—", "&mdash;"))
                        }

script_result(temp_mod_txt, True)
script_result(temp_mod, False)