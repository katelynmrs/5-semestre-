from sql_alchemy import banco

class RoupasModel(banco.Model):
    __tablename__= 'roupas'

    roupa_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(100))
    cor = banco.Column(banco.String(80))
    preco = banco.Column(banco.Float(precision=1))

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

    @classmethod
    def find_roupa(cls, roupa_id):
        roupa = cls.query.filter_by(roupa_id=roupa_id).first()  #SELECT * FROM Roupas Where roupa_id = $roupa_id
        if roupa:
            return roupa
        return None

    def save_roupa(self):
        banco.session.add(self)
        banco.session.commit()
