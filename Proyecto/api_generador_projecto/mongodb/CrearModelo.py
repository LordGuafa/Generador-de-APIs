import xml.etree.ElementTree as ET
import os


def crearModeloMongo(root, project_dir):
    nombre_db = root.find("Nombre")
    entidades = root.findall("Entidad")
    autoIncrement = ""
    for entidad in entidades:
        atributos = entidad.findall("Atributo")
        code = """mongoose=require("mongoose");
        const AutoIncrement = require("mongoose-sequence")(mongoose);

        const  """+f'{entidad[0].text}Schema=new mongoose.Schema('+"{\n"
        for i, atributo in enumerate(atributos):

            if atributo[0].text == "INT":
                tipoDato = "Number"
            elif atributo[0].text == "BOOLEAN":
                tipoDato = "Boolean"
            elif atributo[0].text == "OBJECT":
                tipoDato = "Object"
            else:
                tipoDato = "String"
            if atributo.find("autoincrementable") is not None:
                tieneMiddle = True
                autoIncrement += f"""{entidad[0].text}Schema.plugin(AutoIncrement,"""+"{inc_field:"+f"""'{
                    atributo[1].text}'""" + "});\n"

            code += f'{atributo[1].text.lower()}:'+"{" + f'type:{tipoDato},'
            if atributo.find("nullable").text == "true":
                code += "required: true"
            code += "},\n"
        code += """});
        """

        if tieneMiddle:

            code += autoIncrement
            code += f"""const {entidad[0].text}=mongoose.model('{entidad[0].text}',{
                entidad[0].text}Schema"""
            code += ");"
            code += """module.exports ="""+f'{entidad[0].text}'

        else:
            code += """module.exports ="""+f'{entidad[0].text}Schema;'

        os.makedirs(project_dir+"/backend/models", exist_ok=True)
        file_path = project_dir + \
            f'/backend/models/{entidad[0].text.lower()}.model.js'
        with open(file_path, 'w') as file:
            file.write(code)
        code = ""
        tipoDato = ""
        middleware = ""
        tieneMiddle = False
        autoIncrement = ""
