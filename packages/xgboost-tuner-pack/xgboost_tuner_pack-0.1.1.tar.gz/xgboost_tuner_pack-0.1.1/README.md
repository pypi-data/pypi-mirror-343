# xgbtuner

[![PyPI version](https://img.shields.io/pypi/v/xgbtuner.svg)](https://pypi.org/project/xgbtuner)  
[![Python versions](https://img.shields.io/pypi/pyversions/xgbtuner.svg)]()  
[![License](https://img.shields.io/pypi/l/xgbtuner.svg)](LICENSE)

A **world-class**, **easy-to-use** hyperparameter tuner for XGBoost models, built on top of scikit-learn’s `GridSearchCV` and `RandomizedSearchCV`. Supports both **classification** and **regression** out of the box, with robust error handling, comprehensive testing, and flexible customization.

---

## 🚀 Features

- **Grid Search & Random Search**  
  Choose between exhaustive grid search or randomized search for hyperparameter exploration.
- **Classification & Regression**  
  One API for both objectives—simply set `objective="classification"` or `"regression"`.
- **Default & Custom Grids**  
  Sensible default parameter grid, plus ability to pass your own `param_grid`.
- **Robust Input Validation**  
  Checks for array-like inputs, consistent lengths, and raises clear errors.
- **Detailed Logging**  
  Built-in `logging` statements to trace tuning progress and errors.
- **Fully Tested**  
  Over 10 unit tests cover edge cases, custom grids, list inputs, invalid configs, and more.
- **Scikit-Learn Compatible**  
  Behaves like any estimator: `.tune()`, `.predict()`, and `.predict_proba()` for classification.

---

## 📦 Installation

Install from PyPI:

```bash
pip install xgbtuner
