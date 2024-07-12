import xml.etree.ElementTree as ET
import os

root = ET.parse("./docs/prueba.xml").getroot()
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

            # if atributo.find("llavePrimaria") is not None and atributo.find("autoincrementable") is not None:
            #     primarykey = atributo[1].text.lower()
            #     tieneMiddle = True
            #     code += f'{atributo[1].text.lower()}:' +\
            #         "{" + f'type:Schema.Types.ObjectId,default:null'
            # else:
        code += f'{atributo[1].text.lower()}:'+"{" + f'type:{tipoDato},'
        if atributo.find("nullable").text == "true":
            code += "required: true"
        code += "},\n"
    code += """});
    """

    if tieneMiddle:
        ...
        # code += f"""{entidad[0].text}Schema.pre('save',function (next)"""+"{\n"
        # code += f"""if(!this.{primarykey})"""+"{\n"+f"this.{primarykey}=this.id;"+"""\n
        #     next();}
        #     });"""

        # code += f"const {entidad[0].text}=mongoose.model('{entidad[0].text}',{
        #     entidad[0].text}Schema"
        # code += ");"
        code += autoIncrement
        code += f"const {entidad[0].text}=mongoose.model('{entidad[0].text}',{
            entidad[0].text}Schema"
        code += ");"
        code += """module.exports ="""+f'{entidad[0].text}'

    else:
        code += """module.exports ="""+f'{entidad[0].text}Schema;'

    os.makedirs("./backend/models", exist_ok=True)
    file_path = f'backend/models/{entidad[0].text.lower()}.model.js'
    with open(file_path, 'w') as file:
        file.write(code)
    code = ""
    tipoDato = ""
    middleware = ""
    tieneMiddle = False
    autoIncrement = ""
