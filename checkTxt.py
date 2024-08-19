import os
import json
import generateHtml


def main(key, path, new_data):
    with open(f'./{path}/content.json', 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)

    documents = [str(article['no']) for article in load_dict['documents']['items']]

    folder_path = f'./{path}/documents/txt/'

    # 獲取所有 .txt 文件
    documentLocal = [file for file in os.listdir(folder_path) if file.endswith('.txt')]

    #for document in documentLocal:
        # 移除 .txt 擴展名並檢查是否在 documents 列表中
        #document_no = int(document.split(".")[0])


        #print(f"Document: {document}")
        #print(f"Document No: {document_no}")
        #print(f"Documents: {documents}")
        #print(f"Exist: {exist}")

    exist = key in documents
    print(exist)
    print(new_data)
    generateHtml.main(f"{key}.txt", f"{key}.md", exist, path, new_data)

    #print(f"Final exist value for {document}: {exist}")
    #print("------------------------")

    # 只有在有新文档时才更新和排序 JSON
    if any(doc.split(".")[0] not in documents for doc in documentLocal):
        # --- sort json --- #
        with open(f'./{path}/content.json', 'r', encoding="utf-8") as fJson:
            load_dict = json.load(fJson)

            documents = load_dict['documents']['items']
            documents.sort(key=lambda x: x['no'], reverse=True)

        with open(f'./{path}/content.json', 'w', encoding="utf-8") as fJson:
            json.dump(load_dict, fJson, ensure_ascii=False, indent=4)