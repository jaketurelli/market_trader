import requests
from dotenv import load_dotenv
from collections import deque
from typing import List

import time
import numpy as np
# fmt: off
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.security_class import Security
# fmt: on


class Analyzer:
    def __init__(self, securities: List[Security], max_analyis_samples=5*60):
        self.securities = securities
        # self.price_queue = deque(maxlen=max_analyis_samples)
        # self.time_queue = deque(maxlen=max_analyis_samples)
        self.price_queue = []
        self.time_queue = []

        self.min_index = 0
        self.max_index = 0
        self.index_count = 0
        self.max_analysis_samples = max_analyis_samples

        self.price_linear_approx = None
        self.linear_coeffs = None
        self.linear_slope = 0
        self.linear_slope_threshold = 0

        self.price_2nd_order_approx = None
        self.quad_coeffs = None

        self.plot_count = 0

        import matplotlib.pyplot as plt

        plt.ion()  # Turn on interactive mode

        self.fig, self.ax = plt.subplots(2, 1, figsize=(20, 10))
        x = 1
        # else:
        #     self.ax.cla()  # Clear the axes

        # import matplotlib.pyplot as plt
        # import numpy as np

        # Sample data
        # x = np.linspace(0, 10, 100)
        # y1 = np.sin(x)
        # y2 = np.cos(x)

        # # Create a figure with 2 rows and 2 columns of axes
        # fig, axs = plt.subplots(2, 2, figsize=(10, 6))

        # # Fill each subplot
        # axs[0, 0].plot(x, y1, color='blue')
        # axs[0, 0].set_title('Sine Wave')

        # axs[0, 1].plot(x, y2, color='green')
        # axs[0, 1].set_title('Cosine Wave')

        # axs[1, 0].scatter(x, y1 + y2, color='purple')
        # axs[1, 0].set_title('Sine + Cosine')

        # axs[1, 1].bar(x[::10], y1[::10], color='orange')
        # axs[1, 1].set_title('Bar Plot')

        # plt.tight_layout()
        # plt.show()

    def __repr__(self):
        printable = f"Analyzer(securities=[\n"
        for sec in self.securities:
            printable += f"  {sec.symbol},\n"
        printable += "])"
        return printable

    def __get_size_dataset(self):
        return len(self.queue)

    def plot_data(self):
        import matplotlib.pyplot as plt

        if not self.price_queue or not self.time_queue:
            print("No data to plot.")
            return
        neon_green = '#39FF14'
        neon_yellow = '#FFFF33'
        neon_pink = '#FF6EC7'
        neon_red = '#FF073A'
        neon_blue = '#04D9FF'

        # Set black background for axes and figure
        self.fig.patch.set_facecolor('black')

        # Add coefficients as text on the plot
        linear_text = f"Linear: y = {self.linear_coeffs[0]:.3f}x + {self.linear_coeffs[1]:.3f}"
        quad_text = f"Quadratic: y = {self.quad_coeffs[0]:.3e}x² + {self.quad_coeffs[1]:.3f}x + {self.quad_coeffs[2]:.3f}"

        for i in range(len(self.securities)):
            self.ax[i].cla()  # Clear the axes
            self.ax[i].set_facecolor('black')

            # full day
            self.ax[i].plot(self.time_queue, self.price_queue,
                            linestyle='-', color=neon_blue)

            # linear approx
            self.ax[i].plot(self.time_queue[self.min_index:self.max_index], self.price_linear_approx, marker=None, linestyle='--',
                            color=neon_green if self.linear_slope > self.linear_slope_threshold else neon_pink)

            # 2nd order approx
            self.ax[i].plot(self.time_queue[self.min_index:self.max_index], self.price_2nd_order_approx, marker=None,
                            linestyle=':', color=neon_green if self.quad_coeffs[0] > 0 else neon_pink)

            # text labels
            self.ax[i].text(0.01, 0.99, linear_text, transform=self.ax[i].transAxes, fontsize=10,
                            verticalalignment='top', color=neon_green if self.linear_slope > self.linear_slope_threshold else neon_pink)
            self.ax[i].text(0.01, 0.93, quad_text, transform=self.ax[i].transAxes, fontsize=10,
                            verticalalignment='top', color=neon_green if self.quad_coeffs[0] > 0 else neon_pink)

            # Neon green for x-axis
            self.ax[i].tick_params(axis='x', colors=neon_yellow)
            # Neon pink for y-axis
            self.ax[i].tick_params(axis='y', colors=neon_yellow)

            self.ax[i].set_title(
                f"Price Data for {self.securities[i].symbol}", color=neon_yellow)
            self.ax[i].set_xlabel("Time", color=neon_yellow)
            self.ax[i].set_ylabel("Price", color=neon_yellow)
            self.ax[i].grid(True, color='b', linestyle='--', linewidth=0.5)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # plt.title(f"Price Data for {self.security.symbol}")
        # plt.xlabel("Time")
        # plt.ylabel("Price")
        # plt.grid()
        # print("showing plot...")
        # plt.show(block=False)
        # print("done showing plot.")

    def linear_approximate(self):

        if len(self.price_queue) < 2:
            print("Not enough data to perform linear approximation.")
            return None

        # Perform a linear least squares fit (degree=1 for a straight line)
        # polyfit returns the coefficients of the polynomial, highest degree first.
        # For a linear fit (y = mx + b), it returns [m, b].
        coefficients = np.polyfit(
            self.time_queue[self.min_index:self.max_index],
            self.price_queue[self.min_index:self.max_index],
            1)
        self.linear_coeffs = coefficients

        # Extract the slope (m) and intercept (b)
        self.linear_slope = coefficients[0]
        b = coefficients[1]

        # print(f"Slope (m): {m}")
        # print(f"Intercept (b): {b}")

        # To get the predicted y values based on the fit:
        # y_predicted = m * np.array(self.time_queue) + b
        # fmt: off
        self.price_linear_approx = self.linear_slope * \
            np.array(self.time_queue[self.min_index:self.max_index]) + b
        # fmt: on
        # print(f"Predicted y values: {y_predicted}")

        return coefficients

    def second_order_approximate(self):
        if len(self.price_queue) < 3:
            print("Not enough data to perform second-order approximation.")
            return None

        # Perform a polynomial fit of degree 2 (quadratic)
        coefficients = np.polyfit(
            self.time_queue[self.min_index:self.max_index],
            self.price_queue[self.min_index:self.max_index],
            2)
        self.quad_coeffs = coefficients

        # Extract the coefficients
        a, b, c = coefficients

        # To get the predicted y values based on the fit:
        # fmt: off
        self.price_2nd_order_approx = a * \
            np.array(self.time_queue[self.min_index:self.max_index])**2 + \
            b * np.array(self.time_queue[self.min_index:self.max_index]) + c
        # fmt: on

        return coefficients

    def add_data(self, time_point, price_point, plot_data=False):
        self.time_queue.append(time_point)
        self.price_queue.append(price_point)
        self.index_count = min(self.max_analysis_samples, self.index_count + 1)
        # fmt: off
        self.min_index = self.min_index + 1 \
        if self.index_count >= self.max_analysis_samples else 0
        # fmt: on
        self.max_index += 1

        if self.linear_approximate() is None or self.second_order_approximate() is None:
            return

        # print("plotting data..." if plot_data else "Plotting is disabled.")
        if plot_data and self.plot_count % 1 == 0:
            self.plot_data()

        self.plot_count += 1


load_dotenv()  # Loads variables from .env

ALPACA_API_KEY = os.environ.get("ALPACA_API_KEY")
ALPACA_API_SECRET_KEY = os.environ.get("ALPACA_API_SECRET_KEY")

print("API Key:", ALPACA_API_KEY)
print("API Key:", ALPACA_API_SECRET_KEY)


holdings = [
    Security("TSLA", "Tesla Inc"),
    Security("TSLQ", "ProShares UltraShort Tesla"),


]

headers = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_API_SECRET_KEY
}


SIMULATE = True
# Example usage
if __name__ == "__main__":
    securities = holdings
    analyzer = Analyzer(
        securities, max_analyis_samples=30 if SIMULATE else 5*60)
    print(analyzer)

    i = 0
    while (True):

        if SIMULATE:
            analyzer.add_data(i, np.sin(i * 0.1) +
                              np.random.normal(0, 0.1), plot_data=True)
        else:
            response = requests.get(security.url, headers=headers)
            data = response.json()
            last_price = data["trade"]["p"]
            timestamp = data["trade"]["t"]
            analyzer.add_data(i, last_price, plot_data=True)

        # print("sleeping for 0.1 seconds to simulate real-time data...")
        # Simulate time delay for real-time data
        time.sleep(.1 if SIMULATE else 1)
        i += 1
