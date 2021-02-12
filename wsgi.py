from src import createApp
from src.controllers.generators import generate_candlesticks
import click

app = createApp()

@app.cli.command()
@click.argument("symbol")
def scheduled(symbol):
    generate_candlesticks(symbol)

if __name__ == '__main__':
    app.run()