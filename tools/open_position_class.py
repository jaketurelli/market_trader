
from alpaca.trading.models import Position as AlpacaPosition


class OpenPosition:
    def __init__(self, alpaca_position: AlpacaPosition, same_day: bool = False):
        self.alpaca_position = alpaca_position
        self.is_same_day = same_day

    def __repr__(self):
        return f"Open Position:\nposition=\n'{self.alpaca_position}\n'is_same_day={self.is_same_day})"


# if __name__ == "__main__":
#     position = OpenPosition("AAPL", "Apple Inc.")
#     print(position)
