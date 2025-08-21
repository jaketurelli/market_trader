from collections import deque
import time
import numpy as np
# fmt: off
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.security_class import Security
# fmt: on


class Analyzer:
    def __init__(self, security: Security, max_analyis_samples=30):
        self.security = security
        self.price_queue = deque(maxlen=max_analyis_samples)
        self.time_queue = deque(maxlen=max_analyis_samples)
        
        self.price_linear_approx = None
        self.linear_coeffs = None
        self.linear_slope = 0
        self.linear_slope_threshold = 0
        
        self.price_2nd_order_approx = None
        self.quad_coeffs = None
        
        self.plot_count = 0
        

        import matplotlib.pyplot as plt

        plt.ion()  # Turn on interactive mode


        self.fig, self.ax = plt.subplots(figsize=(20, 10))
        # else:
        #     self.ax.cla()  # Clear the axes

        

    def __repr__(self):
        return f"Analyzer(symbol='{self.security.symbol}', name={self.security.name})"

    def __get_size_dataset(self):
        return len(self.queue)
    
    def plot_data(self):
        import matplotlib.pyplot as plt

        if not self.price_queue or not self.time_queue:
            print("No data to plot.")
            return

        self.ax.cla()  # Clear the axes
        
        self.ax.plot(self.time_queue, self.price_queue, marker='o', linestyle='-', color='b')
        self.ax.plot(self.time_queue, self.price_linear_approx, marker=None, linestyle='--', color='g' if self.linear_slope > self.linear_slope_threshold  else 'r')
        self.ax.plot(self.time_queue, self.price_2nd_order_approx, marker=None, linestyle=':', color='g' if self.quad_coeffs[0] > 0 else 'r')
        
        # Add coefficients as text on the plot
        linear_text = f"Linear: y = {self.linear_coeffs[0]:.3f}x + {self.linear_coeffs[1]:.3f}"
        quad_text = f"Quadratic: y = {self.quad_coeffs[0]:.3e}x² + {self.quad_coeffs[1]:.3f}x + {self.quad_coeffs[2]:.3f}"
        self.ax.text(0.01, 0.99, linear_text, transform=self.ax.transAxes, fontsize=10, verticalalignment='top', color='g' if self.linear_slope > self.linear_slope_threshold else 'r')
        self.ax.text(0.01, 0.93, quad_text, transform=self.ax.transAxes, fontsize=10, verticalalignment='top', color='g' if self.quad_coeffs[0] > 0 else 'r')

        self.ax.set_title(f"Price Data for {self.security.symbol}")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")
        self.ax.grid()

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
        coefficients = np.polyfit(self.time_queue, self.price_queue, 1)
        self.linear_coeffs = coefficients

        # Extract the slope (m) and intercept (b)
        self.linear_slope = coefficients[0]
        b = coefficients[1]

        # print(f"Slope (m): {m}")
        # print(f"Intercept (b): {b}")

        # To get the predicted y values based on the fit:
        # y_predicted = m * np.array(self.time_queue) + b
        self.price_linear_approx = self.linear_slope * np.array(self.time_queue) + b
        # print(f"Predicted y values: {y_predicted}")
        
        return coefficients
    def second_order_approximate(self): 
        if len(self.price_queue) < 3:
            print("Not enough data to perform second-order approximation.")
            return None
        

        # Perform a polynomial fit of degree 2 (quadratic)
        coefficients = np.polyfit(self.time_queue, self.price_queue, 2)
        self.quad_coeffs = coefficients

        # Extract the coefficients
        a, b, c = coefficients

        # To get the predicted y values based on the fit:
        self.price_2nd_order_approx = a * np.array(self.time_queue)**2 + b * np.array(self.time_queue) + c
        
        return coefficients
        
    def add_data(self, time_point, price_point, plot_data=False):
        self.time_queue.append(time_point)
        self.price_queue.append(price_point)
        
        if self.linear_approximate() is None or self.second_order_approximate() is None:
            return
        
        # print("plotting data..." if plot_data else "Plotting is disabled.")
        if plot_data and self.plot_count % 1 == 0:
            self.plot_data()
        
        self.plot_count += 1


# Example usage
if __name__ == "__main__":
    security = Security("TSLA", "Tesla Inc")
    analyzer = Analyzer(security)
    print(analyzer)
    
    for i in range(1000):
        analyzer.add_data(i, np.sin(i * 0.1) + np.random.normal(0, 0.1), plot_data=True)
        # print("sleeping for 0.1 seconds to simulate real-time data...")
        time.sleep(0.25)  # Simulate time delay for real-time data
