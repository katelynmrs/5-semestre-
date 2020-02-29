from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(30))
    senha = banco.Column(banco.String(30))
    nome = banco.Column(banco.String(80))

    def __init__(self, login, senha, nome):
        self.login = login
        self.senha = senha
        self.nome = nome

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'nome': self.nome
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()  #SELECT * FROM Roupas Where roupa_id = $roupa_id
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        login = cls.query.filter_by(login=login).first()  #SELECT * FROM Roupas Where roupa_id = $roupa_id
        if login:
            return login
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
    
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
