import xml.etree.ElementTree as ET
import os


def crearApiSQLJS(root, project_dir):
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
  app.use(express.json());"""

    code += """// Configurar la conexion a la base de datos MySQL
  const dbConfig = {
    host: "api-db",
    user: "root",
    password: "1234",""" + f"""database:"{root.find("Nombre").text}","""+""" 
    };"""

    code += """// Middleware para inyectar la conexión de la base de datos en las solicitudes
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

        code += f"""app.get("/{entidad[0].text}/:{primarykey}",{
            entidad[0].text.lower()}.get);\n"""
        code += f"""app.put("/{entidad[0].text}/:{primarykey}",{
            entidad[0].text.lower()}.update);\n"""
        code += f"""app.delete("/{entidad[0].text}/:{primarykey}",{
            entidad[0].text.lower()}.delete);\n"""
        code += f"""app.get("/{entidad[0].text}/*",{
            entidad[0].text.lower()}.noExist);\n"""
        code += "//---------------------------------------------------------------------\n"
    code += """
  const PORT = process.env.PORT || 8080;
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });

  """
    json = """{
  "dependencies": {
    "body-parser": "^1.20.2",
    "express": "^4.19.2",
    "mongoose": "^8.5.0",
    "mongoose-sequence": "^6.0.1",
    "mysql2": "^3.10.2"
  },
  "scripts": {
    "start": "node ./backend/Api.js"
  }
}"""
    os.makedirs(project_dir+"/backend", exist_ok=True)
    file_path = project_dir+'/backend/Api.js'
    file_path2 = project_dir+'/package.json'
    with open(file_path, 'w') as file:
        file.write(code)
    with open(file_path2, 'w') as file:
        file.write(json)
