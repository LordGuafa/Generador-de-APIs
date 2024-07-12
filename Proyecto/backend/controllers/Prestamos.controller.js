
const prestamos=require("../models/prestamos.model")
const Prestamos=
{
get: async(req,res)=>{
 const{id_prestamo}=req.params;const temp= await prestamos.findOne({id_prestamo});res.status(200).send(temp);
    },
    getAll: async(req,res)=>{const temp= await prestamos.find();
    res.status(200).send(temp);
    },
noExist: async(req,res)=>{
        res.status(404).send("No existe")
        },

        create: async(req,res)=>{try{const temp= new prestamos(req.body);
    const saved= await temp.save();
    res.status(201).send(saved._id);
    }
catch (error) {
    res.status(400).send(error);
  }},
update: async(req,res)=>{const{ id_prestamo}=req.params
        try {
        const updated = await prestamos.findOneAndUpdate({id_prestamo}, 
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
        const{id_prestamo}=req.params;
const temp = await prestamos
        .findOne({id_prestamo});
if(temp){
        await prestamos.deleteOne({id_prestamo});}
res.status(200).send("Se ha eliminado con exito");}
}
module.exports=Prestamos;