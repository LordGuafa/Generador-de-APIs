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

const {entidad[0].text}=
"""+'{\n'
    code += "get: async(req,res)=>{\n "
    code += "const{"
    code += f"{primarykey}"+"}=req.params;"
    code += """ try {
    """
    code += f"""const query = 'SELECT * FROM {
        entidad[0].text} WHERE cod_cliente = ?';"""
    code += f"""const [results] = await req.db.execute(query, [{
        primarykey}]);"""
    code += """await req.db.end();
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
    """
    code += f"""const query = 'SELECT * FROM {entidad[0].text}';"""
    code += """ const [results] = await req.db.execute(query);
    await req.db.end();
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
      """
    code += f"""const query = 'INSERT INTO {entidad[0].text} ("""
    cont = 0
    for i in arrayAtributos:
        if atributo.find("autoincrementable") is not None:
            code += ""
        else:
            cont += 1
            code += i
            if cont < len(arrayAtributos):
                code += ", "
    code += f""") VALUES ({interrogantes})';\n"""
    code += f"""const [results] = await req.db.execute(query, [{listaAtributos}])
    await req.db.end();"""
    code += "res.status(201).json({"
    code += f'{primarykey}:results.insertId, {listaAtributos}'
    code += """});
    } catch (error) {
        res.status(500).json({ error: error.message });
      }
    },\n
      """
    code += """update: async(req,res)=>{
      const{"""
    code += f'{primarykey}'
    code += """}=req.params;
    const{"""
    code += f"{listaAtributos}"+"}=req.body;\n"
    code += """try{
    """
    code += f"""const query='UPDATE {entidad[0].text} SET """
    cont = 0
    for i in arrayAtributos:
        if atributo.find("autoincrementable") is not None:
            code += ""
        else:
            cont += 1
            code += i
        if cont < len(arrayAtributos):
            code += " = ?, "
    code += f" WHERE {primarykey} = ? ';\n"
    code += f"""const[results]=await req.db.execute(query,[{
        listaAtributos},{primarykey}]);
        await req.db.end();"""
    code += """if(results.affectedRows===0){
      return res.status(404).json({error:error.message});
      }
      }
      catch(error){
        res.status(500).json({error:error.message})}
        },

        """
    code += """delete: async(req,res)=>{
      const{"""
    code += f'{primarykey}'+'}=req.params;\n'
    code += """try {
    \n
    """
    code += f"""const query = 'DELETE FROM {entidad[0].text} WHERE {primarykey} = ?';
    const [results] = await req.db.execute(query, [{primarykey}]);
    await req.db.end();\n"""
    code += """if (results.affectedRows === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.status(204).send();
  } catch (error) {
    res.status(500).json({ error: error.message });
  }\n}\n}\n
  """
    code += f'module.exports={entidad[0].text};'
    os.makedirs("./backend/controllers", exist_ok=True)
    file_path = f'backend/controllers/{entidad[0].text}.controller.js'
    with open(file_path, 'w') as file:
        file.write(code)
    code = ""
    listaAtributos = ""
    arrayAtributos.clear()
    interrogantes = ""
