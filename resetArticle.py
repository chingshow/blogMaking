# -*- coding: utf-8 -*-
import os
import json
import glob


#with open('content.json', 'r', encoding="utf-8") as fJson:
 #   load_dict = json.load(fJson)

#load_dict['documents']['items'] = []

#with open('content.json', 'w', encoding="utf-8") as fJson:
 #   json.dump(load_dict, fJson, ensure_ascii=False, indent=4)

def main(site: str):
    all_text = glob.glob(f'./{site}/documents/*.html')
    for t in all_text:
        os.remove(t)

    all_text = glob.glob(f'./{site}/documents/txt/*.txt')
    for t in all_text:
        os.remove(t)

    all_text = glob.glob(f'./{site}/documents/txt/*.md')
    for t in all_text:
        os.remove(t)


if __name__ == '__main__':
    main("Free Cancer")
