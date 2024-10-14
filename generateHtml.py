import os
from dominate import document
from dominate.tags import *
from dominate.util import raw
import json
import markdown
from bs4 import BeautifulSoup


def mainf(inputFile1, inputFile2, exist, path, new_data):
    # HTML init
    newHtml = document(title="")

    with newHtml.head:
        meta(charset="utf-8")
        link(rel="stylesheet", href="../styles.css")
        link(rel="stylesheet", href="./styles2.css")

    # Add functions div
    with newHtml:
        with nav():
            with div(cls="functions"):
                a("首頁", href="../index.html", id="homePage")
                a("回到頂部", href="#", id="backToTop")

    # Add title div
    title_div = newHtml.add(div(id="title", cls="container"))

    # Add contents div
    contents_div = newHtml.add(div(id="contents"))

    with contents_div:
        div(id="stickyImageContainer")
        with main():
            div(id="ad3Container", hidden="")
            content_div = div(id="content")

    # Add sidebar and sticky image container
    with contents_div:
        with aside(id="sidebar"):
            with div(id="sidebarContent"):
                with section():
                    h3("日期歸檔")
                    ul(id="dateArchive")
                with section():
                    h3("標籤")
                    ul(id="tagList")
            div(id="stickyImageContainer2", hidden="")

    # Read and process inputFile1
    filepath = os.path.join(f'./{path}/documents/txt/', inputFile1)
    #filepath = os.path.join(f'.', inputFile1)
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()
        if i == 0:
            no = line
        elif i == 1:
            title_div.add(p(line, id="date"))
        elif i == 2:
            title_name = line
            title_div.add(h1(title_name, id="title_name"))
            newHtml.title = title_name
        elif i == 3:
            auther = line
            title_div.add(h2(auther, id="auther"))
        else:
            if line.startswith('*'):
                content_div.add(h3(line[1:]))
            else:
                content_div.add(p(line))

    # Process inputFile2
    filepath = os.path.join(f'./{path}/documents/txt/', inputFile2)
   # filepath = os.path.join(f'.', inputFile2)
    with open(filepath, encoding="utf-8") as input_file:
        text = input_file.read()

    html_content = markdown.markdown(text)
    soup = BeautifulSoup(html_content, 'html.parser')

    for element in soup.contents:
        if element.name:
            content_div.add(raw(str(element)))
        else:
            content_div.add(raw(str(element)))

    with newHtml:
        script(src="script_articles.js")
        script(src="https://d3js.org/d3.v6.min.js")
        script(src="https://cdnjs.cloudflare.com/ajax/libs/d3-cloud/1.2.5/d3.layout.cloud.min.js")

    # Write the HTML file
    filepath = f'./{path}/documents/{no}.html'
    #filepath = f'{no}.html'
    with open(filepath, 'w', encoding="utf-8") as f:
        f.write(newHtml.render())

    # Update JSON file
    json_path = f'./{path}/content.json'
    with open(json_path, 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)
        documents = load_dict['documents']['items']

        if not exist:
            if not any(doc['no'] == no for doc in documents):
                print(f"Adding new document: {no}")
                documents.append(new_data)
        else:
            for doc in documents:
                if doc['no'] == new_data['no']:
                    print(new_data)
                    doc.update(new_data)
                    break
            print(f"Document {no} already exists, skipping JSON update")

    with open(json_path, 'w', encoding="utf-8") as fJson:
        json.dump(load_dict, fJson, ensure_ascii=False, indent=4)



