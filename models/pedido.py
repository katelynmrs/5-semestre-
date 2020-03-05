from sql_alchemy import banco

class PedidosModel(banco.Model):
    __tablename__ = 'pedidos'

    pedido_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.Integer, banco.ForeignKey('roupa.nome'))
    cor = banco.Column(banco.Integer, banco.ForeignKey('roupa.cor'))
    preco= banco.Column(banco.Integer, banco.ForeignKey('roupa.preco'))
    user= banco.Column(banco.Integer, banco.ForeignKey('usuarios.user_id'))

    def __init__(self, nome, cor, preco, user_id):
        self.nome = nome
        self.cor = cor
        self.preco = preco
        self.user_id = user_id

    def json(self):
        return {
            'self.pedido_id': self.pedido_id,
            'nome': self.nome,
            'cor': self.cor,
            'preco': self.preco,
            'user_id': self.user_id
        }

    @classmethod
    def find_pedido(cls, pedido_id):
        pedido = cls.query.filter_by(pedido_id=pedido_id).first()  #SELECT * FROM Roupas Where roupa_id = $roupa_id
        if pedido:
            return pedido
        return None

    def save_pedido(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_pedido(self):
        # deletando todos as roupas associados ao pedido.
        [roupa.delete_roupa() for roupa in self.roupas]

        # deletando pedido
        banco.session.delete(self)
        banco.session.commit()
