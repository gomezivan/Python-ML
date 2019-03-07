app = Flask(__name__)

api = Api(
    app, 
    version='1.0', 
    title='Estimador de precio vehicular',
    description='Ivan G.')

ns = api.namespace('Predict', 
     description='Predict price')
   
parser = api.parser()

parser.add_argument(
    'Make', 
    type=str, 
    required=True, 
    help='Car Maker', 
    location='args')

parser.add_argument(
    'Model', 
    type=str, 
    required=True, 
    help='Car Model', 
    location='args')

parser.add_argument(
    'State', 
    type=str, 
    required=True, 
    help='State', 
    location='args')

parser.add_argument(
    'Mileage', 
    type=str, 
    required=True, 
    help='Mileage', 
    location='args')

parser.add_argument(
    'Year', 
    type=str, 
    required=True, 
    help='Year', 
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
         "result": predict_car_value() #predict_proba(args['URL'])
        }, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8889)