from flask import Flask
from flask_restful import Api
from resources.roupas import Roupas, Roupa

app = Flask(__name__)
api = Api(app)

api.add_resource(Roupas, '/roupas')
api.add_resource(Roupa, '/roupas/<string:roupa_id>')

if __name__ == '__main__':
    app.run(debug=True)
