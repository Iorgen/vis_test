# Напишите функцию сравнения двух json-объектов (float поля должны сравниваться с
# точностью до 5 знаков).
# BMC for task 3 
# надо просто ответить одинаковые json'ы или нет. видимо в данных терминов - если полное совпадение, то true, если нет, то false
# TODO Add commentaries 
# TODO Insert to git 
# 
import json
import argparse
import os
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("JSON Сomparer:")

arguments_parser = argparse.ArgumentParser(prog="python task1.py", description="JSON comparator.")
arguments_parser.add_argument('-f', '--initial', default='first.json')
arguments_parser.add_argument('-s', '--comparable', default='second.json')

def _dict_comparisons(dict1: dict, dict2: dict):
    absolute_match = True
    in_keys = set(dict1.keys())
    co_keys = set(dict2.keys())

    all_keys = set([*in_keys, *co_keys])
    logger.info(f'All keys: {all_keys}')

    match_keys = in_keys.intersection(co_keys)
    match = {_key: None for _key in match_keys}
    
    for _key in all_keys:
        if _key not in match_keys:
            absolute_match = False

    for _key in match_keys: 
        if isinstance(dict1[_key], type(dict2[_key])) and isinstance(dict2[_key], type(dict1[_key])):
            
                if isinstance(dict1[_key], list): 
                    match[_key], absolute_match = _dict_comparisons(
                        {_idx: value for _idx, value in enumerate(dict1[_key])}, 
                        {_idx: value for _idx, value in enumerate(dict2[_key])} 
                    )
                
                elif isinstance(dict1[_key], dict): 
                    match[_key], absolute_match = _dict_comparisons(dict1=dict1[_key], dict2=dict2[_key])
                
                elif isinstance(dict1[_key], float): 
                    match[_key] = round(dict1[_key], 5) == round(dict2[_key], 5)
                    if not match[_key] : 
                        absolute_match = False 
                
                elif isinstance(dict1[_key], str): 
                    match[_key] = dict1[_key] == dict2[_key]
                    if not match[_key] : 
                        absolute_match = False 
                
                else: 
                    logger.warning(f'Not supported type')
                
        else:
            continue 
    return match, absolute_match


if __name__ == "__main__":
    
    arguments = arguments_parser.parse_args()
    with open(os.path.join('data', arguments.initial)) as initial_file:
        initial = json.load(initial_file)
        
    with open(os.path.join('data', arguments.comparable)) as comparable_file:
        comparable = json.load(comparable_file)
    
    match, absolute_match = _dict_comparisons(dict1=initial, dict2=comparable)
    logger.info(f'JSONs absoulte match status: {absolute_match}')
    logger.info(f'JSONs certain match status: {match}')
