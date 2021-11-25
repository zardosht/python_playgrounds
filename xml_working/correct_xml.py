import os
import pathlib
import xml.etree.ElementTree as ET



path_to_xmls = "./images_03_part1_copy"

paths = pathlib.Path(path_to_images).glob("*.xml")

for path_str in paths:
    tree = ET.parse('country_data.xml')
    root = tree.getroot()
    filename = root.findall("filename")