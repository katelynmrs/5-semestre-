from flask_restful import Resource, reqparse
from models.roupas import RoupasModel
from flask_jwt_extended import jwt_required

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
        return {'roupas': [roupa.json() for roupa in RoupasModel.query.all()]}

class Roupa(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ficar em branco")
    argumentos.add_argument('cor',type=str, required=True, help="O campo 'cor' não pode ficar em branco")
    argumentos.add_argument('preco')

    def get(self, roupa_id):
        roupa = RoupasModel.find_roupa(roupa_id)
        if roupa:
            return roupa.json()
        return {'message': 'A Roupa não foi encontrada.'}, 404 #Not Found

    @jwt_required
    def post(self, roupa_id):
        if RoupasModel.find_roupa(roupa_id):
            return {'message': 'A Roupa ID "{}" já existe.'.format(roupa_id)}, 400 #bad Request
        dados = Roupa.argumentos.parse_args()
        roupa = RoupasModel(roupa_id, **dados)
        try:
            roupa.save_roupa()
        except:
            return {'message': 'Ocorreu um erro interno ao salvar a Roupa.'}, 500 # Internal Server Error
        return roupa.json()

    @jwt_required
    def put(self, roupa_id):
        dados = Roupa.argumentos.parse_args()
        roupa_encontrada = RoupasModel.find_roupa(roupa_id)
        if roupa_encontrada:
            roupa_encontrada.update_roupa(**dados)
            roupa_encontrada.save_roupa()
            return roupa_encontrada.json(), 200
        roupa = RoupasModel(roupa_id, **dados)
        try:
            roupa.save_roupa()
        except:
            return {'message': 'Ocorreu um erro interno ao salvar a Roupa.'}, 500 # Internal Server Error
        return roupa.json(), 201 #created/criado
    @jwt_required
    def delete(self, roupa_id):
        roupa = RoupasModel.find_roupa(roupa_id)
        if roupa:
            try:
                roupa.delete_roupa()
            except:
                return {'message': 'Ocorreu um erro interno ao deletar a Roupa'}, 500 # Internal Server Error
            return {'message': 'Camisa deletada.'}
        return {'message': 'Camisa não existe.'}, 404
