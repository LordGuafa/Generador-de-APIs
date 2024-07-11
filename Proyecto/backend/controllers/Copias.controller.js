
constcopias=require(".models/copias.model")
const Copias=
{
get: async(req,res)=>{
 const{n_copia}=req.params;const temp= await copias.findOne({n_copia});res.status(200).send(temp);
    },getAll: async(req,res)=>{const temp= awaitcopias.find();
    res.status(200).send(temp);
    },noExist: async(req,res)=>{
        res.status(404).send("No existe")
        },
        create: async(req,res)=>{const temp= newcopias(req.body);
    const saved= await temp.save();
    res.status(201).send(saved._id);
    },update: async(req,res)=>{
        const{n_copia}=req.params;
const temp = await copias
        .findOne({n_copia});
Object.assing(temp,req.body);
    await user.save();
    res.status(204);
    },destroy: async (req,res)=>{
        const{n_copia}=req.params;
const temp = await copias
        .findOne({n_copia});
if(temp){
        await copias.deleteOne({n_copia});}
}
}
module.exports=Copias;