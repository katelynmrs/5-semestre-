from flask_restful import Resource, reqparse

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

class RoupasModel:
    def __init__(self, roupa_id, nome, cor, preco):
        self.roupa_id = roupa_id
        self.nome = nome
        self.cor = cor
        self.preco = preco

    def json(self):
        return {
            'roupa_id': self.roupa_id,
            'nome': self.nome,
            'cor': self.cor,
            'preco': self.preco
        }

class Roupas(Resource):
    def get(self):
        return {'roupas': roupas}

class Roupa(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('roupa_id')
    argumentos.add_argument('nome')
    argumentos.add_argument('cor')
    argumentos.add_argument('preco')

    def find_roupa(roupa_id):
        for roupa in roupas:
            if roupa['roupa_id'] == roupa_id:
                return roupa
        return None
    def get(self, roupa_id):
        roupa = Roupa.find_roupa(roupa_id)
        if roupa:
            return roupa
        return {'message': 'A Roupa não foi encontrada.'}, 404 #Not Found

    def post(self, roupa_id):
        dados = Roupa.argumentos.parse_args()
        nova_roupa = {'roupa_id': roupa_id, **dados}
        #nova_roupa = {'roupa_id': roupa_id, **dados}
        roupas.append(nova_roupa)
        return nova_roupa, 200

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
