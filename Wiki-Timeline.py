from Wiki_pyFunction import load_json
from pyFunction import R, G, B, Y, RE, json_load, printr, script_result

used_json = [
                "json_character",
                "json_characterEN",
                "json_handbook_team",
                "json_handbook_teamEN",
                "json_stage",
                "json_stageEN",
            ]
DB = load_json(used_json)

def subpower_list(show : bool = False):
    temp_char = {}
    for char in DB["json_character"]:
        temp_main = []
        temp_sub = []
        if char.startswith("char") and DB["json_character"][char]["subPower"]:
            temp_main = [power for power in list(DB["json_character"][char]["mainPower"].values()) if power]
            for sub_power in DB["json_character"][char]["subPower"]:
                for power in sub_power.values():
                    if power: temp_sub.append(power)
            temp_char[char] = {"main" : temp_main, "sub" : list(set(temp_sub))}
    return temp_char

def power_name(power : str) -> str:
    return DB["json_handbook_teamEN"][power]["powerName"] if power in DB["json_handbook_teamEN"].keys() else DB["json_handbook_team"][power]["powerCode"]

def char_subpower():
    temp_char = {}
    subpower_json = subpower_list()
    for char in subpower_json.keys():
        char_name = DB["json_characterEN"][char]["name"] if char in DB["json_characterEN"].keys() else DB["json_character"][char]["appellation"]
        char_main = ", ".join([power_name(power) for power in subpower_json[char]["main"]])
        char_sub = ", ".join([power_name(power) for power in subpower_json[char]["sub"]])
        temp_char[char_name] = {"Main Power" : char_main, "Sub Power" : char_sub}
    return {char:temp_char[char] for char in sorted(temp_char.keys())}

def event_sypnosis(show : bool = False):
    events = {}
    SStag = DB["json_stage"]["storylineTags"]
    tags_en = DB["json_stageEN"]["storylineTags"] if "storylineTags" in DB["json_stageEN"].keys() else {}
    SStag.update(tags_en)
    tags = {tag:SStag[tag]["tagDesc"] for tag in SStag}
    
    SSset = DB["json_stage"]["storylineStorySets"]
    SSset_en = DB["json_stageEN"]["storylineStorySets"] if "storylineStorySets" in DB["json_stageEN"].keys() else {}
    SSset.update(SSset_en)

    for event in SSset:
        
        if SSset[event]["ssData"]:
            events[" ".join(SSset[event]["ssData"]["backgroundId"].split("_")[1:]).capitalize()] = {"desc" : SSset[event]["ssData"]["desc"], "retro" : SSset[event]["ssData"]["retroActivityId"], "tag" : ", ".join([tags[tag] for tag in SSset[event]["ssData"]["tags"]])}
        elif SSset[event]["collectData"]:
            events[" ".join(SSset[event]["collectData"]["backgroundId"].split("_")[1:]).capitalize()] = {"desc" : SSset[event]["collectData"]["desc"], "retro" : None}
        
    return events

def menu():
    def menu_gen(mode : dict) -> str:
        temp_menu = []
        for key in mode.keys():
            temp_menu.append(f'\t{R}{key} {RE}: {G if int(key) % 2 == 1 else B}{mode[key]}')
        return "\n".join(temp_menu)
    
    mode = {
                "1" : "Operator Subpower",
                "2" : "Event Sypnosis",
            }
    interface = [
                    f'\n{Y}What script do you want ?',
                    menu_gen(mode),
                    f'{Y}Select{RE} : '
    ]
    user_input = input("\n".join(interface))
    if user_input in mode.keys():
        print(f'\n{"#"*30}\n{G if int(user_input) % 2 == 1 else B}{mode[user_input]}{RE} is {Y}Selected{RE}\n{"#"*30}')
        return user_input
    print(f'\n{"#"*30}\n{R}{user_input}{RE} is {R}Invalid !!!{RE}\n{"#"*30}')

if __name__ == "__main__":
    while True:
        selected = menu()
        if selected: break
    
    match selected:
        case "1":
            script_result(char_subpower(), True, forced_txt = True)
        case "2":
            script_result(event_sypnosis(), True, forced_txt = True)
        case _:
            printr(f'{R}How did you come here !!!{RE} : {Y}{selected}{RE}')