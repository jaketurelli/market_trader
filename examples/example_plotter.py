from example_local_webpage import LivePlotApp
import multiprocessing
import time
import numpy as np


class SinePlot(LivePlotApp):
    def background_data_updater(self):
        n = 0
        while True:
            x = self.latest_data["x"]
            self.latest_data["data"]['sin'] = np.sin(x + n * 0.1)
            n += 1
            time.sleep(1)


class CosinePlot(LivePlotApp):
    def background_data_updater(self):
        n = 0
        while True:
            x = self.latest_data["x"]
            self.latest_data["data"]['cos'] = np.cos(x + n * 0.1)
            n += 1
            time.sleep(1)


def run_plot(app, port):
    app.run(port=port)


if __name__ == "__main__":
    plot1 = SinePlot(title="Sine Plot")
    plot2 = CosinePlot(title="Cosine Plot")

    # Run each app on a different port in its own process
    p1 = multiprocessing.Process(target=run_plot, args=(plot1, 8150))
    p2 = multiprocessing.Process(target=run_plot, args=(plot2, 8151))
    p1.start()
    p2.start()

    # Keep main process alive
    p1.join()
    p2.join()
