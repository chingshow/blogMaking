# -*- coding: utf-8 -*-
import os
import json
import generateHtml


def main(path):
    with open(f'./{path}/content.json', 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)

    documents = load_dict['articles']
    folder_path = f'./{path}/documents/txt/'

    documentLocal = []
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            documentLocal.append(file)
            #print(file)

    exist = 0
    for document in documentLocal:
        # print("document:", document)
        exist = 0
        for item in documents:
            # print(str(item['no']) + ".txt")
            if str(item['no']) + ".txt" == document:
                exist = 1
                break
        # 發現不存在這個文章 --> 開始產生html
        generateHtml.main(document, exist, path)

    # --- sort json --- #

    with open(f'./{path}/content.json', 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)

        documents = load_dict['articles']
        for i in range(len(documents)-1, -1, -1):
            for j in range(i-1, -1, -1):
                if documents[i]['no'] > documents[j]['no']:
                    temp = documents[i]
                    documents[i] = documents[j]
                    documents[j] = temp

    with open(f'./{path}/content.json', 'w', encoding="utf-8") as fJson:
        json.dump(load_dict, fJson, ensure_ascii=False, indent=4)




