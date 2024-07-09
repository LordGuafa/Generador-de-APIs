import xml.etree.ElementTree as ET
import os

root = ET.parse("lector/prueba.xml").getroot()
nombre_db = root.find("Nombre")
aux = ""
entidades = root.findall("Entidad")
code = """
const express = require("express");
const mysql = require("mysql2");
const bodyParser = require("body-parser");
const fs = require("fs");\n"""
for entidad in entidades:
    code += f"""{entidad[0].text.lower()
                 }=require({entidad[0].text.lower()}.controller.js)\n"""
code += """const path = require("path");
// Crear una instancia de Express
const app = express();
app.use(express.json());
// Configurar la conexion a la base de datos MySQL
const connection = mysql.createConnection({
  host: "localhost", // Cambia esto a tu host de la base de datos
  user: "root", // Cambia esto a tu usuario de la base de datos
  password: "1234", // Cambia esto a tu contrasena de la base de datos
  database: "Prueba", // Cambia esto a tu base de datos
});

// Conectar a la base de datos
connection.connect((err) => {
  if (err) {
    console.error("Error connecting to the database:", err.stack);
    return;
  }
  console.log("Connected to the database as id " + connection.threadId);
});
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
        entidad[0].text.lower()}.getAll);\n"""
    code += f"""app.get("/{entidad[0].text}/:{primarykey}",{
        entidad[0].text.lower()}.getAll);\n"""
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
