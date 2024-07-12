
const clientes=require("../models/clientes.model")
const Clientes=
{
get: async(req,res)=>{
 const{cod_cliente}=req.params;const temp= await clientes.findOne({cod_cliente});res.status(200).send(temp);
    },
    getAll: async(req,res)=>{const temp= await clientes.find();
    res.status(200).send(temp);
    },
noExist: async(req,res)=>{
        res.status(404).send("No existe")
        },

        create: async(req,res)=>{try{const temp= new clientes(req.body);
    const saved= await temp.save();
    res.status(201).send(saved._id);
    }
catch (error) {
    res.status(400).send(error);
  }},
update: async(req,res)=>{const{ cod_cliente}=req.params
        try {
        const updated = await clientes.findOneAndUpdate({cod_cliente}, 
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
        const{cod_cliente}=req.params;
const temp = await clientes
        .findOne({cod_cliente});
if(temp){
        await clientes.deleteOne({cod_cliente});}
res.status(200).send("Se ha eliminado con exito");}
}
module.exports=Clientes;