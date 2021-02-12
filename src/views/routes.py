from . import main
from flask.views import MethodView
from flask import make_response, json
from src import cache
from pathlib import Path
import pandas as pd
import os

class ScreenerView(MethodView):
    """Class controlling public routes"""
    
    def get(self):
        dataFolder = Path('src/datasets/')
        dataFile = dataFolder / "symbols.csv"
        files = pd.read_csv(dataFile, sep='\n', header=None)
        dfs = []
        
        # iterate over the csv file to get symbol names
        for symbol in files.iterrows():
            symbol_name = symbol[1][0]
            coin_json = cache.get('{}_file'.format(symbol_name))
            
            if coin_json:
                df = pd.read_json(coin_json, typ='series')
                dfs.append(df)
            else:
                pass
            
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