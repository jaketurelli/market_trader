import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import threading
import time


class LivePlotApp:
    def __init__(self, title="Interactive Plot"):
        self.latest_data = {
            "x": np.linspace(0, 10, 100),
            "data": {},
        }
        self.app = dash.Dash(__name__)
        self.title = title
        self._setup_layout()
        self._setup_callback()
        threading.Thread(target=self.background_data_updater,
                         daemon=True).start()

    def background_data_updater(self):
        x = 1
        # n = 0
        # while True:
        #     x = np.linspace(0, 10, 100)
        #     y = np.sin(x + n * 0.1)
        #     y2 = np.cos(x + n * 0.1) + 2
        #     self.latest_data["x"] = x
        #     self.latest_data["y"] = y
        #     self.latest_data["y2"] = y2
        #     n += 1
        #     time.sleep(1)

    def _setup_layout(self):
        self.app.layout = html.Div([
            html.H1(self.title),
            dcc.Graph(id="sine"),
            dcc.Interval(id="interval", interval=1000, n_intervals=0)
        ])

    def _setup_callback(self):
        @self.app.callback(
            Output("sine", "figure"),
            Input("interval", "n_intervals")
        )
        def update_graph(n_intervals):
            x = self.latest_data["x"]
            to_graph = []
            for curr_data in self.latest_data["data"]:
                to_graph.append(
                    {"x": x, "y": self.latest_data["data"]
                        [curr_data], "type": "line", "name": curr_data}
                )
            return {
                "data": to_graph,
                "layout": {"title": "Sine and Cosine Waves"}
            }

    def run(self, host="0.0.0.0", port=8050, debug=True):
        self.app.run(host=host, port=port, debug=debug)


# Example usage:
if __name__ == "__main__":
    plot_app = LivePlotApp()
    plot_app.run()
