
from alpaca.trading.models import Position as AlpacaPosition


class OpenPosition:
    def __init__(self, alpaca_position: AlpacaPosition, percent_gain_to_sell: float = 1.0):
        self.alpaca_position = alpaca_position
        self.percent_gain_to_sell = percent_gain_to_sell

    def should_sell(self):
        if self.alpaca_position.unrealized_plpc >= self.percent_gain_to_sell:
            return True
        return False

# if __name__ == "__main__":
#     position = OpenPosition("AAPL", "Apple Inc.")
#     print(position)
