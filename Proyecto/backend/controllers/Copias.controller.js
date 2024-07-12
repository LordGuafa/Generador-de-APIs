
const copias=require("../models/copias.model")
const Copias=
{
get: async(req,res)=>{
 const{n_copia}=req.params;const temp= await copias.findOne({n_copia});res.status(200).send(temp);
    },
    getAll: async(req,res)=>{const temp= await copias.find();
    res.status(200).send(temp);
    },
noExist: async(req,res)=>{
        res.status(404).send("No existe")
        },

        create: async(req,res)=>{try{const temp= new copias(req.body);
    const saved= await temp.save();
    res.status(201).send(saved._id);
    }
catch (error) {
    res.status(400).send(error);
  }},
update: async(req,res)=>{const{ n_copia}=req.params
        try {
        const updated = await copias.findOneAndUpdate({n_copia}, 
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
        const{n_copia}=req.params;
const temp = await copias
        .findOne({n_copia});
if(temp){
        await copias.deleteOne({n_copia});}
res.status(200).send("Se ha eliminado con exito");}
}
module.exports=Copias;