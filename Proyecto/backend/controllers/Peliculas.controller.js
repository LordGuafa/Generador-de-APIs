
constpeliculas=require(".models/peliculas.model")
const Peliculas=
{
get: async(req,res)=>{
 const{id_pelicula}=req.params;const temp= await peliculas.findOne({id_pelicula});res.status(200).send(temp);
    },getAll: async(req,res)=>{const temp= awaitpeliculas.find();
    res.status(200).send(temp);
    },noExist: async(req,res)=>{
        res.status(404).send("No existe")
        },
        create: async(req,res)=>{const temp= newpeliculas(req.body);
    const saved= await temp.save();
    res.status(201).send(saved._id);
    },update: async(req,res)=>{
        const{id_pelicula}=req.params;
const temp = await peliculas
        .findOne({id_pelicula});
Object.assing(temp,req.body);
    await user.save();
    res.status(204);
    },destroy: async (req,res)=>{
        const{id_pelicula}=req.params;
const temp = await peliculas
        .findOne({id_pelicula});
if(temp){
        await peliculas.deleteOne({id_pelicula});}
}
}
module.exports=Peliculas;