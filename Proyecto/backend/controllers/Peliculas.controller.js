
const peliculas=require("../models/peliculas.model")
const Peliculas=
{
get: async(req,res)=>{
 const{id_pelicula}=req.params;const temp= await peliculas.findOne({id_pelicula});res.status(200).send(temp);
    },
    getAll: async(req,res)=>{const temp= await peliculas.find();
    res.status(200).send(temp);
    },
noExist: async(req,res)=>{
        res.status(404).send("No existe")
        },

        create: async(req,res)=>{try{const temp= new peliculas(req.body);
    const saved= await temp.save();
    res.status(201).send(saved._id);
    }
catch (error) {
    res.status(400).send(error);
  }},
update: async(req,res)=>{const{ id_pelicula}=req.params
        try {
        const updated = await peliculas.findOneAndUpdate({id_pelicula}, 
req.body,
{ new : true, runValidators:true });
        if(!updated){
          return  res.status(404).send("No encontrado");
            }
        res.status(200).send(updated);
        } catch (error){
            res.status(400).send(error)
        }
},
        delete: async (req,res)=>{
        const{id_pelicula}=req.params;
const temp = await peliculas
        .findOne({id_pelicula});
if(temp){
        await peliculas.deleteOne({id_pelicula});}
res.status(200).send("Se ha eliminado con exito");}
}
module.exports=Peliculas;