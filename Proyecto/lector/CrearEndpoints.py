import xml.etree.ElementTree as ET
import os

root = ET.parse("lector/prueba.xml").getroot()
nombre_db = root.find("Nombre")
entidades = root.findall("Entidad")
interrogantes = ""
listaAtributos = ""
arrayAtributos = []
for entidad in entidades:
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
    code = f"""const express = require("express");
const mysql = require("mysql2");
const bodyParser = require("body-parser");
const fs = require("fs");
const {entidad[0].text}=
"""+'{\n'
    code += "get: async(req,res)=>{\n "
    code += "const{"
    code += f"{primarykey}"+"}=req.params;"
    code += """ try {
    const connection = await getConnection();
    const query = 'SELECT * FROM users WHERE cod_cliente = ?';"""
    code += f"const [results] = await connection.execute(query, [{primarykey}]);"
    code += """await connection.end();
    if (results.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
     res.json(results[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
  },\n"""
    code += """getAll: async (req, res) => {
  try {
    const connection = await getConnection();
    const query = 'SELECT * FROM users';
    const [results] = await connection.execute(query);
    await connection.end();
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
},"""
    code += """noExist: (req, res) => {
        res.status(404).send("No existe");
      },
    
    """
    code += """create: async(req,res)=>{
      const{"""
    code += f'{listaAtributos}'
    code += "}= req.body\n"
    code += """try{
      const connection = await getConnection();"""
    code += f"""const query = 'INSERT INTO users ("""
    cont = 0
    for i in arrayAtributos:
        cont += 1
        code += i
        if cont < len(arrayAtributos):
            code += ", "
    code += f""") VALUES ({interrogantes})';"""
    code += f"""const [results] = await connection.execute(query, [{listaAtributos}])
    await connection.end();"""
    code += "res.status(201).json({"
    code += f'{primarykey}:results.insertId, {listaAtributos}'
    code += """});
    } catch (error) {
        res.status(500).json({ error: error.message });
      }
    }
      """
    code += """update: async(req,res)=>{
      const{"""
    code += f'{primarykey}'
    code += """}req.params;
    const{"""
    code += f"{listaAtributos}"+"}=req.body;\n"
    code += """try{
    const connection= await getConnection();\n
    """
    code += f"""'const query='UPDATE {entidad[0].text} SET'"""
    for i in arrayAtributos:
        cont += 1
        code += i
        if cont < len(arrayAtributos):
            code += " = ?, "
    code += f"WHERE{primarykey}=?;\n"
    code
    os.makedirs("./backend/controllers", exist_ok=True)
    file_path = f'backend/controllers/{entidad[0].text}.controller.js'
    with open(file_path, 'w') as file:
        file.write(code)


# app.put("/Clientes/:cod_cliente", clientes.update)
# app.delete("/Clientes/:cod_cliente", clientes.delete);
