from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Calca(Resource):
    def get(self):
        return {'calca': 'calca jeans'}

api.add_resource(Calca, '/calcajeans')

if __name__ == '__main__':
    app.run(debug=True)
