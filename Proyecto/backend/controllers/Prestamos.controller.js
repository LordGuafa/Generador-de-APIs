
constprestamos=require(".models/prestamos.model")
const Prestamos=
{
get: async(req,res)=>{
 const{id_prestamo}=req.params;const temp= await prestamos.findOne({id_prestamo});res.status(200).send(temp);
    },getAll: async(req,res)=>{const temp= awaitprestamos.find();
    res.status(200).send(temp);
    },noExist: async(req,res)=>{
        res.status(404).send("No existe")
        },
        create: async(req,res)=>{const temp= newprestamos(req.body);
    const saved= await temp.save();
    res.status(201).send(saved._id);
    },update: async(req,res)=>{
        const{id_prestamo}=req.params;
const temp = await prestamos
        .findOne({id_prestamo});
Object.assing(temp,req.body);
    await user.save();
    res.status(204);
    },destroy: async (req,res)=>{
        const{id_prestamo}=req.params;
const temp = await prestamos
        .findOne({id_prestamo});
if(temp){
        await prestamos.deleteOne({id_prestamo});}
}
}
module.exports=Prestamos;