constclientes = require(".models/clientes.model");
const Clientes = {
  get: async (req, res) => {
    const { cod_cliente } = req.params;
    const temp = await clientes.findOne({ cod_cliente });
    res.status(200).send(temp);
  },
  getAll: async (req, res) => {
    const temp = awaitclientes.find();
    res.status(200).send(temp);
  },
  noExist: async (req, res) => {
    res.status(404).send("No existe");
  },
  create: async (req, res) => {
    const temp = newclientes(req.body);
    const saved = await temp.save();
    res.status(201).send(saved._id);
  },
  update: async (req, res) => {
    const { cod_cliente } = req.params;
    const temp = await clientes.findOne({ cod_cliente });
    Object.assing(temp, req.body);
    await user.save();
    res.status(204);
  },
  destroy: async (req, res) => {
    const { cod_cliente } = req.params;
    const temp = await clientes.findOne({ cod_cliente });
    if (temp) {
      await clientes.deleteOne({ cod_cliente });
    }
  },
};
module.exports = Clientes;
