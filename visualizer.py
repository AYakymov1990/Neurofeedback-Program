import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class RealTimeVisualizer:
    def __init__(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        plt.style.use("fivethirtyeight")

        # Strumień EEG
        self.ax1.set_title("Strumień EEG na żywo")
        self.ax1.set_ylabel("Amplituda (uV)")
        self.eeg_line = None  # zostanie zainicjalizowane przy pierwszej aktualizacji

        # Słupki stanu mentalnego
        self.ax2.set_title("Stan Mentalny")
        self.ax2.set_xlim(0, 1)
        self.ax2.set_yticks([1, 2])
        self.ax2.set_yticklabels(["Relaksacja", "Koncentracja"])
        self.relaxation_bar = self.ax2.barh(1, 0, color="blue")
        self.concentration_bar = self.ax2.barh(2, 0, color="red")

    def update_plot(self, frame_data):
        if not isinstance(frame_data, dict):
            return

        # Aktualizacja linii EEG (jeden kanał)
        eeg = frame_data.get("eeg")
        if eeg is not None:
            x = list(range(len(eeg)))
            if self.eeg_line is None:
                (self.eeg_line,) = self.ax1.plot(x, eeg, linewidth=1.0, color="black")
            else:
                self.eeg_line.set_data(x, eeg)
            # Auto‑skalowanie osi Y z niewielkim marginesem
            ymin = float(min(eeg)) if len(eeg) else -1.0
            ymax = float(max(eeg)) if len(eeg) else 1.0
            if ymin == ymax:
                ymax = ymin + 1.0
            pad = 0.1 * (ymax - ymin)
            self.ax1.set_xlim(0, max(1, len(x) - 1))
            self.ax1.set_ylim(ymin - pad, ymax + pad)

        # Aktualizacja słupków stanu
        def _clamp01(v):
            if v is None:
                return 0.0
            try:
                return max(0.0, min(1.0, float(v)))
            except Exception:
                return 0.0

        relaxation = _clamp01(frame_data.get("relaxation"))
        concentration = _clamp01(frame_data.get("concentration"))
        self.relaxation_bar[0].set_width(relaxation)
        self.concentration_bar[0].set_width(concentration)

        # Przerysowanie
        self.fig.canvas.draw_idle()

    def start(self, update_function):
        self.ani = FuncAnimation(self.fig, update_function, interval=500, cache_frame_data=False)
        plt.tight_layout()
        plt.show()


