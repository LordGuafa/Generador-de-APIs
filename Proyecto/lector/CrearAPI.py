import xml.etree.ElementTree as ET
import os

root = ET.parse("lector/prueba.xml").getroot()
nombre_db = root.find("Nombre")
entidades = root.findall("Entidad")
code = """
const express = require("express");
const mysql = require("mysql2/promise"); // Utiliza mysql2/promise para soporte de async/await
const bodyParser = require("body-parser");
\n"""
for entidad in entidades:
    code += f"""const {entidad[0].text.lower()
                       }=require('./controllers/{entidad[0].text.lower()}.controller.js')\n"""
code += """const path = require("path");
// Crear una instancia de Express
const app = express();
app.use(express.json());

// Configurar la conexion a la base de datos MySQL
const dbConfig = {
  host: "localhost",
  user: "root",
  password: "1234",
  database: "Prueba",
};

// Middleware para inyectar la conexión de la base de datos en las solicitudes
app.use(async (req, res, next) => {
  try {
    req.db = await mysql.createConnection(dbConfig);
    await req.db.connect();
    next();
  } catch (err) {
    console.error("Error connecting to the database:", err.stack);
    res.status(500).json({ error: "Database connection failed" });
  }
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
