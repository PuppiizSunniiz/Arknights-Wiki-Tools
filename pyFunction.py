from datetime import datetime
import json
import inspect
import os
import subprocess
from typing import Any, Callable, Literal, Self
import csv
import pandas as pd

R = '\033[31m'
G = '\033[32m'
Y = '\033[33m'
B = '\033[34m'
RE = '\033[0m'

CN_PATH = r'json/gamedata/ArknightsGameData/zh_CN/gamedata/'
EN_PATH = r'json/gamedata/ArknightsGameData_YoStar/en_US/gamedata/'
JP_PATH = r'json/gamedata/ArknightsGameData_YoStar/ja_JP/gamedata/'
KR_PATH = r'json/gamedata/ArknightsGameData_YoStar/ko_KR/gamedata/'

def printr(*arg):
    print(f'{R}[:{inspect.currentframe().f_back.f_lineno:<4}]{RE}', *arg, RE)

def printc(*arg):
    all_arg = [*arg]
    print(f'{R}[:{inspect.currentframe().f_back.f_lineno:<4}]{RE}', " ".join([f'{G}{all_arg[i]}' if i % 2 == 1 else f'{B}{all_arg[i]}' for i in range(len(all_arg))]), RE) # type: ignore

def printf(*arg, file = "",  mode = ""):
    print(f'{Y}>> Printf From{RE} : [{R}{file}:{inspect.currentframe().f_back.f_lineno}{RE}]\n')
    if mode == "c":
        all_arg = [*arg]
        print(" ".join([f'{G}{all_arg[i]}' if i % 2 == 1 else f'{B}{all_arg[i]}' for i in range(len(all_arg))]), RE)
        print(f'{Y}>> Printf END{RE}')
    else:
        print(*arg)
        print(f'\n{Y}>> Printf END{RE}')

def json_load(filepath : str, internal : bool = False, default_json : dict|list = {}):
    if internal:
        try :
            with open(f'{filepath}', 'r', encoding = 'utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            printr(f'{G}FileNotFoundError {RE}: {Y}{filepath} {RE}(Default : {B}{default_json})')
            return default_json
    else:
        with open(f'C:/Github/AN-EN-Tags/{filepath}', 'r', encoding = 'utf-8') as file:
            return json.load(file)

def txt_load(filepath : str, temp = False):
    if temp:
        with open(f'{filepath}', 'r', encoding = 'utf-8') as file:
            return file.readlines()
    else:
        with open(f'C:/Github/AN-EN-Tags/{filepath}', 'r', encoding = 'utf-8') as file:
            return file.readlines()

def epoch(time) -> str :
    return f'{TimeFormat(datetime.fromtimestamp(time))} is {time_diff(datetime.fromtimestamp(time))}'

def time_to_str(self) -> str :  # return Date as Y M D H M or S
    if self.days > 365 :
        return str(self.days // 365) + ' Year(s)'
    elif self.days > 31 :
        return str(self.days // 30) + ' Month(s)'
    elif self.days > 0 :
        return str(self.days) + ' Day(s)'
    elif self.seconds > 3600 :
        return str(self.seconds // 3600) + ' Hour(s)'
    elif self.seconds > 60 :
        return str(self.seconds // 60) + ' Minute(s)'
    else :
        return str(self.seconds) + ' Second(s)'

def time_diff(self) -> str :  # Time different Before(ago) or After(in)
    if self < datetime.now() :
        return time_to_str(datetime.now() - self) + ' ago'
    else :
        return 'in ' + time_to_str(self - datetime.now())

def TimeFormat(self) -> str :
    return self.strftime('%d %b %Y %H:%M:%S')

def char_ready(char_json : dict , mode : int = 0) -> dict:
    '''
        Get character_table -> Return Code2Name Name2Code dict
        
        Mode 1 : ["Code2Name"]
        Mode 2 : ["Name2Code"]
        Mode 3 : ["Exclude"]
        Default : All
    '''

    Chars : dict[str, Any] = {"Code2Name":{}, "Name2Code":{}}
    for char_key in char_json.keys() :
        if "char_" in char_key :
            Chars["Code2Name"][char_key] = get_char_name(char_json,char_key)
            Chars["Name2Code"][get_char_name(char_json,char_key)] = char_key
    Chars["Exclude"] = [[char_key, get_char_name(char_json, char_key)] for char_key in char_json.keys() if "char_" in char_key and char_json[char_key]["isNotObtainable"]]
    match mode :
        case 1 :
            return Chars["Code2Name"]
        case 2 :
            return Chars["Name2Code"]
        case 3 :
            return Chars["Exclude"] # type: ignore
        case _ :
            return Chars

def get_char_name(char_json : dict[str, dict[str, Any]], char_key : str) -> str :
    return name_check(char_json[char_key]["appellation"])

def name_check(appellation : str) -> str :
    Russian : dict = {
                        'Гум'       : 'Gummy',
                        'Зима'      : 'Zima',
                        'Истина'    : 'Istina',
                        'Позёмка'   : 'Pozëmka',
                        'Роса'      : 'Rosa',
                        'Лето'      : 'Leto'
                    }
    return Russian.get(appellation, appellation)

def print_header(text : str) -> str:
    length : int = 20
    return f'\n{"#" * length * 3}\n{"#" * length}{text:^{length}}{"#" * length}\n{"#" * length * 3}'

def script_result(text : str | list | set | dict ,
                    show : bool = False,
                    indent : int | None = 4,
                    key_sort : bool = False,
                    sort_keys : Callable = lambda x: x,
                    forced_txt : bool = False,
                    txt_nokey : bool = False,
                    no_tab : bool = False,
                    script_exit : bool = False
                    ) -> None:
    '''
        Output result
            STR, LIST, SET  >   TXT
            DICT            >   JSON
    '''
    def dict_to_txt(text : dict, tab : int = 0) -> str:
        to_txt = []
        keys = sorted(text.keys(), key = sort_keys) if key_sort else text.keys()
        for key in keys:
            if isinstance(text[key], dict):
                to_txt.append(f'{"" if tab else "\n"}{"\t" * tab}{key}')
                to_txt += dict_to_txt(text[key], 0 if no_tab else tab + 1)
            else:
                value_text = (f'\n{text[key]}').replace("\n", f'\n{"\t" * (tab + (len(key) + 3) // 4 + 1)}') if text[key] and "\n" in str(text[key]) else text[key]
                to_txt += [f'{"\t" * tab}{value_text}'] if txt_nokey else [f'{"\t" * tab}{key} : {value_text}']
        return to_txt
    
    if not text:
        print(f'\n{Y}Script Result is {R}Empty')
        exit()
    
    if isinstance(text, str):
        with open("py/script.txt", "w", encoding = "utf-8") as filepath:
            filepath.write(text.replace(" ", " "))
    elif isinstance(text, list) or isinstance(text, set):
        with open("py/script.txt", "w", encoding = "utf-8") as filepath:
            filepath.write("\n".join(text).replace(" ", " "))
    elif isinstance(text, dict) and indent:
        if forced_txt:
            with open("py/script.txt", "w", encoding = "utf-8") as filepath:
                filepath.write("\n".join(dict_to_txt(text)).replace(" ", " "))
        else :
            with open("py/script.json", "w", encoding = "utf-8") as filepath:
                json.dump(text, filepath, indent = indent, ensure_ascii = False, sort_keys = key_sort)
    else:
        with open("py/script.json", "w", encoding = "utf-8") as filepath:
            json.dump(text, filepath, separators = (",", ":"), ensure_ascii = False, sort_keys = key_sort)
    
    file = f'py/script.{"json" if isinstance(text, dict) and not forced_txt else "txt"}'
    print(f'\n{Y}Script Completed{RE} -> {R}{file}{RE}')
    if show:
        subprocess.run(f'code --reuse-window -g "{os.path.abspath(file)}"', shell = True)
    if script_exit:
        exit()

def join_and(text_list : list | set) -> str :
    return_text = " and ".join(text_list)
    if len(text_list) >= 3:
        return_text = return_text.replace(" and ", ", ", len(text_list) - 2)
    return return_text

def join_or(text_list : list | set) -> str :
    return_text = " or ".join(text_list)
    if len(text_list) >= 3:
        return_text = return_text.replace(" or ", ", ", len(text_list) - 2)
    return return_text

def falsy_compare(a, b) -> bool:
    return not bool(a) and not bool(b) or a == b

def decimal_format(dec : float|str) -> str:
    if isinstance(dec, str):
        dec = float(dec)
    
    if int(dec) != dec and len(str(dec).split(".")[-1]) > 1:
        return f'{dec:.2f}'
    elif int(dec) != dec and len(str(dec).split(".")[-1]) == 1:
        return f'{dec:.1f}'
    else:
        return f'{dec:.0f}'
    
def sorted_dict_key(curr_dict : dict, sorted_key : Callable = None, mode : Literal["dict", "keys"] = "dict"):
    key_sorted = sorted(list(curr_dict.keys()), key = sorted_key)
    match mode:
        case "dict":
            return {k:curr_dict[k] for k in key_sorted}
        case "keys":
            return key_sorted
        case _:
            print(f'Wrong {Y}sorted_dict_key{RE} mode : {R}{mode}')
            exit()
            
def blackboard_format(desc, format):
    match format:
        case "0":
            return f'{desc:g}'
        case "0%":
            return f'{desc*100:g}%'
        case _:
            print(f'New format for {Y}blackboard_format{RE} : {R}{format}')
            exit()
    return

def DictToCSV(
        data : dict, 
        dataset : Self, 
        main : str = "",
        separator : str = "|", 
        file_type : Literal["csv", "txt", "xlsx"] = "txt",
        sheet_name : str = "",
        use_keys : bool = False,
        keys : list[str] = [],
    ):
    
    keys : list[str|int|float]  = keys if keys else dataset.keys
    sheet_name : str            = sheet_name if sheet_name else dataset.classname
    file_type : str             = file_type
    
    match file_type:
        case "txt":
            csv_header = keys
            csv_result = [separator.join(csv_header)]
            for data_key in data:
                key_data : dict = data[data_key]
                if use_keys:
                    key_result  = [str(data_key), str(key_data)]
                else :
                    key_result  = [str(key_data.get(key, "")) or "" for key in keys]
                csv_result.append(separator.join(key_result))
            script_result(csv_result, True)
        case "csv":
            if use_keys:
                csv_data = [{keys[0]:k, keys[1]:v} for k,v in data.items()]
            else:
                csv_data = [value for value in data.values()]
            
            with open("py/script.csv", mode = "w", newline = "", encoding = "utf-8") as file:
                writer = csv.DictWriter(file, fieldnames = keys, delimiter = separator)
                writer.writeheader()
                writer.writerows(csv_data)
        case "xlsx":
            df = pd.DataFrame.from_dict(data, orient="index")
            try:
                with pd.ExcelWriter(f'output/{main}.xlsx', mode = "a", if_sheet_exists = "replace") as writer:
                    df.to_excel(writer, sheet_name = sheet_name, index = False)
            except FileNotFoundError:
                with pd.ExcelWriter(f'output/{main}.xlsx', mode = "w") as writer:
                    df.to_excel(writer, sheet_name = sheet_name, index = False)
        case _ :
            print(f'DictToCSV do not support this file type : {file_type}')