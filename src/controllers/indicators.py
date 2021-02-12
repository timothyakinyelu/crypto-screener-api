import pandas as pd
import os
import talib

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