

const Prestamos=
{
get: async(req,res)=>{
 const{id_prestamo}=req.params; try {
    const query = 'SELECT * FROM Prestamos WHERE cod_cliente = ?';const [results] = await req.db.execute(query, [id_prestamo]);await req.db.end();
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
    const query = 'SELECT * FROM Prestamos'; const [results] = await req.db.execute(query);
    await req.db.end();
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
},noExist: (req, res) => {
        res.status(404).send("No existe");
      },

    create: async(req,res)=>{
      const{fecha_pretamo, fecha_tope, fecha_entrega, cod_cliente, n_copia}= req.body
try{
      const query = 'INSERT INTO Prestamos (fecha_pretamo, fecha_tope, fecha_entrega, cod_cliente, n_copia) VALUES (?, ?, ?, ?, ?)';
const [results] = await req.db.execute(query, [fecha_pretamo, fecha_tope, fecha_entrega, cod_cliente, n_copia])
    await req.db.end();res.status(201).json({id_prestamo:results.insertId, fecha_pretamo, fecha_tope, fecha_entrega, cod_cliente, n_copia});
    } catch (error) {
        res.status(500).json({ error: error.message });
      }
    },

      update: async(req,res)=>{
      const{id_prestamo}=req.params;
    const{fecha_pretamo, fecha_tope, fecha_entrega, cod_cliente, n_copia}=req.body;
try{
    const query='UPDATE Prestamos SET fecha_pretamo = ?, fecha_tope = ?, fecha_entrega = ?, cod_cliente = ?, n_copia WHERE id_prestamo = ? ';
const[results]=await req.db.execute(query,[fecha_pretamo, fecha_tope, fecha_entrega, cod_cliente, n_copia,id_prestamo]);
        await req.db.end();if(results.affectedRows===0){
      return res.status(404).json({error:error.message});
      }
      }
      catch(error){
        res.status(500).json({error:error.message})}
        },

        delete: async(req,res)=>{
      const{id_prestamo}=req.params;
try {
    

    const query = 'DELETE FROM Prestamos WHERE id_prestamo = ?';
    const [results] = await req.db.execute(query, [id_prestamo]);
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

  module.exports=Prestamos;