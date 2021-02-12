from . import main
from flask.views import MethodView
from flask import make_response, jsonifycd 
from src.controllers.generators import generate_candlesticks

class ScreenerView(MethodView):
    """Class controlling public routes"""
    
    def get(self):
        generate_candlesticks()
        return make_response(jsonify({'msg':'success'}), 200)
    
    
# define public routes
screener_view = ScreenerView.as_view('screener_view')

# create url endpoints
main.add_url_rule(
    '/',
    view_func=screener_view
)