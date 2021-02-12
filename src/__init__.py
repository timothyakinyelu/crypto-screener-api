from flask import Flask, json, jsonify, make_response
from flask_cors import CORS
from src.helpers.load_config import loadConfig
from flask_caching import Cache

cache = Cache()

def createApp():
    """initialize app"""
    
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    MODE = app.env
    Config = loadConfig(MODE)
    app.config.from_object(Config)
    cache.init_app(app)
    
    
    # @app.route('/')
    # def index():
    #     generate_candlesticks()
    #     # files = pd.read_csv('src/datasets/symbols.csv', sep='\n', header=None)
    #     # dfs = []
        
    #     # # iterate over the csv file to get symbol names
    #     # for symbol in files.iterrows():
    #     #     symbol_name = symbol[1][0]
    #     #     coin_json = cache.get('{}_file'.format(symbol_name))
            
    #     #     df = pd.read_json(coin_json, typ='series')
    #     #     dfs.append(df)
            
    #     # temp = pd.concat(dfs, axis=1)
    #     # res = {'data': temp}
    #     # res_json = json.dumps(res, default=lambda temp: json.loads(temp.to_json()))
    #     # results = json.loads(res_json)
    #     # # print(temp.transpose())
    #     # return make_response(results, 200)
    #     return make_response(jsonify({'msg':'success'}), 200)
    
    
    with app.app_context():
        # add route blueprints
        from src.views import routes
        
        app.register_blueprint(routes.main)
        return app