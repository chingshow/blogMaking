import json
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_sitemap(json_file_path, output_file_path):
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create the root element
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation',
               'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')

    # Add comment
    comment = ET.Comment(' created with Free Online Sitemap Generator www.xml-sitemaps.com ')
    urlset.append(comment)

    # Add the homepage
    home_url = ET.SubElement(urlset, 'url')
    ET.SubElement(home_url, 'loc').text = 'https://breastcancer.tech/'
    ET.SubElement(home_url, 'lastmod').text = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    ET.SubElement(home_url, 'priority').text = '1.00'

    # Add other pages (you may need to adjust this part based on your JSON structure)
    pages = [
        ('https://breastcancer.tech/intro.html', '0.80'),
        ('https://breastcancer.tech/index.html', '0.64')
    ]
    # Add articles
    for article in data['documents']['items']:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = f"https://breastcancer.tech/documents/{article['no']}.html"
        ET.SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        ET.SubElement(url, 'priority').text = '0.8'

    # Create a formatted XML string
    xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="")

    # Remove extra newlines
    xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])

    # Write to file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(xml_str)

    print(f"Sitemap generated successfully: {output_file_path}")


# Usage
json_file_path = 'content.json'  # Path to your JSON file
output_file_path = 'sitemap.xml'  # Path where you want to save the sitemap
generate_sitemap(json_file_path, output_file_path)