from pathlib import Path

import pandas as pd
import numpy as np

from tabulate import tabulate

from sklearn.metrics import log_loss

from .subgroup_analysis import subgroup_analysis_fairlearn, subgroup_analysis_OLS
from ..utils import plot_violin

class ModelAuditor():
    """
    A class for explaining and analyzing bias in a predictive model's outcomes based on sensitive features.
    """
    def __init__(
            self, 
            y_true: pd.Series, 
            y_pred: np.ndarray, 
            sensitive_features: pd.DataFrame, 
            task: str,
            output_dir: Path,
            **kwargs: dict
        ) -> None:
        self.y_true = y_true
        self.y_pred = y_pred
        self.sensitive_features = sensitive_features
        self.task = task
        self.output_dir = output_dir
        self.mapper = {"mean_prediction": "Demographic Parity",
                       "false_positive_rate": "(FPR) Equalized Odds",
                       "true_positive_rate": "(TPR) Equalized Odds or Equal Opportunity"}
        self.kwargs = kwargs
    
    def run(
            self, 
            relative: bool = False, 
            fairness_threshold: float = 1.2
        ) -> None:
        """
        Runs the bias explainer analysis on the provided data. It first evaluates the potential bias in the model's predictions
        using the OLS regression F-statistic p-value. If the p-value is below the threshold of 0.05, indicating 
        potential bias in the sensitive feature, the method proceeds to generate visualizations and calculate fairness metrics.

        Args:
            relative (bool): 
                If True, the metrics will be presented relative to the most frequent value of each sensitive feature.
            fairness_threshold (float): 
                A threshold for determining fairness based on relative metrics. If the relative metric exceeds this threshold, 
                a warning flag will be applied.
        """
        if self.task == 'binary':
            y_true_array = self.y_true.to_numpy()
            bias_metric = np.array([
                log_loss([y_true_array[idx]], [self.y_pred[idx]], labels=np.unique(y_true_array))
                for idx in range(len(y_true_array))
            ])
            self.y_pred = (self.y_pred >= .5).astype(int)
        elif self.task == 'regression':
            bias_metric = np.sqrt((self.y_true.to_numpy() - self.y_pred) ** 2)

        self.results = []
        for sensitive_feature in self.sensitive_features.columns:
            _, f_pvalue = subgroup_analysis_OLS(sensitive_feature, bias_metric, self.output_dir)
            if f_pvalue < 0.05:
                plot_violin(sensitive_feature, bias_metric, self.output_dir, show_figure=True)
                result = subgroup_analysis_fairlearn(sensitive_feature, fairness_threshold, relative=relative)

                print(f"\n=== Subgroup Analysis for '{sensitive_feature.title()}' using FairLearn ===\n")
                table_output = tabulate(result.iloc[:, :4], headers='keys', tablefmt='grid')
                print('\n'.join(['    ' + line for line in table_output.split('\n')]), '\n')

                result.to_csv(self.output_dir / f'{sensitive_feature}_fm_metrics.csv')
