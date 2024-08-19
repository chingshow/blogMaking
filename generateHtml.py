# -*- coding: utf-8 -*-
import os
from dominate.tags import *
import dominate
import json
import sys
import markdown
import codecs
from dominate.util import raw
from bs4 import BeautifulSoup

def main(inputFile1, inputFile2, exist, path, new_data):
    # --------generate html from txt----------------#
    # html init
    newHtml = dominate.document()
    newHtml.add(link(rel="stylesheet", href="./styles2.css"))
    newHtml.add(meta(charset="utf-8"))
    title = newHtml.add(div(id="title", className="container"))
    content = newHtml.add(div(id="content", className="container"))

    filepath = os.path.join(f'./{path}/documents/txt/', inputFile1)
    print(filepath)
    #print(filepath)
    # read txt
    f = open(filepath, encoding="utf-8")
    length = 0
    for line in f.readlines():
        if line[0] != ' ' and line[0] != '\n':
            if length == 0:
                num = line
                no = []
                for char in num:
                    if char != '\n':
                        no.append(char)
                no = ''.join(str(x) for x in no)
            elif length == 1:
                title.add(p(line, id="date"))
            elif length == 2:
                title_name = []
                for char in line:
                    if char != '\n':
                        title_name.append(char)
                title_name = ''.join(str(x) for x in title_name)
                title.add(h1(title_name, id="title_name"))
                newHtml.title = title_name
            elif length == 3:
                auther = []
                for char in line:
                    if char != '\n':
                        auther.append(char)
                auther = ''.join(str(x) for x in auther)
                title.add(h2(auther, id="auther"))
            else:
                if(line[0] == '*'):
                    content.add(h3(line[1:]))
                else:
                    content.add(p(line))
            length += 1
    f.close()

    filepath = os.path.join(f'./{path}/documents/txt/', inputFile2)
    print(path, inputFile2)
    print(filepath)
    #input_file = codecs.open(filepath, 'r', encoding="utf-8")
    input_file = open(filepath, encoding="utf-8")
    text = input_file.read()
    #print("Markdown content:", text)
    html_content = markdown.markdown(text)
    #print("HTML content:", html_content)

    soup = BeautifulSoup(html_content, 'html.parser')

    print("Soup contents:", soup.contents)

    for element in soup.contents:
        print("Processing element:", element)
        if element.name:
            content.add(getattr(dominate.tags, element.name)(raw(str(element))))
        else:
            content.add(raw(str(element)))

    print("Final content:", content.render())

    # document name
    filepath = f'./{path}/documents/' + str(new_data["no"]) + '.html'

    with open(filepath, 'w', encoding="utf-8") as f:
        f.write(newHtml.render())

    # --------finish generate html from txt----------------#
    if not exist:
        print(f"Adding new document: {no}")
        with open(f'./{path}/content.json', 'r', encoding="utf-8") as fJson:
            load_dict = json.load(fJson)

            documents = load_dict['documents']['items']
            if not any(doc['no'] == no for doc in documents):
                documents.append(new_data)

        with open(f'./{path}/content.json', 'w', encoding="utf-8") as fJson:
            json.dump(load_dict, fJson, ensure_ascii=False, indent=4)
    else:
        print(f"Document {no} already exists, skipping JSON update")

