import numpy as np
from brainflow.ml_model import (
    MLModel,
    BrainFlowMetrics,
    BrainFlowClassifiers,
    BrainFlowModelParams,
)


class MentalStateAnalyzer:
    def __init__(self):
        # Próba wykrycia metryk w różnych wersjach BrainFlow
        self.relaxation_model = None
        self.concentration_model = None

        def _get_metric(name_candidates):
            for name in name_candidates:
                metric = getattr(BrainFlowMetrics, name, None)
                if metric is not None:
                    return metric.value
            return None

        relaxation_metric = _get_metric(
            ["RELAXATION", "MINDFULNESS", "MEDITATION", "CALM"]
        )
        concentration_metric = _get_metric(
            ["CONCENTRATION", "ATTENTION", "FOCUS"]
        )

        def _get_classifier(name_candidates):
            for name in name_candidates:
                clf = getattr(BrainFlowClassifiers, name, None)
                if clf is not None:
                    return clf.value
            return None

        classifier = _get_classifier(["REGRESSION", "DEFAULT_CLASSIFIER", "ONNX_CLASSIFIER"])

        if relaxation_metric is not None and classifier is not None:
            self.relaxation_params = BrainFlowModelParams(relaxation_metric, classifier)
            self.relaxation_model = MLModel(self.relaxation_params)
            self.relaxation_model.prepare()

        if concentration_metric is not None and classifier is not None:
            self.concentration_params = BrainFlowModelParams(concentration_metric, classifier)
            self.concentration_model = MLModel(self.concentration_params)
            self.concentration_model.prepare()

    def _heuristics(self, avg_bands):
        # avg_bands: [delta, theta, alpha, beta, (gamma?)] — zależy od BrainFlow
        delta = float(avg_bands[0]) if len(avg_bands) > 0 else 0.0
        theta = float(avg_bands[1]) if len(avg_bands) > 1 else 0.0
        alpha = float(avg_bands[2]) if len(avg_bands) > 2 else 0.0
        beta = float(avg_bands[3]) if len(avg_bands) > 3 else 0.0

        # Najprostsze znormalizowane wskaźniki
        # relaksacja ~ alpha / (alpha + beta + theta + 1e-9)
        denom_relax = alpha + beta + theta + 1e-9
        relaxation = alpha / denom_relax

        # koncentracja ~ beta / (beta + alpha + theta + 1e-9)
        denom_conc = beta + alpha + theta + 1e-9
        concentration = beta / denom_conc

        # Ograniczamy do [0,1]
        relaxation = max(0.0, min(1.0, relaxation))
        concentration = max(0.0, min(1.0, concentration))
        return relaxation, concentration

    def analyze(self, band_powers):
        # band_powers: (avg_band_powers, std_band_powers)
        avg_bands = band_powers[0] if isinstance(band_powers, (list, tuple)) else band_powers
        feature_vector = np.concatenate((band_powers[0], band_powers[1]))

        relaxation_score = None
        concentration_score = None

        if self.relaxation_model is not None:
            relaxation_score = float(self.relaxation_model.predict(feature_vector)[0])
        if self.concentration_model is not None:
            concentration_score = float(self.concentration_model.predict(feature_vector)[0])

        # Fallback do heurystyk, jeśli jeden/oba modele są niedostępne
        if relaxation_score is None or concentration_score is None:
            rel_h, conc_h = self._heuristics(avg_bands)
            if relaxation_score is None:
                relaxation_score = rel_h
            if concentration_score is None:
                concentration_score = conc_h

        return relaxation_score, concentration_score

    def release(self) -> None:
        if self.relaxation_model is not None:
            self.relaxation_model.release()
        if self.concentration_model is not None:
            self.concentration_model.release()


