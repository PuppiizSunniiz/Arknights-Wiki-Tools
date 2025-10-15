import re
from typing import Literal
from pyFunction import B, G, R, RE, Y, json_load, printr, script_result, txt_load
from pyFunction_Wiki import load_json, replace_apos_between, wiki_story


used_json = [
                "json_story_reviewEN",
            ]

DB = load_json(used_json)

def get_story_json(story_key : str, stage_key : Literal["storyCode", "storyName"]):
    story_json = []
    for actvity in DB["json_story_reviewEN"]:
        infoUnlockDatas = DB["json_story_reviewEN"][actvity]["infoUnlockDatas"]
        if infoUnlockDatas:
            for story in infoUnlockDatas:
                if story[stage_key] == story_key:
                    story_json.append((story.get("storyInfo", ""), story["storyTxt"]))
    if story_json:
        return story_json
    else:
        printr(f'{Y}Story not found')
        exit()

def get_story(stage_code : str = "", stage_name : str = ""):
    if stage_code:
        return get_story_json(stage_code, "storyCode")
    elif stage_name:
        return get_story_json(stage_name, "storyName")
    else:
        printr(f'{R}HOW DID YOU GET HERE')
        exit()
        
    
def story_head(story_file : str):
    head_json = txt_load(fr'json\gamedata\ArknightsGameData_YoStar\en_US\gamedata\story\[uc]{story_file}.txt')
    return f'{{{{Story head|{wiki_story(head_json, clean_all = all_clean)}}}}}'.replace("<br/>}}", "}}")

def story_cell(story_file : str):
    def end_cell(prev_name : str, cell_list : list, prev_dialogue : str):
        if not prev_dialogue:
            return cell_list, ""
        
        if prev_dialogue.endswith("<br/>"):
            prev_dialogue = prev_dialogue[:-5]
        
        if prev_name == "[Subtitle]":
            prev_dialogue += "|mode=subtitle}}"
        elif prev_name == "[Speech]":
            prev_dialogue += "|mode=speech}}"
        else:
            prev_dialogue += "}}"
        cell_list.append(prev_dialogue.replace("<br/><br/>", "<br/>"))
        #printr(curr_dialogue)
        return cell_list, ""
    
    def transcript_cell(cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue):
        # Start New conversation
        if curr_name != prev_name:
            if prev_dialogue:
                cell_list, prev_dialogue = end_cell(prev_name, cell_list, prev_dialogue)
            prev_name = curr_name
            prev_dialogue = curr_dialogue
        # Mid conversation
        elif curr_name == prev_name:
            prev_dialogue += f'<br/>{curr_line}'
        printr(prev_dialogue)
        return cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue

    cell_list       : list[str] = []
    doctor_decision : list[str] = []
    doctor_predicate            = ""
    prev_predicate              = ""
    prev_name                   = ""
    prev_dialogue               = ""
    
    cut_list = ("[Image(", "[Background(", "[playsound(", "[ImageTween", "[PlaySound")
    skip_list = ("[HEADER", "[charslot", "[Blocker", "[delay", "[Delay", "[stopmusic]", "[Dialog]", "[subtitle]", "[PlayMusic", "[stopmusic", "[CameraShake(", "[stopSound", "[Image]", "[playMusic")
    cell_json = txt_load(fr'json\gamedata\ArknightsGameData_YoStar\en_US\gamedata\story\{story_file}.txt')
    
    for line in cell_json:
        if line.startswith(("[name=", "[multiline(name=", "[Subtitle(text=")):
            DIALOUGE = line.startswith(("[name=", "[multiline(name=")) # Dialouge / Subtitle
            dialogue_match = re.match(r'^.+?name="(.+?)"\)?](?:\s*|)(.+?)$', line)
            curr_name = replace_apos_between(dialogue_match.group(1)) if DIALOUGE else "[Subtitle]"
            curr_line = wiki_story(dialogue_match.group(2), clean_all = all_clean) if DIALOUGE else wiki_story(re.match(r'^\[Subtitle\(text="(.+?)",.+?$', line).group(1))
            curr_dialogue = f'{{{{sc|{curr_name}|{curr_line}' if DIALOUGE else f'{{{{sc|{curr_line}'
            cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue = transcript_cell(cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue)
        elif not line.startswith("["):
            curr_name = "[Speech]"
            curr_line = wiki_story(line, clean_all = all_clean)
            curr_dialogue = f'{{{{sc|{curr_line}'
                
            cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue = transcript_cell(cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue)
        elif line.startswith(("[Decision(options=", "[Predicate(")):
            if line.startswith("[Decision(options="):
                if prev_name != "Doctor" : cell_list, prev_dialogue = end_cell(prev_name, cell_list, prev_dialogue)
                line_match  = re.match(r'\[Decision\(options="(.+?)", ?values="(.+?)"\)]', line)
                doctor_decision = line_match.group(1).split(";")
                doctor_predicate = line_match.group(2)
            elif line.startswith("[Predicate("):
                curr_predicate  = re.match(r'\[Predicate\(references="(.+?)"\)\]', line).group(1)
                if curr_predicate != doctor_predicate:
                    curr_name = "Doctor"
                    curr_index = doctor_predicate.split(";").index(curr_predicate)
                    curr_line = wiki_story(doctor_decision[curr_index], clean_all = all_clean)
                    curr_dialogue = f'{{{{sc|{curr_name}|{curr_line}'
                    cell_list, prev_dialogue = end_cell(prev_name, cell_list, prev_dialogue)
                    if curr_index == 0:
                        cell_list.append("{{sc|mode=branchstart}}")
                    else:
                        cell_list.append("{{sc|mode=branch}}")
                    
                    cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue = transcript_cell(cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue)
                    prev_predicate = curr_predicate
                # ex. [Predicate(references="1;2")]
                elif curr_predicate == doctor_predicate and curr_predicate != doctor_predicate.split(";")[0]:
                    if prev_predicate:
                        cell_list, prev_dialogue = end_cell(prev_name, cell_list, prev_dialogue)
                        cell_list.append("{{sc|mode=branchend}}")
                        doctor_decision = []
                        doctor_predicate = ""
                        prev_predicate = ""
                    else:
                        curr_name = "Doctor"
                        curr_line = wiki_story((" / ").join(doctor_decision), clean_all = all_clean)
                        curr_dialogue = f'{{{{sc|{curr_name}|{curr_line}'
                        
                        cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue = transcript_cell(cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue)
                        doctor_decision = []
                        doctor_predicate = ""
                        prev_predicate = ""
                # ex. [Predicate(references="1")]
                else:
                    curr_name = "Doctor"
                    curr_line = wiki_story(doctor_decision[0], clean_all = all_clean)
                    curr_dialogue = f'{{{{sc|{curr_name}|{curr_line}'
                        
                    cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue = transcript_cell(cell_list, prev_name, prev_dialogue, curr_name, curr_line, curr_dialogue)
                    doctor_decision = []
                    doctor_predicate = ""
                    prev_predicate = ""
                    
        elif line.startswith(cut_list):
            if skip_cut:
                continue
            elif line.startswith(("[playsound(", "[PlaySound")):
                if cell_list[-1].endswith("|mode=action}}") and not prev_dialogue: continue
                cell_list, prev_dialogue = end_cell(prev_name, cell_list, prev_dialogue)
                cell_list.append(f'{{{{sc||mode=action}}}}')
                prev_name = ""
            else:
                cell_list, prev_dialogue = end_cell(prev_name, cell_list, prev_dialogue)
                cell_list.append(f'{{{{sc||mode={line.split("(", 1)[0][1:].lower()}}}}}')
                prev_name = ""
        elif line.startswith(skip_list):
            continue
        else:
            cell_list.append(f'Test case : {line.replace("\n", "")}')
    cell_list, prev_dialogue = end_cell(prev_name, cell_list, prev_dialogue)
    return "\n".join(cell_list)

def wiki_story_transcript(stage_code : str = "", stage_name : str = ""):
    story_files = []
    story_article = []
    if bool(stage_code) + bool(stage_name) != 1 :
        printr(f'Choose {R}one{RE} BAKA !!! :\n{G}Stage ID : {stage_code}\n{B}Stage name : {stage_name}')
        exit()
    else:
        story_files = get_story(stage_code, stage_name)
        for story_file in story_files:
            if story_file[0]:
                story_article.append(story_head(story_file[0]))
            story_article.append(story_cell(story_file[1]))
            story_article.append("{{Table end}}")
    script_result(story_article, True)

stage_code  = "EA-ST-3"
stage_name  = ""
skip_cut    = False # True False
all_clean   = False # True False
wiki_story_transcript(stage_code, stage_name)