

const Clientes=
{
get: async(req,res)=>{
 const{cod_cliente}=req.params; try {
    const query = 'SELECT * FROM Clientes WHERE cod_cliente = ?';const [results] = await req.db.execute(query, [cod_cliente]);await req.db.end();
    if (results.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
     res.json(results[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
  },
getAll: async (req, res) => {
  try {
    const query = 'SELECT * FROM Clientes'; const [results] = await req.db.execute(query);
    await req.db.end();
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
},noExist: (req, res) => {
        res.status(404).send("No existe");
      },

    create: async(req,res)=>{
      const{dni, nombre, apellido1, apellido2, direccion, email}= req.body
try{
      const query = 'INSERT INTO Clientes (dni, nombre, apellido1, apellido2, direccion, email) VALUES (?, ?, ?, ?, ?, ?)';
const [results] = await req.db.execute(query, [dni, nombre, apellido1, apellido2, direccion, email])
    await req.db.end();res.status(201).json({cod_cliente:results.insertId, dni, nombre, apellido1, apellido2, direccion, email});
    } catch (error) {
        res.status(500).json({ error: error.message });
      }
    },

      update: async(req,res)=>{
      const{cod_cliente}=req.params;
    const{dni, nombre, apellido1, apellido2, direccion, email}=req.body;
try{
    const query='UPDATE Clientes SET dni = ?, nombre = ?, apellido1 = ?, apellido2 = ?, direccion = ?, email WHERE cod_cliente = ? ';
const[results]=await req.db.execute(query,[dni, nombre, apellido1, apellido2, direccion, email,cod_cliente]);
        await req.db.end();if(results.affectedRows===0){
      return res.status(404).json({error:error.message});
      }
      }
      catch(error){
        res.status(500).json({error:error.message})}
        },

        delete: async(req,res)=>{
      const{cod_cliente}=req.params;
try {
    

    const query = 'DELETE FROM Clientes WHERE cod_cliente = ?';
    const [results] = await req.db.execute(query, [cod_cliente]);
    await req.db.end();
if (results.affectedRows === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.status(204).send();
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
}

  module.exports=Clientes;