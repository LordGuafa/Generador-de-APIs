

const Peliculas=
{
get: async(req,res)=>{
 const{id_pelicula}=req.params; try {
    const query = 'SELECT * FROM Peliculas WHERE cod_cliente = ?';const [results] = await req.db.execute(query, [id_pelicula]);await req.db.end();
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
    const query = 'SELECT * FROM Peliculas'; const [results] = await req.db.execute(query);
    await req.db.end();
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
},noExist: (req, res) => {
        res.status(404).send("No existe");
      },

    create: async(req,res)=>{
      const{titulo, anno, critica, caratula}= req.body
try{
      const query = 'INSERT INTO Peliculas (titulo, anno, critica, caratula) VALUES (?, ?, ?, ?)';
const [results] = await req.db.execute(query, [titulo, anno, critica, caratula])
    await req.db.end();res.status(201).json({id_pelicula:results.insertId, titulo, anno, critica, caratula});
    } catch (error) {
        res.status(500).json({ error: error.message });
      }
    },

      update: async(req,res)=>{
      const{id_pelicula}=req.params;
    const{titulo, anno, critica, caratula}=req.body;
try{
    const query='UPDATE Peliculas SET titulo = ?, anno = ?, critica = ?, caratula WHERE id_pelicula = ? ';
const[results]=await req.db.execute(query,[titulo, anno, critica, caratula,id_pelicula]);
        await req.db.end();if(results.affectedRows===0){
      return res.status(404).json({error:error.message});
      }
      }
      catch(error){
        res.status(500).json({error:error.message})}
        },

        delete: async(req,res)=>{
      const{id_pelicula}=req.params;
try {
    

    const query = 'DELETE FROM Peliculas WHERE id_pelicula = ?';
    const [results] = await req.db.execute(query, [id_pelicula]);
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

  module.exports=Peliculas;