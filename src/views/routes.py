from . import main
from flask.views import MethodView
from flask import make_response, json
import pandas as pd

class ScreenerView(MethodView):
    """Class controlling public routes"""
    
    def get(self):
        files = pd.read_csv('src/datasets/symbols.csv', sep='\n', header=None)
        dfs = []
        
        # iterate over the csv file to get symbol names
        for symbol in files.iterrows():
            symbol_name = symbol[1][0]
            coin_json = cache.get('{}_file'.format(symbol_name))
            
            df = pd.read_json(coin_json, typ='series')
            dfs.append(df)
            
        temp = pd.concat(dfs, axis=1)
        res = {'data': temp}
        res_json = json.dumps(res, default=lambda temp: json.loads(temp.to_json()))
        results = json.loads(res_json)
        # print(temp.transpose())
        return make_response(results, 200)
    
    
# define public routes
screener_view = ScreenerView.as_view('screener_view')

# create url endpoints
main.add_url_rule(
    '/',
    view_func=screener_view
)