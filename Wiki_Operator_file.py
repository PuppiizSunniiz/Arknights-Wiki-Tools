from typing import Literal
from pyFunction import B, R, RE, Y, printr, script_result
from pyFunction_Wiki import load_json, wiki_cleanup, wiki_story

used_json = [
                "json_handbook_info",
                "json_handbook_infoEN",
            ]
DB = load_json(used_json)

def wiki_operator_file(operator_list : list[str] | str, server : Literal["CN", "EN"] = "EN"):
    if isinstance(operator_list, str):
        operator_list = [operator_list]
        
    article_writer = []
    handbook_info_json = DB["json_handbook_infoEN"] if server == "EN" else DB["json_handbook_info"]
    for operator_id in operator_list:
        if operator_id not in handbook_info_json["handbookDict"]:
            printr(f'{Y}{operator_id} {R}not{RE} in {B}{server}{RE} server')
            continue
        article_writer.append(f'{operator_id}\n{{{{Operator tab}}}}')
        for storyTextAudio in handbook_info_json["handbookDict"][operator_id]["storyTextAudio"]:
            if storyTextAudio["storyTitle"] in ["Basic Info", "Physical Exam"]:
                continue
            else:
                article_writer.append(f'{{{{Archive\n|title = {storyTextAudio["storyTitle"]}\n|text = {wiki_story(storyTextAudio["stories"][0]["storyText"])}}}}}')
    if article_writer:
        script_result("\n".join(article_writer), True)

OP_FILE_LIST = "char_197_poca"

wiki_operator_file(operator_list = OP_FILE_LIST)