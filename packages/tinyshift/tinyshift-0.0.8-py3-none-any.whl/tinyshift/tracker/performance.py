import numpy as np
from sklearn.metrics import f1_score
import pandas as pd
from .base import BaseModel
from typing import Callable, Tuple, Union


class PerformanceTracker(BaseModel):
    def __init__(
        self,
        reference: pd.DataFrame,
        target_col: str,
        prediction_col: str,
        datetime_col: str,
        period: str,
        metric_score: Callable = f1_score,
        statistic: Callable = np.mean,
        confidence_level: float = 0.997,
        n_resamples: int = 1000,
        random_state: int = 42,
        drift_limit: Union[str, Tuple[float, float]] = "stddev",
        confidence_interval: bool = False,
    ):
        """
        Initialize a tracker for monitoring model performance over time using a specified evaluation metric.
        The tracker compares the performance metric across time periods to a reference distribution
        and identifies potential performance degradation.

        Parameters:
        ----------
        reference : pd.DataFrame
            The reference dataset used to compute the baseline metric distribution.
        target_col : str
            The name of the column containing the actual target values.
        prediction_col : str
            The name of the column containing the predicted values.
        datetime_col : str
            The name of the column containing datetime values for temporal grouping.
        period : str
            The frequency for grouping data (e.g., 'W' for weekly, 'M' for monthly).
        metric_score : Callable, optional
            The function to compute the evaluation metric (e.g., `f1_score`).
            Default is `f1_score`.
        statistic : Callable, optional
            The statistic function used to summarize the reference metric distribution.
            Default is `np.mean`.
        confidence_level : float, optional
            The confidence level for calculating statistical thresholds.
            Default is 0.997.
        n_resamples : int, optional
            Number of resamples for bootstrapping when calculating statistics.
            Default is 1000.
        random_state : int, optional
            Seed for reproducibility of random resampling.
            Default is 42.
        drift_limit : Union[str, Tuple[float, float]], optional
            The method or thresholds for drift detection. If "stddev", thresholds are based on standard deviation.
            If a tuple, it specifies custom lower and upper thresholds.
            Default is "stddev".
        confidence_interval : bool, optional
            Whether to calculate confidence intervals for the metric distribution.
            Default is False.

        Attributes:
        ----------
        period : str
            The grouping frequency used for analysis.
        metric_score : Callable
            The evaluation metric function used for tracking performance.
        reference_distribution : pd.DataFrame
            The performance metric distribution of the reference dataset.
        """

        self._validate_params(
            confidence_level,
            n_resamples,
            period,
        )
        self._validate_columns(
            reference,
            target_col,
            datetime_col,
        )

        if not callable(metric_score):
            raise TypeError("metric_score must be a callable function.")

        self.period = period
        self.metric_score = metric_score

        # Initialize distributions and statistics
        self.reference_distribution = self._calculate_metric(
            reference,
            target_col,
            prediction_col,
            datetime_col,
        )
        super().__init__(
            self.reference_distribution,
            confidence_level,
            statistic,
            n_resamples,
            random_state,
            drift_limit,
            confidence_interval,
        )

    def _calculate_metric(
        self,
        df: pd.DataFrame,
        target_col: str,
        prediction_col: str,
        datetime_col: str,
    ):
        """
        Calculate the performance metric for each time period in the dataset.

        Parameters:
        ----------
        df : DataFrame
            The dataset containing the data to analyze.
        target_col : str
            The name of the column containing the actual target values.
        prediction_col : str
            The name of the column containing the predicted values.
        datetime_col : str
            The name of the datetime column for temporal grouping.

        Returns:
        -------
        DataFrame
            A DataFrame with the calculated metric for each time period.
        """
        if target_col not in df.columns or prediction_col not in df.columns:
            raise KeyError(
                f"Columns {target_col} and/or {prediction_col} are not in the DataFrame."
            )
        if datetime_col not in df.columns:
            raise KeyError(f"Datetime column {datetime_col} is not in the DataFrame.")
        if not pd.api.types.is_datetime64_any_dtype(df[datetime_col]):
            raise TypeError(f"Column {datetime_col} must be of datetime type.")

        grouped = df.groupby(pd.Grouper(key=datetime_col, freq=self.period)).apply(
            lambda x: self.metric_score(x[target_col], x[prediction_col])
        )
        return grouped.reset_index(name="metric")

    def score(
        self,
        analysis: pd.DataFrame,
        target_col: str,
        prediction_col: str,
        datetime_col: str,
    ):
        """
        Assess model performance over time by calculating the evaluation metric
        for each time period and comparing it to the reference distribution.

        Parameters:
        ----------
        analysis : DataFrame
            The dataset to analyze for performance drift.
        target_col : str
            The name of the column containing the actual target values.
        prediction_col : str
            The name of the column containing the predicted values.
        datetime_col : str
            The name of the datetime column for temporal grouping.

        Returns:
        -------
        DataFrame
            A DataFrame containing datetime values, calculated metrics, and a boolean
            indicating whether performance drift was detected for each time period.
        """

        self._validate_columns(analysis, target_col, datetime_col)

        if analysis.empty:
            raise ValueError("Input DataFrame is empty.")

        metrics = self._calculate_metric(
            analysis, target_col, prediction_col, datetime_col
        )
        metrics["is_drifted"] = self._is_drifted(metrics)
        return metrics
