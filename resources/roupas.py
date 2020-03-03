from flask_restful import Resource, reqparse
from models.roupas import RoupasModel
from flask_jwt_extended import jwt_required
import sqlite3 # a consulta ela é feita atrávez do banco

roupa = []

def normalize_path_params(nome=None,
                          #cor=None,
                          preco_min=0,
                          preco_max=10000,
                          limit = 50,
                          offset= 0,**dados):
    if nome: #or cor:
        return {
            'preco_min': preco_min,
            'preco_max': preco_max,
            'nome': nome,
            #'cor': cor,
            'limit': limit,
            'offset': offset}
    return {
            'preco_min': preco_min,
            'preco_max': preco_max,
            'limit': limit,
            'offset': offset}

# path/roupas?cor=vermelha&preco_min=50&preco_max=400 (exemplo de path)

path_params = reqparse.RequestParser()
path_params.add_argument('nome', type=str)
#path_params.add_argument('cor', type=str)
path_params.add_argument('preco_min', type=float)
path_params.add_argument('preco_max', type=float)
path_params.add_argument('limit', type=float) # quantidade de item para exibir por pagina
path_params.add_argument('offset', type=float) # quantidade de item que deseja pular

class Roupas(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None} #tratamento para dados validos, os dados que aperecem como NULL por exemplos não são validos.
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('nome'):
            consulta = "SELECT * FROM roupas \
            WHERE (preco >= ? and preco <= ?) \
            LIMIT ? OFFSET ? "
            tupla = tuple([parametros[chave] for chave in parametros]) # ele pega os argument na ordem
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM roupas \
            WHERE (preco >= ? and preco <= ?) \
            and nome = ? LIMIT ? OFFSET ? "
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)

        roupas = []
        for linha in resultado:
            roupas.append({
                'roupa_id': linha[0],
                'nome':linha[1],
                'cor':linha[2],
                'preco':linha[3]
            })

        #return {'roupas': [roupa.json() for roupa in RoupasModel.query.all()]}
        return {'roupas': roupas}

class Roupa(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ficar em branco")
    argumentos.add_argument('cor',type=str, required=False, help="O campo 'cor' não pode ficar em branco")
    argumentos.add_argument('preco')

    def get(self, roupa_id):
        roupa = RoupasModel.find_roupa(roupa_id)
        if roupa:
            return roupa.json()
        return {'message': 'A Roupa não foi encontrada.'}, 404 #Not Found

    #@jwt_required
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

    #@jwt_required
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
