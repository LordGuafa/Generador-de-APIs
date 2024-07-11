import xml.etree.ElementTree as ET
import os

root = ET.parse("./docs/prueba.xml").getroot()
nombre_db = root.find("Nombre")
entidades = root.findall("Entidad")
code = """
const express = require("express");
const mongoose = require("mongoose");
\n"""
for entidad in entidades:
    code += f"""const {entidad[0].text.lower()
                       }=require('./controllers/{entidad[0].text.lower()}.controller.js')\n"""
code += """
// Crear una instancia de Express
const app = express();
app.use(express.json());
mongoose.connect(
  "mongodb+srv://Admin:hola1234@cluster0.jefznfs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" // Cambiar por la url de la base de datos
);
"""
for entidad in entidades:
    code += f'//Endpoints para {entidad[0].text}\n'
    atributos = entidad.findall("Atributo")
    for i, atributo in enumerate(atributos):
        if atributo.find("llavePrimaria") is not None:
            primarykey = atributo[1].text.lower()

    code += f"""app.post("/{entidad[0].text}",{
        entidad[0].text.lower()}.create);\n"""
    code += f"""app.get("/{entidad[0].text}",{
        entidad[0].text.lower()}.getAll);\n"""
    code += f"""app.get("/{entidad[0].text}/*",{
        entidad[0].text.lower()}.noExist);\n"""
    code += f"""app.get("/{entidad[0].text}/:{primarykey}",{
        entidad[0].text.lower()}.get);\n"""
    code += f"""app.put("/{entidad[0].text}/:{primarykey}",{
        entidad[0].text.lower()}.update);\n"""
    code += f"""app.delete("/{entidad[0].text}/:{primarykey}",{
        entidad[0].text.lower()}.delete);\n"""

    code += "//---------------------------------------------------------------------\n"
code += """
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

"""
os.makedirs("./backend", exist_ok=True)
file_path = 'backend/Api.js'
with open(file_path, 'w') as file:
    file.write(code)
