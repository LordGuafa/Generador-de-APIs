import xml.etree.ElementTree as ET

def leer_xml(filename):
    return ET.parse(f"schemas/{filename}").getroot()
