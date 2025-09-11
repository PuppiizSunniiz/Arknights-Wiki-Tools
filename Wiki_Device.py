from types import NoneType
from pyFunction import decimal_format, json_load, printr, script_result
from pyFunction_Wiki import load_json, range_template, spType, wiki_text

used_json = [
                "json_activityEN",
                "json_character",
                "json_characterEN",
                "json_skillEN",
            ]
DB = load_json(used_json)
DB["json_characterJP"] = json_load("json/gamedata/ArknightsGameData_YoStar/ja_JP/gamedata/excel/character_table.json")
DB["json_characterKR"] = json_load("json/gamedata/ArknightsGameData_YoStar/ko_KR/gamedata/excel/character_table.json")

def device_info(device_list : list) -> dict[str, str|int|float]:
    device_data = {}
    for device_name in device_list:
        for key in DB["json_characterEN"]:
            if key.find("trap_") != -1 and DB["json_characterEN"][key]["name"] == device_name:
                device_skill = DB["json_characterEN"][key]["skills"][0]["skillId"] if DB["json_characterEN"][key]["skills"] else ""
                device_data[device_name] = {
                                                "name"      :   device_name,
                                                "cnname"    :   DB["json_character"][key]["name"],
                                                "jpname"    :   DB["json_characterJP"][key]["name"],
                                                "krname"    :   DB["json_characterKR"][key]["name"],
                                                "othername" :   ", ".join(set([DB["json_characterEN"][key]["appellation"].capitalize(), 
                                                                                DB["json_character"][key]["appellation"].capitalize(), 
                                                                                DB["json_characterJP"][key]["appellation"].capitalize(), 
                                                                                DB["json_characterKR"][key]["appellation"].capitalize()])),
                                                
                                                "range"     :   DB["json_characterEN"][key]["phases"][-1]["rangeId"],
                                                "trait"     :   DB["json_characterEN"][key]["description"],
                                                "hp"        :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["maxHp"],
                                                "atk"       :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["atk"],
                                                "def"       :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["def"],
                                                "res"       :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["magicResistance"],
                                                "aggro"     :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["tauntLevel"],
                                                "block"     :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["blockCnt"],
                                                "interval"  :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["baseAttackTime"],
                                                "rdp"       :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["respawnTime"],
                                                "cost"      :   DB["json_characterEN"][key]["phases"][-1]["attributesKeyFrames"][-1]["data"]["cost"],
                                                
                                                "talent"    :   DB["json_characterEN"][key]["talents"],
                                                
                                                "skill"     :   device_skill,
                                                
                                                "skillname" :   "",
                                                "sp"        :   "",
                                                "type"      :   "",
                                                "spcost"    :   "",
                                                "spinit"    :   "",
                                                "duration"  :   0,
                                                "skillrange":   "",
                                                "effect"    :   "",
                                                "effect_bb" :   "",
                                            }
                if device_skill :
                    device_data[device_name].update({
                                                    "skillname" :   DB["json_skillEN"][device_skill]["levels"][0]["name"],
                                                    "sp"        :   DB["json_skillEN"][device_skill]["levels"][0]["spData"]["spType"],
                                                    "type"      :   DB["json_skillEN"][device_skill]["levels"][0]["skillType"],
                                                    "spcost"    :   DB["json_skillEN"][device_skill]["levels"][0]["spData"]["spCost"],
                                                    "spinit"    :   DB["json_skillEN"][device_skill]["levels"][0]["spData"]["initSp"],
                                                    "duration"  :   DB["json_skillEN"][device_skill]["levels"][0]["duration"],
                                                    "skillrange":   DB["json_skillEN"][device_skill]["levels"][0]["rangeId"],
                                                    "effect"    :   DB["json_skillEN"][device_skill]["levels"][0]["description"],
                                                    "effect_bb" :   DB["json_skillEN"][device_skill]["levels"][0]["blackboard"],
                    })
    return device_data

def device_talent_writer(device_talents : list|NoneType) -> str:
    if isinstance(device_talents, NoneType):
        return ""
    talent_list = ["==Talent=="]
    for device_talent in device_talents:
        talent_list.append(f'{{{{Talent\n|name = {device_talent["candidates"][0]["name"]}')
        for candidate_i in range(len(device_talent["candidates"])):
            talent_list.append(f'|desc{candidate_i} = {device_talent["candidates"][candidate_i]["description"]}')
        talent_list.append(f'}}}}')
    return  "\n".join(talent_list)

def device_skill_writer(device_data : dict) -> str:
    if not device_data["skill"]:
        return ""
    skill_writer = f'''==Skill==
                        {{{{Device skill
                        |name = {device_data["skillname"]}
                        |icon = {device_data["name"].replace("'", "").replace(" ","")}
                        |sp = {"" if device_data["type"].lower() == "passive" else spType(device_data["sp"])}
                        |type = {device_data["type"].lower()}
                        |cost = {device_data["spinit"]}, {device_data["spcost"]}
                        |duration = {decimal_format(device_data["duration"]) if device_data["duration"] > 0 else ""}
                        |range = {range_template(device_data["skillrange"])}
                        |effect = {wiki_text((device_data["effect"], device_data["effect_bb"]))}}}}}'''.replace("                        ", "")
    return skill_writer

def device_info_writer(device_list : list|str, gamemode = "") -> NoneType:
    writer = []
    
    if isinstance(device_list, str):
        device_list = [device_list]
    
    device_data : dict[str, str|int|float] = device_info(device_list)
    
    for device in device_data.keys():
        #printr(device_data[device])
        device_article = f'''{{{{Construction}}}}
                            {{{{Device infobox
                            |name = {device_data[device]["name"]}
                            |title =
                            |image = {device_data[device]["name"]}.png
                            |othername = {device_data[device]["othername"]}
                            |intro = <!--Icebreaker Games 1-->
                            |feature = <!--Icebreaker Games 1-->
                            |cnname = {device_data[device]["cnname"]}
                            |jpname = {device_data[device]["jpname"]}
                            |krname = {device_data[device]["krname"]}
                            |type = <!--Deployable/Static-->
                            |position = <!--Low/High-->
                            |invulnerable = <!--yes|no|nodamage|notarget|nodestroy|notapplicable-->
                            |healable = 
                            |user = 
                            |enemy = 
                            {f'|{gamemode} = true' if gamemode else ""}
                            }}}}
                            \'\'\'{device_data[device]["name"]}\'\'\' is a [[deployable device]]/[[static device]] in \'\'[[Arknights]]\'\'.
                            
                            ==Overview==
                            {{{{Stub|section}}}}
                            
                            ==Appearances==
                            
                            ==Stats==
                            {{{{Device info
                            |range = {range_template(device_data[device]["range"]) if device_data[device]["range"] else ""}
                            |trait = {device_data[device]["trait"] if device_data[device]["trait"] else ""}
                            |hp = {device_data[device]["hp"]}
                            |hp note = <!--Redundant as {device_data[device]["name"]} is invulnerable-->
                            |atk = {device_data[device]["atk"]}
                            |atk note = <!--Redundant as {device_data[device]["name"]} does not attack-->
                            |def = {device_data[device]["def"]}
                            |res = {decimal_format(device_data[device]["res"])}
                            |aggro = {device_data[device]["aggro"]}
                            |block = {device_data[device]["block"]}
                            |interval = {device_data[device]["interval"]}
                            |rdp = {device_data[device]["rdp"]}
                            |cost = {device_data[device]["cost"]}
                            |align = <!--friendly/neutral/hostile-->}}}}
                            
                            {device_talent_writer(device_data[device]["talent"])}
                            
                            {device_skill_writer(device_data[device])}
                            
                            {f'==See also==\n{"\n".join([f'*[[{key}]]' for key in sorted(device_data.keys()) if key != device])}' if len(device_data.keys()) > 1 else ""}
                            
                            {{{{Devices}}}}{{{{Other devices}}}}
                            [[Category:Deployable devices]][[Category:Static devices]]
                            '''.replace("                            ", "").replace("\n\n\n\n", "\n\n").replace("\n\n\n", "\n\n")
        writer.append(f'\n# {device_data[device]["name"]}\n{device_article}')
    script_result(device_data)
    script_result(writer, True)

# device_info_writer(["Cheerleader", "Protective Gear Giver", "Chaotic Fireworks", "Beastmode Energy Drink", "Soda Dispenser"], "ig")
device_info_writer(["Facility Builder", "Expert Facility Builder", "Collapsed Junk Pile", "Construction Workshop", "Recuperation Pod", "Hydraulic Platform", "Concrete Roadblock", "Portable Exercise Rack",], "ig")

'''
deploy
# device_info_writer(["Cheerleader", "Protective Gear Giver", "Chaotic Fireworks", "Beastmode Energy Drink", "Soda Dispenser"], "ig")

static
# device_info_writer(["Expert Facility Builder", "Collapsed Junk Pile", "Construction Workshop", "Recuperation Pod", "Hydraulic Platform", "Concrete Roadblock", "Portable Exercise Rack",], "Static", True, "ig")
"trap_202_muworkg": {
    "name": "Expert Facility Builder",
    
"trap_203_mufrprn": {
    "name": "Collapsed Junk Pile",
    
  "trap_205_mufrfm": {
    "name": "Construction Workshop",
    
  "trap_206_mufrbk": {
    "name": "Recuperation Pod",
    
  "trap_207_mufrwl": {
    "name": "Hydraulic Platform",
    
  "trap_208_mufrst": {
    "name": "Concrete Roadblock",
    
  "trap_209_mufrbs": {
    "name": "Portable Exercise Rack",
    
    
'''