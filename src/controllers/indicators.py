import pandas as pd
import os
import talib
import numpy as np

def run_indicators(symbol, file):
        try:
            if os.path.exists(file):
                # read file
                df = np.genfromtxt(file, delimiter=',')
                
                # run talib indicators using dataframe
                # create additional columns in the datafarame
                closePrice = df[:,4]
                openPrice = df[:,1]
                highPrice = df[:,2]
                lowPrice = df[:,3]
                volume = df[:,5]
                
                sma = talib.SMA(closePrice)
                atr = talib.ATR(highPrice, lowPrice, closePrice)
                natr = talib.NATR(highPrice, lowPrice, closePrice)
                adx = talib.ADX(highPrice, lowPrice, closePrice)
                mfi = talib.MFI(highPrice, lowPrice, closePrice, volume)
                ppo = talib.PPO(closePrice, fastperiod=12, slowperiod=26, matype=0)
                rsi = talib.RSI(closePrice)
                slowk, slowd = talib.STOCH(highPrice, lowPrice, closePrice, fastk_period=14, slowk_period=3, slowd_period=3)
                macd, macdsignal, macdhist = talib.MACD(closePrice, fastperiod=12, slowperiod=26, signalperiod=9)
            
                # create crypto object
                crypto = {}
                
                crypto['ticker'] = symbol
                crypto['price'] = closePrice[-1]
                crypto['SMA14'] = sma[-1]
                crypto['ATR'] = atr[-1]
                crypto['NATR'] = natr[-1]
                crypto['ADX'] = adx[-1]
                crypto['MFI'] = mfi[-1]
                crypto['RSI'] = rsi[-1]
                crypto['STO'] = slowk[-1], slowd[-1]
                crypto['MACD'] = macd[-1]
                crypto['PPO'] = ppo[-1]

                return crypto
            else:
                pass
        except Exception as e:
            print(str(e))