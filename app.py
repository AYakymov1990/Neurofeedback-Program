import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

try:
    from brainflow.data_filter import DataFilter, FilterTypes
except Exception:
    DataFilter = None
    FilterTypes = None


BASE_DIR = Path(__file__).parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "eeg_data.csv"
DEFAULT_SAMPLING_RATE = 250

app = Flask(__name__)


def _generate_synthetic_dataset(
    duration_seconds: int = 10,
    sampling_rate: int = DEFAULT_SAMPLING_RATE,
    n_channels: int = 4,
) -> Tuple[pd.DataFrame, int]:
    """Tworzy niewielki syntetyczny zestaw EEG, aby interfejs działał bez pliku CSV."""
    t = np.arange(0, duration_seconds, 1.0 / sampling_rate)
    data = {}
    base_freqs = [8.0, 10.0, 12.0, 6.0]
    for idx in range(n_channels):
        freq = base_freqs[idx % len(base_freqs)]
        signal = 30 * np.sin(2 * np.pi * freq * t)  # alpha-like content
        signal += 5 * np.sin(2 * np.pi * 0.5 * t)  # slow drift
        noise = np.random.normal(0, 3.0, size=t.shape)
        data[f"Ch{idx + 1}"] = signal + noise
    df = pd.DataFrame(data)
    return df, sampling_rate


def _infer_sampling_rate(df: pd.DataFrame, fallback: int = DEFAULT_SAMPLING_RATE) -> int:
    time_cols = [c for c in df.columns if c.lower() in {"time", "timestamp"}]
    for col in time_cols:
        series = pd.to_numeric(df[col], errors="coerce")
        valid = series.dropna()
        if len(valid) > 1:
            diffs = np.diff(valid)
            diffs = diffs[diffs > 0]
            if len(diffs):
                median_diff = float(np.median(diffs))
                if median_diff > 0:
                    inferred = int(round(1.0 / median_diff))
                    return max(1, inferred)
    return fallback


def _select_channels(df: pd.DataFrame) -> List[str]:
    metadata = {"time", "timestamp", "marker", "sample", "id", "index"}
    numeric_cols = [
        col
        for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col]) and col.lower() not in metadata
    ]
    if numeric_cols:
        return numeric_cols
    return [c for c in df.columns if c.lower() not in metadata]


def _build_time_axis(df: pd.DataFrame, sampling_rate: int) -> np.ndarray:
    for col in ["time", "timestamp"]:
        if col in df.columns:
            series = pd.to_numeric(df[col], errors="coerce")
            if series.notna().sum() == len(df):
                return series.to_numpy()
    return np.arange(len(df)) / float(sampling_rate)


def _load_eeg_data() -> Tuple[pd.DataFrame, List[str], int, np.ndarray, bool, Path]:
    data_path_env = os.environ.get("EEG_FILE")
    data_path = Path(data_path_env) if data_path_env else DEFAULT_DATA_PATH

    if data_path.exists():
        df = pd.read_csv(data_path)
        synthetic = False
    else:
        df, sr = _generate_synthetic_dataset()
        data_path = data_path if data_path_env else DEFAULT_DATA_PATH
        synthetic = True
        sampling_rate = sr
        channels = _select_channels(df)
        time_axis = _build_time_axis(df, sampling_rate)
        return df, channels, sampling_rate, time_axis, synthetic, data_path

    sampling_rate = _infer_sampling_rate(df, DEFAULT_SAMPLING_RATE)
    channels = _select_channels(df)
    time_axis = _build_time_axis(df, sampling_rate)
    return df, channels, sampling_rate, time_axis, synthetic, data_path


DATAFRAME, CHANNELS, SAMPLING_RATE, TIME_VECTOR, USING_SYNTHETIC, DATA_PATH = _load_eeg_data()


def _coerce_int(value, default: int) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def _apply_filters(signal: np.ndarray, sampling_rate: int, use_filter: bool) -> np.ndarray:
    if not use_filter:
        return np.array(signal, dtype=float)

    filtered = np.array(signal, dtype=float)

    if DataFilter is not None and FilterTypes is not None:
        try:
            DataFilter.perform_bandstop(
                filtered,
                sampling_rate,
                58.0,
                62.0,
                4,
                FilterTypes.BUTTERWORTH.value,
                0,
            )
            DataFilter.perform_bandpass(
                filtered,
                sampling_rate,
                8.0,
                13.0,
                4,
                FilterTypes.BUTTERWORTH.value,
                0,
            )
            return filtered
        except Exception:
            # Fallback do prostego wygładzania, gdy BrainFlow jest niedostępny
            pass

    window = max(3, min(25, max(3, len(filtered) // 10)))
    kernel = np.ones(window) / window
    padded = np.pad(filtered, (window // 2, window - 1 - window // 2), mode="edge")
    smoothed = np.convolve(padded, kernel, mode="valid")
    return smoothed.astype(float)


@app.route("/")
def index():
    if not CHANNELS:
        return "Nie wykryto kanałów EEG w zbiorze danych.", 500

    total_samples = len(DATAFRAME)
    return render_template(
        "index.html",
        channels=CHANNELS,
        sampling_rate=SAMPLING_RATE,
        total_samples=total_samples,
        using_synthetic=USING_SYNTHETIC,
        data_path=str(DATA_PATH),
    )


@app.route("/data")
def data():
    if not CHANNELS:
        return jsonify({"error": "Brak dostępnych kanałów EEG"}), 500

    channel = request.args.get("channel", CHANNELS[0])
    if channel not in CHANNELS:
        return jsonify({"error": f"Nieznany kanał: {channel}"}), 400

    total_samples = len(DATAFRAME)
    default_end = min(total_samples, SAMPLING_RATE * 5)

    start = _coerce_int(request.args.get("start", 0), 0)
    end = _coerce_int(request.args.get("end", default_end), default_end)
    filtered = request.args.get("filtered", "false").lower() == "true"

    start = max(0, start)
    end = min(total_samples, max(start + 1, end))

    signal = DATAFRAME[channel].to_numpy()
    segment = signal[start:end]
    segment = _apply_filters(segment, SAMPLING_RATE, filtered)
    time_segment = TIME_VECTOR[start:end]

    return jsonify(
        {
            "channel": channel,
            "filtered": filtered,
            "time": time_segment.tolist(),
            "voltage": segment.tolist(),
            "start": start,
            "end": end,
            "sampling_rate": SAMPLING_RATE,
            "using_synthetic": USING_SYNTHETIC,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
