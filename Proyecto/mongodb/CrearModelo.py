import xml.etree.ElementTree as ET
import os

root = ET.parse("./docs/prueba.xml").getroot()
nombre_db = root.find("Nombre")
entidades = root.findall("Entidad")
