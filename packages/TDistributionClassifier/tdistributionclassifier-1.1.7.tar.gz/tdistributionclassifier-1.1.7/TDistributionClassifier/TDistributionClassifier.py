# Made by : Abdul Mofique Siddiqui
import numpy as np
from scipy.stats import t, multivariate_t
from numpy.linalg import LinAlgError

class TDistributionClassifier:
    def __init__(self):
        self.class_stats = {}
        self.mode = None  # 'univariate' or 'multivariate'

    def fit(self, X, y):
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        self.mode = 'univariate' if X.shape[1] == 1 else 'multivariate'

        self.classes_ = np.unique(y)
        for c in self.classes_:
            Xc = X[y == c]
            mean = np.mean(Xc, axis=0)
            df = Xc.shape[0] - 1
            if self.mode == 'univariate':
                std = np.std(Xc, ddof=1)
                self.class_stats[c] = {"mean": mean[0], "std": std, "df": df}
            else:
                cov = np.cov(Xc.T, ddof=1)
                # Add regularization to avoid singular matrix
                cov += np.eye(cov.shape[0]) * 1e-6
                self.class_stats[c] = {"mean": mean, "cov": cov, "df": df}

    def _log_pdf_univariate(self, x, stats):
        t_score = (x - stats["mean"]) / stats["std"]
        log_pdf = t.logpdf(t_score, df=stats["df"]) - np.log(stats["std"])
        return log_pdf

    def _log_pdf_multivariate(self, x, stats):
        try:
            return multivariate_t.logpdf(x, loc=stats["mean"], shape=stats["cov"], df=stats["df"])
        except LinAlgError:
            return -np.inf  # Return very low prob if covariance is not invertible

    def predict_proba(self, X):
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)

        log_probs = []
        for x in X:
            class_log_probs = {}
            for c in self.classes_:
                stats = self.class_stats[c]
                if self.mode == 'univariate':
                    log_p = self._log_pdf_univariate(x[0], stats)
                else:
                    log_p = self._log_pdf_multivariate(x, stats)
                class_log_probs[c] = log_p

            # Log-sum-exp trick for numerical stability
            max_log = max(class_log_probs.values())
            exp_shifted = {k: np.exp(v - max_log) for k, v in class_log_probs.items()}
            total = sum(exp_shifted.values()) + 1e-10
            probs = {k: v / total for k, v in exp_shifted.items()}
            log_probs.append((probs[0], probs[1]))
        return np.array(log_probs)

    def predict(self, X):
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)


# Made by : Abdul Mofique Siddiqui