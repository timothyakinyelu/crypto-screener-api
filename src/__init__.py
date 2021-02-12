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
    
    with app.app_context():
        # add route blueprints
        from src.views import routes
        
        app.register_blueprint(routes.main)
        return app