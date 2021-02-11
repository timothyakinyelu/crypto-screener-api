from flask import Flask, json, jsonify, make_response
from flask_cors import CORS
from src.helpers.load_config import loadConfig
from binance.client import Client
from flask_caching import Cache
from datetime import datetime, timedelta
import pandas as pd
import os
import talib
import click

cache = Cache()

def createApp():
    """initialize app"""
    
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    MODE = app.env
    Config = loadConfig(MODE)
    app.config.from_object(Config)
    cache.init_app(app)
    
    client = Client(app.config['BINANCE_API_KEY'], app.config['BINANCE_SECRET_KEY'])
    
    def generate_candlesticks(symbol):
        """ Generate candlestick files for each crypto"""
        
        start_date = datetime.now() - timedelta(hours=24)
        end_date = datetime.now()
        
        startValue = int(datetime.timestamp(start_date)  * 1000)
        endValue = int(datetime.timestamp(end_date) * 1000)
        
        filename = 'src/datasets/cryptodata/{}_candles.csv'.format(symbol)
        indicatorsFile = 'src/datasets/cryptodata/{}_result.json'.format(symbol)
        
        try:
            if os.path.exists(filename):
                df = pd.read_csv(filename, header=None)
                # get last timestamp from dataframe
                last_timestamp = int(df.tail(1).iloc[0].get(0)) + (30 * 60 * 1000)
                
                candles = client.get_klines(
                    symbol = symbol,
                    interval = Client.KLINE_INTERVAL_30MINUTE,
                    startTime = last_timestamp,
                    endTime = endValue
                )
                
                # remove rows from top based on length of new candles fetched
                index_to_delete = len(candles)
                df = df.iloc[index_to_delete:]
                
                # remove columns that aren't needed from the candles
                for line in candles:
                    del line[6:]
                    
                df2 = pd.DataFrame(candles)
                df3 = df.append(df2)
                
                # write new dataframe to csv with updated rows
                with open(filename, 'w') as f:
                    df3.to_csv(f, header=None, index=False)   
            else:
                candles = client.get_klines(
                    symbol = symbol,
                    interval = Client.KLINE_INTERVAL_30MINUTE,
                    startTime = startValue,
                    endTime = endValue
                )
                
                # remove columns that aren't needed from the candles
                if candles:
                    for line in candles:
                        del line[6:]
                        
                    df = pd.DataFrame(candles)
                    df.to_csv(filename, header=None, index=False)
                else:
                    pass
            result = run_indicators(symbol, filename)
            with open(indicatorsFile, 'w') as f:
                json.dump(result, f)
                
            cache.set('{}_file'.format(symbol), indicatorsFile)
        except Exception:
            pass
    
    
    def run_indicators(symbol, file):
        try:
            if os.path.exists(file):
                # read file
                df = pd.read_csv(file, header=None)
                
                # run talib indicators using dataframe
                # create additional columns in the datafarame
                openPrice = df[1]
                highPrice = df[2]
                lowPrice = df[3]
                closePrice = df[4]
                volume = df[5]
                
                df[6] = talib.SMA(closePrice)
                df[7] = talib.ATR(highPrice, lowPrice, closePrice)
                df[8] = talib.NATR(highPrice, lowPrice, closePrice)
                df[9] = talib.ADX(highPrice, lowPrice, closePrice)
                df[10] = talib.MFI(highPrice, lowPrice, closePrice, volume)
                df[11] = talib.PPO(closePrice, fastperiod=12, slowperiod=26, matype=0)
                df[12] = talib.RSI(closePrice)
                df[13], df[14] = talib.STOCH(highPrice, lowPrice, closePrice, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
                df[15], df[16], df[17] = talib.MACD(closePrice, fastperiod=12, slowperiod=26, signalperiod=9)
            
                # create crypto object
                crypto = {}
                
                crypto['ticker'] = symbol
                crypto['price'] = df.tail(1).iloc[0].get(4)
                crypto['SMA14'] = df.tail(1).iloc[0].get(6)
                crypto['ATR'] = df.tail(1).iloc[0].get(7)
                crypto['NATR'] = df.tail(1).iloc[0].get(8)
                crypto['ADX'] = df.tail(1).iloc[0].get(9)
                crypto['MFI'] = df.tail(1).iloc[0].get(10)
                crypto['RSI'] = df.tail(1).iloc[0].get(12)
                crypto['STO'] = df.tail(1).iloc[0].get(13), df.tail(1).iloc[0].get(14)
                crypto['MACD'] = df.tail(1).iloc[0].get(15)

                # res = {'data': crypto}
                return crypto
            else:
                pass
        except Exception as e:
            print(str(e))
      
          
    @app.cli.command()
    @click.argument("symbol")
    def scheduled(symbol):
        print(symbol)
        # generate_candlesticks(symbol)
    
    @app.route('/')
    def index():
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
    
    
    with app.app_context():
        return app