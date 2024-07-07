import xml.etree.ElementTree as ET
import os

root = ET.parse("lector/prueba.xml").getroot()
nombre_db = root.find("Nombre")
entidades = root.findall("Entidad")
script = ""
for entidad in entidades:
    atributos = entidad.findall("Atributo")
    script += f"CREATE TABLE IF NOT EXISTS `{entidad[0].text}`(\n"
    for i, atributo in enumerate(atributos):
        script += f"\t`{atributo[1].text}` "
        if(atributo[0].text == "VARCHAR"):
            script += f"{atributo[0].text}(255)"
        else:
            script += f"{atributo[0].text}"
        if atributo.find("llavePrimaria") is not None:
            script += " PRIMARY KEY"
        elif atributo.find("nullable").text == "true":
            script += " NULL"
        else:
            script += " NOT NULL"
        if atributo.find("autoincrementable") is not None:
            script += " AUTO_INCREMENT"

        # Solo agregar la coma si no es el último atributo
        if i < len(atributos) - 1:
            script += ",\n"
        else:
            script += "\n"

    script += ");\n"

relaciones = root.find("Relaciones").findall("Relacion")
for relacion in relaciones:
    for entidad in entidades:
        if entidad[0].text == relacion.find("EntidadPrincipal").text:
            clase_padre = entidad
        elif entidad[0].text == relacion.find("EntidadDependiente").text:
            clase_hija = entidad
    script += f"ALTER TABLE `{clase_hija[0].text}`\n\tADD CONSTRAINT `FK_{clase_hija[0].text}_{clase_padre[0].text}`\n"
    for atributo in clase_padre.findall("Atributo"):
        if atributo.find("llavePrimaria") is not None:
            llave = atributo.find("nombre").text
            
    script += f" \t\tFOREIGN KEY (`{llave}`) REFERENCES `{clase_padre[0].text}` (`{llave}`) ON DELETE Restrict ON UPDATE Restrict"
    script += "\n;\n"

os.makedirs("./database", exist_ok=True)
file_path = 'database/script.sql'
with open(file_path, 'w') as file:
    file.write(script)