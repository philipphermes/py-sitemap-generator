import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom
from datetime import datetime
from bs4 import BeautifulSoup

class Generate:
    _found_urls = []
    _url = ""
    _file_path = ""

    def __init__(self, url, file_path):
        self._url = url
        self._file_path = file_path

    def _scrape_and_search_urls(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            anchor_tags = soup.find_all('a', href=True)
            urls = [link['href'] for link in anchor_tags]

            for found_url in urls:
                if found_url in self._found_urls or self._url + found_url in self._found_urls:
                    continue

                if found_url.startswith('/') or found_url.startswith(self._url):
                    if found_url.startswith('/'):
                        found_url = self._url + found_url
                    
                    self._found_urls.append(found_url)
                    print("Searching: " + found_url)

                    self._scrape_and_search_urls(found_url)
        return self._found_urls
    
    def start(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        self._scrape_and_search_urls(self._url)

        rootXML = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        self._found_urls.sort()
        for url in self._found_urls:
            childXML_url = ET.SubElement(rootXML, "url")
            childXML_loc = ET.SubElement(childXML_url, "loc")
            childXML_loc.text = url
            childXML_mod = ET.SubElement(childXML_url, "lastmod")
            childXML_mod.text = current_date
            childXML_pri = ET.SubElement(childXML_url, "priority")
            childXML_pri.text = str(0.5) #TODO
        
        XMLstr = ET.tostring(rootXML, encoding='unicode')

        dom = xml.dom.minidom.parseString(XMLstr)
        pretty_xml_str = dom.toprettyxml(encoding="utf-8").decode('utf-8')

        with open(self._file_path, "w", encoding="utf-8") as file:
            file.write(pretty_xml_str)

generate = Generate("https://google.com", "path/to/sitemap.xml")
found_urls = generate.start()
