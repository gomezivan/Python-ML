#!/usr/bin/python
from flask import Flask
from flask_restplus import Api, Resource, fields
from sklearn.externals import joblib
from Model_Movie_CLF import clasff_movie

app = Flask(__name__)

api = Api(
    app, 
    version='1.0', 
    title='Movie Genre Classification',
    description='Desarrollado por: Iván Gómez, Cristian Najera, Natalia Martínez')

ns = api.namespace('Classification', 
     description='Classification movie')
   
parser = api.parser()

parser.add_argument(
    'Title', 
    type=str, 
    required=True, 
    help='Title of the movie', 
    location='args')

parser.add_argument(
    'Plot', 
    type=str, 
    required=True, 
    help='Description of the movie', 
    location='args')

parser.add_argument(
    'Year', 
    type=str, 
    required=True, 
    help='Year of the movie', 
    location='args')


resource_fields = api.model('Resource', {
    'result': fields.String,
})

@ns.route('/')
class PredPriceApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        return {
         "result": clasff_movie(args['Title'],args['Plot'],args['Year'])
        }, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8889)