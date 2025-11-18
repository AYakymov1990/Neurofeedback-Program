from data_generator import EEGGenerator
from signal_processor import SignalProcessor
from mental_state_analyzer import MentalStateAnalyzer
from visualizer import RealTimeVisualizer


# Inicjalizacja
generator = EEGGenerator()
processor = SignalProcessor(generator.sampling_rate)
analyzer = MentalStateAnalyzer()
visualizer = RealTimeVisualizer()


def update(frame):
    # 1. Pobranie danych (co najmniej 1 s bufora)
    required = max(256, generator.sampling_rate)
    data = generator.get_data(required)
    if data is None or data.shape[1] < required:
        return

    # 2. Filtrowanie i moce pasm
    processor.filter_signal(data, generator.eeg_channels)
    band_powers = processor.get_band_powers(data, generator.eeg_channels)

    # 3. Analiza stanu
    relaxation, concentration = analyzer.analyze(band_powers)
    print(f"Relaksacja: {relaxation:.2f}, Koncentracja: {concentration:.2f}")

    # 4. Aktualizacja wizualizacji (logika w update_plot)
    # Przekazujemy ostatni wycinek EEG i metryki
    try:
        last_eeg = data[generator.eeg_channels[0], :]
    except Exception:
        last_eeg = None
    frame_payload = {
        "eeg": last_eeg,
        "relaxation": relaxation,
        "concentration": concentration,
    }
    visualizer.update_plot(frame_payload)

    # 5. Prosty feedback
    if relaxation > 0.6:
        visualizer.fig.set_facecolor("lightblue")
    else:
        visualizer.fig.set_facecolor("white")


if __name__ == "__main__":
    # Uruchomienie
    generator.start_stream()
    try:
        visualizer.start(update)
    finally:
        # Zakończenie
        generator.stop_stream()
        analyzer.release()


