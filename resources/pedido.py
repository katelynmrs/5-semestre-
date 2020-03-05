from flask_restful import Resource
from models.pedido import PedidosModel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from resources.roupas import Roupas, Roupa

class Pedidos(Resource):
    def get (self):
        return {'pedidos': [pedido.json() for pedido in PedidosModel.query.all()]}

class Pedido(Resource):
    def get(self, pedido):
        pedido = PedidosModel.find_pedido(pedido)
        if pedido:
            return pedido.json()
        return {'message': 'O pedido não foi encontrado'}, 404 #not found

    def post(self, pedido):
        if PedidosModel.find_pedido(pedido):
            return {'message': "O pedido já existe '{}' já existe.".format(pedido)}, 400 #bad request
        pedido = PedidosModel(pedido)
        try:
            pedido.save_pedido()
        except:
            return {'message': 'Ocorreu um erro interno tentando criar este pedido.'}, 500 #error
        return pedido.json()

    def delete(self, pedido):
        pedido = PedidosModel.fint_pedido(pedido)
        if pedido:
            pedido.delete_pedido()
            return {'message': 'O pedido foi deletado'}, 200
        return {'message': 'Este pedido não existe'}
