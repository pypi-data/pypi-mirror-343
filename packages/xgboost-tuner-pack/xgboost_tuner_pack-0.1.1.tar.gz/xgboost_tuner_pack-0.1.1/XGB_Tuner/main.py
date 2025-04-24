"""
tuner.py
--------
A robust hyperparameter tuner for XGBoost models.
Supports both grid search and randomized search methods using scikit-learn's tools.
"""

import logging
import warnings
from typing import Any, Dict, Optional, Union

import numpy as np
from xgboost import XGBClassifier, XGBRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.utils.validation import check_array, check_consistent_length

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Optionally, you can filter out XGBoost warnings by uncommenting the following line:
# warnings.filterwarnings("ignore", category=UserWarning, module="xgboost")

# Define type for parameter grid
ParamGridType = Dict[str, Union[list, tuple]]


class XGBTuner:
    """
    Hyperparameter tuner for XGBoost models supporting both classification and regression objectives.
    
    Attributes
    ----------
    best_params_ : dict
        Best parameter configuration after tuning.
    best_score_ : float
        The best score achieved during cross-validation.
    best_estimator_ : XGBClassifier or XGBRegressor
        The XGBoost model fitted with the best found parameters.
    
    Parameters
    ----------
    objective : str, default="classification"
        The type of problem ("classification" or "regression"). Case insensitive.
    search_method : str, default="grid"
        The search method to use; either "grid" for GridSearchCV or "random" for RandomizedSearchCV. Case insensitive.
    param_grid : dict, optional
        Custom parameter grid/distributions to search over. If None, a default grid is provided.
    n_iter : int, default=10
        Number of iterations to sample in randomized search (only used if search_method is "random").
    cv : int, default=5
        The number of folds in cross-validation.
    scoring : str or callable, default=None
        A string (as defined in scikit-learn documentation) or a scorer callable.
    random_state : int, default=42
        Random state for reproducibility.
    n_jobs : int, default=-1
        Number of jobs to run in parallel.
    """
    
    def __init__(
        self,
        objective: str = "classification",
        search_method: str = "grid",
        param_grid: Optional[ParamGridType] = None,
        n_iter: int = 10,
        cv: int = 5,
        scoring: Optional[Union[str, Any]] = None,
        random_state: int = 42,
        n_jobs: int = -1,
    ) -> None:
        self.objective = objective.lower()
        if self.objective not in {"classification", "regression"}:
            raise ValueError("Objective must be either 'classification' or 'regression'.")

        self.search_method = search_method.lower()
        if self.search_method not in {"grid", "random"}:
            raise ValueError("Search method must be either 'grid' or 'random'.")

        self.param_grid: ParamGridType = param_grid or {}
        self.n_iter = n_iter
        self.cv = cv
        self.scoring = scoring
        self.random_state = random_state
        self.n_jobs = n_jobs

        # Internal attributes
        self._model: Optional[Union[XGBClassifier, XGBRegressor]] = None
        self._searcher: Optional[Union[GridSearchCV, RandomizedSearchCV]] = None

        self.best_params_: Optional[Dict[str, Any]] = None
        self.best_score_: Optional[float] = None
        self.best_estimator_: Optional[Union[XGBClassifier, XGBRegressor]] = None

        self._create_default_param_grid()

    def _create_default_param_grid(self) -> None:
        """Assign a default parameter grid if none was provided."""
        if self.param_grid:
            logger.debug("Custom parameter grid provided.")
            return

        logger.info("No parameter grid provided. Using default hyperparameter grid.")
        self.param_grid = {
            "n_estimators": [50, 100],
            "max_depth": [3, 6, 9],
            "learning_rate": [0.01, 0.1],
            "subsample": [0.8, 1.0],
            "colsample_bytree": [0.8, 1.0],
        }

    def _init_model(self) -> None:
        """Instantiate the XGBoost model based on the objective."""
        if self.objective == "classification":
            # Removed "use_label_encoder" to avoid deprecation warnings.
            self._model = XGBClassifier(random_state=self.random_state, eval_metric="logloss")
        elif self.objective == "regression":
            self._model = XGBRegressor(random_state=self.random_state)
        else:
            raise ValueError("Unsupported objective type provided.")
        logger.info("Initialized XGBoost model for %s.", self.objective)

    def tune(self, X: Union[np.ndarray, list], y: Union[np.ndarray, list]) -> "XGBTuner":
        """
        Perform hyperparameter tuning on the provided data.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix.
        y : array-like, shape (n_samples,)
            Target vector.
        
        Returns
        -------
        self : instance of XGBTuner.
        
        Raises
        ------
        ValueError
            If X and y are not valid or have inconsistent lengths.
        RuntimeError
            If tuning fails.
        """
        try:
            X = check_array(X)
            y = np.array(y)
            check_consistent_length(X, y)
        except Exception as e:
            logger.error("Input validation error: %s", str(e))
            raise ValueError("Invalid input data. Ensure X and y are array-like with consistent lengths.") from e

        self._init_model()

        if self.search_method == "grid":
            self._searcher = GridSearchCV(
                estimator=self._model,
                param_grid=self.param_grid,
                cv=self.cv,
                scoring=self.scoring,
                n_jobs=self.n_jobs,
                verbose=1,
            )
        elif self.search_method == "random":
            self._searcher = RandomizedSearchCV(
                estimator=self._model,
                param_distributions=self.param_grid,
                n_iter=self.n_iter,
                cv=self.cv,
                scoring=self.scoring,
                random_state=self.random_state,
                n_jobs=self.n_jobs,
                verbose=1,
            )
        else:
            raise ValueError("Invalid search method.")

        logger.info("Starting hyperparameter tuning using %s search...", self.search_method)
        try:
            self._searcher.fit(X, y)
        except Exception as e:
            logger.error("Tuning failed: %s", str(e))
            raise RuntimeError("Hyperparameter tuning failed.") from e

        self.best_params_ = self._searcher.best_params_
        self.best_score_ = self._searcher.best_score_
        self.best_estimator_ = self._searcher.best_estimator_

        logger.info("Tuning completed. Best score: %s", self.best_score_)
        return self

    def predict(self, X: Union[np.ndarray, list]) -> np.ndarray:
        """
        Predict target values using the tuned model.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Data for prediction.
        
        Returns
        -------
        y_pred : numpy.ndarray
            Predicted values.
        
        Raises
        ------
        RuntimeError
            If tuning has not been run.
        """
        if self.best_estimator_ is None:
            logger.error("Prediction attempted before tuning.")
            raise RuntimeError("No best estimator found. Call `tune` first.")
        X_checked = check_array(X)
        return self.best_estimator_.predict(X_checked)

    def predict_proba(self, X: Union[np.ndarray, list]) -> np.ndarray:
        """
        Predict class probabilities (only for classification).
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Data for probability prediction.
        
        Returns
        -------
        y_proba : numpy.ndarray
            Predicted class probabilities.
        
        Raises
        ------
        RuntimeError
            If tuning has not been run.
        ValueError
            If the model is not built for classification.
        """
        if self.best_estimator_ is None:
            logger.error("Probability prediction attempted before tuning.")
            raise RuntimeError("No best estimator found. Call `tune` first.")
        if self.objective != "classification":
            logger.error("predict_proba called on a non-classification objective.")
            raise ValueError("predict_proba is only available for classification.")
        X_checked = check_array(X)
        return self.best_estimator_.predict_proba(X_checked)
