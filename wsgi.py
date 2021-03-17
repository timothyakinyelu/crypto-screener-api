from src import createApp
from src.controllers.generators import generate_candlesticks
import pandas as pd
import multiprocessing

app = createApp()

@app.cli.command()
def scheduled():
    pool = multiprocessing.Pool()
    
    df = pd.read_csv('src/datasets/symbols.csv')
    for symbol in df.iterrows():
        symbol_name = symbol[1][0]
        
        pool.apply_async(func=generate_candlesticks, args=(symbol_name,))
    pool.close()
    pool.join()

if __name__ == '__main__':
    app.run()