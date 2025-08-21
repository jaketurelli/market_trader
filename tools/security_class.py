class Security:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.url = f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest"

    def __repr__(self):
        return f"Security(symbol='{self.symbol}', name={self.name})"
