from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="O campo 'login' não pode ser deixado em branco")
atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser deixado em branco")
atributos.add_argument('nome', type=str, required=False, help="O campo 'nome' não pode ser deixado em branco")

class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'O usuário não foi encontrada.'}, 404 #Not Found
    #@jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'Ocorreu um erro interno ao deletar o Usuário'}, 500 # Internal Server Error
            return {'message': 'Usuário foi deletado com sucesso.'}
        return {'message': 'Usuário não existe.'}, 404

class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': "O Usuário '{}' já existe.".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'Usuário criado com sucesso'}, 201 #Created

class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']): #safe_str garante que a senha é igual a do banco
            return {'message': 'Você entrou com sucesso'}, 200
        return {'message': 'O usuário ou senha está incorreto'}, 401 #Não será permitido.p

class UserLogout(Resource):

    #jwt_required
    def post(self):
        #jwt_id = get_raw_jwt()['jti'] # JWT Token Identifier
        #BLACKLIST.add(jwt_id)
        return {'message': 'Logout feito com sucesso!'}, 200
