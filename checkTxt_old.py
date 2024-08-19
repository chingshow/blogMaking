# -*- coding: utf-8 -*-
import os
import json
import generateHtml


def main(path, new_data):
    with open(f'./{path}/content.json', 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)

    documents = [article['no'] for article in load_dict['documents']['items']]

    folder_path = f'./{path}/documents/txt/'

    # 獲取所有 .txt 文件
    documentLocal = [file for file in os.listdir(folder_path) if file.endswith('.txt')]

    for document in documentLocal:
        # 移除 .txt 擴展名並檢查是否在 documents 列表中
        document_no = document.split(".")[0]
        exist = 1 if document_no in documents else 0

        print(f"Document: {document}")
        print(f"Document No: {document_no}")
        print(f"Documents: {documents}")
        print(f"Exist: {exist}")

        generateHtml.main(document, exist, path, new_data)

        print(f"Final exist value for {document}: {exist}")
        print("------------------------")

    # --- sort json --- #

    with open(f'./{path}/content.json', 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)

        documents = load_dict['documents']['items']
        for i in range(len(documents)-1, -1, -1):
            for j in range(i-1, -1, -1):
                if documents[i]['no'] > documents[j]['no']:
                    temp = documents[i]
                    documents[i] = documents[j]
                    documents[j] = temp

    with open(f'./{path}/content.json', 'w', encoding="utf-8") as fJson:
        json.dump(load_dict, fJson, ensure_ascii=False, indent=4)


if "__main__" == __name__:
    main("Avater Medicine 2023")


