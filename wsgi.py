from src import createApp
import click

app = createApp()

@app.cli.command()
@click.argument("symbol")
def scheduled(symbol):
    print(symbol)

if __name__ == '__main__':
    app.run()