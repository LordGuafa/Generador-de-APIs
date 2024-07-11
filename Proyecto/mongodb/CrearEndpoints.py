import xml.etree.ElementTree as ET
import os

root = ET.parse("./docs/prueba.xml").getroot()
nombre_db = root.find("Nombre")
entidades = root.findall("Entidad")
code = ""
interrogantes = ""
listaAtributos = ""
arrayAtributos = []
for entidad in entidades:
    modelo = entidad[0].text.lower()
    atributos = entidad.findall("Atributo")
    for i, atributo in enumerate(atributos):
        if atributo.find("llavePrimaria") is not None:
            primarykey = atributo[1].text.lower()
        if atributo.find("autoincrementable") is not None:
            listaAtributos += ""
            interrogantes += ""
        else:

            listaAtributos += atributo[1].text.lower()
            arrayAtributos.append(atributo[1].text.lower())
            interrogantes += "?"
            if i < len(atributos)-1:
                listaAtributos += ", "
                interrogantes += ", "
    code += f"""
const{modelo}=require(".models/{modelo}.model")
const {entidad[0].text}=
"""+'{\n'
    code += "get: async(req,res)=>{\n "
    code += "const{"
    code += f"{primarykey}"+"}=req.params;"
    code += f"const temp= await {modelo}.findOne("+"{"
    code += f"{primarykey}"+"});"
    code += """res.status(200).send(temp);
    },"""
    code += """getAll: async(req,res)=>{"""
    code += f"""const temp= await{modelo}.find();
    res.status(200).send(temp);
    """+"},"
    code += """noExist: async(req,res)=>{
        res.status(404).send("No existe")
        },
        """
    code += "create: async(req,res)=>{"
    code += f"""const temp= new{modelo}(req.body);
    const saved= await temp.save();
    res.status(201).send(saved._id);
    """+"},"
    code += """update: async(req,res)=>{
        const{"""
    code += f"{primarykey}"+"}=req.params;\n"
    code += f"""const temp = await {modelo}
        .findOne("""+"{"+f"{primarykey}"+"});\n"
    code += """Object.assing(temp,req.body);
    await user.save();
    res.status(204);
    """+"},"
    code += """destroy: async (req,res)=>{
        const{"""
    code += f"{primarykey}"+"}=req.params;\n"
    code += f"""const temp = await {modelo}
        .findOne("""+"{"+f"{primarykey}"+"});\n"
    code += """if(temp){
        await """+f'{modelo}.deleteOne('+'{'+f'{primarykey}'+'});}\n}\n}\n'
    code += f'module.exports={entidad[0].text};'

    os.makedirs("./backend/controllers", exist_ok=True)
    file_path = f'backend/controllers/{entidad[0].text}.controller.js'
    with open(file_path, 'w') as file:
        file.write(code)
    code = ""
    listaAtributos = ""
    arrayAtributos.clear()
    interrogantes = ""
print(arrayAtributos)
# app.put("/Clientes/:cod_cliente", clientes.update)
# app.delete("/Clientes/:cod_cliente", clientes.delete);
