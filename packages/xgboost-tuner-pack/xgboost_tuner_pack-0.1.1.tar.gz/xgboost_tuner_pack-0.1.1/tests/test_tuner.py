"""
test_tuner.py
-------------
Extended unit tests for the XGBTuner class.
Tests include classification, regression, custom parameter grid, case-insensitive input,
list inputs, and invalid configurations.
"""

import pytest
import numpy as np
from sklearn.datasets import load_iris, fetch_california_housing
from XGB_Tuner import XGBTuner


# Fixtures for datasets
@pytest.fixture(scope="module")
def iris_data():
    data = load_iris()
    return data.data, data.target

@pytest.fixture(scope="module")
def housing_data():
    data = fetch_california_housing()
    return data.data, data.target


# Classification tests
def test_classification_tuning(iris_data):
    X, y = iris_data

    # Grid search
    tuner_grid = XGBTuner(objective="classification", search_method="grid", cv=3, n_jobs=1)
    tuner_grid.tune(X, y)
    assert tuner_grid.best_params_ is not None, "Expected best parameters for classification."
    assert tuner_grid.best_score_ is not None, "Expected best score for classification."
    preds = tuner_grid.predict(X[:5])
    assert len(preds) == 5, "Mismatch in number of predictions."

    # Random search
    tuner_random = XGBTuner(objective="classification", search_method="random", n_iter=5, cv=3, n_jobs=1)
    tuner_random.tune(X, y)
    assert tuner_random.best_params_ is not None, "Expected best parameters from random search."
    preds_proba = tuner_random.predict_proba(X[:5])
    assert preds_proba.shape[0] == 5, "Mismatch in probability prediction samples."
    assert preds_proba.shape[1] == len(set(y)), "Mismatch in number of classes."


# Regression tests
def test_regression_tuning(housing_data):
    X, y = housing_data

    tuner = XGBTuner(objective="regression", search_method="grid", cv=3, n_jobs=1)
    tuner.tune(X, y)
    assert tuner.best_params_ is not None, "Expected best parameters for regression."
    preds = tuner.predict(X[:5])
    assert len(preds) == 5, "Expected predictions for 5 samples."
    with pytest.raises(ValueError):
        tuner.predict_proba(X[:5])


# Tests for errors before tuning
def test_error_before_tuning(iris_data):
    X, _ = iris_data
    tuner = XGBTuner(objective="classification")
    with pytest.raises(RuntimeError):
        tuner.predict(X)
    with pytest.raises(RuntimeError):
        tuner.predict_proba(X)


# Test for invalid input types
def test_invalid_input():
    tuner = XGBTuner(objective="classification")
    with pytest.raises(ValueError):
        tuner.tune("invalid_input", "invalid_input")


# Test mismatched lengths between X and y
def test_mismatched_lengths(iris_data):
    X, y = iris_data
    # Remove one sample to create a mismatch.
    with pytest.raises(ValueError):
        X_mismatch = X[:-1]
        tuner = XGBTuner(objective="classification")
        tuner.tune(X_mismatch, y)


# Test that list inputs work as well as numpy arrays
def test_list_input_format(iris_data):
    X, y = iris_data
    X_list = X.tolist()
    y_list = y.tolist()
    tuner = XGBTuner(objective="classification")
    tuner.tune(X_list, y_list)
    preds = tuner.predict(X_list[:5])
    assert isinstance(preds, np.ndarray), "Predictions should be returned as a numpy array."


# Test custom parameter grid is respected
def test_custom_param_grid(iris_data):
    X, y = iris_data
    custom_grid = {
        "n_estimators": [10, 20],
        "max_depth": [2, 4],
    }
    tuner = XGBTuner(objective="classification", param_grid=custom_grid, cv=3, n_jobs=1)
    tuner.tune(X, y)
    for param in custom_grid:
        assert param in tuner.param_grid, f"Custom param '{param}' missing in tuner.param_grid."


# Test case-insensitive objective and search method with a small dataset
def test_case_insensitive_objective():
    # Use cv=2 to allow 4 samples (instead of default cv=5)
    tuner1 = XGBTuner(objective="RegresSion", search_method="RanDom", cv=2)
    X = [[1], [2], [3], [4]]
    y = [1, 2, 3, 4]
    tuner1.tune(X, y)
    preds = tuner1.predict(X)
    assert len(preds) == 4, "Expected predictions for 4 samples in case-insensitive test."


# Test invalid objective should raise ValueError
def test_invalid_objective():
    with pytest.raises(ValueError):
        XGBTuner(objective="clustering")  # Invalid objective


# Test invalid search method should raise ValueError
def test_invalid_search_method():
    with pytest.raises(ValueError):
        XGBTuner(objective="classification", search_method="bayesian")  # Invalid search method
