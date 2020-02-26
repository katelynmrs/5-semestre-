from flask_restful import Resource, reqparse
from models.roupas import RoupasModel

roupas =      [
            {
            'roupa_id': 'calcajeans',
            'nome' :'calca jeans',
            'cor' : 'azul',
            'preco': 45.00
            },
            {
            'roupa_id': 'shorts',
            'nome' :'shorts',
            'cor' : 'preto',
            'preco': 30.00
            },
            {
            'roupa_id': 'shortsjeans',
            'nome' :'shorts jeans',
            'cor' : 'azul',
            'preco': 30.00
            }
]
class Roupas(Resource):
    def get(self):
        return {'roupas': roupas}

class Roupa(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('roupa_id')
    argumentos.add_argument('nome')
    argumentos.add_argument('cor')
    argumentos.add_argument('preco')

    def get(self, roupa_id):
        roupa = RoupasModel.find_roupa(roupa_id)
        if roupa:
            return roupa
        return {'message': 'A Roupa não foi encontrada.'}, 404 #Not Found

    def post(self, roupa_id):
        if RoupasModel.find_roupa(roupa_id):
            return {'message': 'A Roupa ID "{}" já existe.'.format(roupa_id)}, 400 #bad Request
        dados = Roupa.argumentos.parse_args()
        roupa = RoupaModel(roupa_id, **dados)
        roupa.save_roupa()
        return roupa.json()


    def put(self, roupa_id):
        dados = Roupa.argumentos.parse_args()
        nova_roupa = {'roupa_id': roupa_id, **dados}
        roupa = Roupa.find_roupa(roupa_id)
        if roupa:
            roupa.update(nova_roupa)
            return nova_roupa, 200
        roupas.append(nova_roupa)
        return nova_roupa, 201 #created/criado

    def delete(self, roupa_id):
        global roupas
        roupas = [roupa for roupa in roupas if roupa['roupa_id'] != roupa_id]
        return {'message': 'Hotel deletado.'}
