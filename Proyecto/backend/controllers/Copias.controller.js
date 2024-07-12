

const Copias=
{
get: async(req,res)=>{
 const{n_copia}=req.params; try {
    const query = 'SELECT * FROM Copias WHERE cod_cliente = ?';const [results] = await req.db.execute(query, [n_copia]);await req.db.end();
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
    const query = 'SELECT * FROM Copias'; const [results] = await req.db.execute(query);
    await req.db.end();
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
},noExist: (req, res) => {
        res.status(404).send("No existe");
      },

    create: async(req,res)=>{
      const{deteriorada, formato, id_pelicula, precio_alquiler}= req.body
try{
      const query = 'INSERT INTO Copias (deteriorada, formato, id_pelicula, precio_alquiler) VALUES (?, ?, ?, ?)';
const [results] = await req.db.execute(query, [deteriorada, formato, id_pelicula, precio_alquiler])
    await req.db.end();res.status(201).json({n_copia:results.insertId, deteriorada, formato, id_pelicula, precio_alquiler});
    } catch (error) {
        res.status(500).json({ error: error.message });
      }
    },

      update: async(req,res)=>{
      const{n_copia}=req.params;
    const{deteriorada, formato, id_pelicula, precio_alquiler}=req.body;
try{
    const query='UPDATE Copias SET deteriorada = ?, formato = ?, id_pelicula = ?, precio_alquiler WHERE n_copia = ? ';
const[results]=await req.db.execute(query,[deteriorada, formato, id_pelicula, precio_alquiler,n_copia]);
        await req.db.end();if(results.affectedRows===0){
      return res.status(404).json({error:error.message});
      }
      }
      catch(error){
        res.status(500).json({error:error.message})}
        },

        delete: async(req,res)=>{
      const{n_copia}=req.params;
try {
    

    const query = 'DELETE FROM Copias WHERE n_copia = ?';
    const [results] = await req.db.execute(query, [n_copia]);
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

  module.exports=Copias;