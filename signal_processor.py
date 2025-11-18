from brainflow.data_filter import DataFilter, FilterTypes


class SignalProcessor:
    def __init__(self, sampling_rate: int):
        self.sampling_rate = sampling_rate

    def filter_signal(self, data, eeg_channels) -> None:
        for channel in eeg_channels:
            # Usuwanie szumu sieciowego 60 Hz
            DataFilter.perform_bandstop(
                data[channel],
                self.sampling_rate,
                58.0,  # częstotliwość początkowa
                62.0,  # częstotliwość końcowa
                4,
                FilterTypes.BUTTERWORTH.value,
                0,
            )
            # Filtr pasmowoprzepustowy dla pasma alfa (8–13 Hz)
            DataFilter.perform_bandpass(
                data[channel],
                self.sampling_rate,
                8.0,   # częstotliwość początkowa
                13.0,  # częstotliwość końcowa
                4,
                FilterTypes.BUTTERWORTH.value,
                0,
            )

    def get_band_powers(self, data, eeg_channels):
        # Zwraca (avg_band_powers, stddev_band_powers)
        return DataFilter.get_avg_band_powers(
            data, eeg_channels, self.sampling_rate, True
        )


