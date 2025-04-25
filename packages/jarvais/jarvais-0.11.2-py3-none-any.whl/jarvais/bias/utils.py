import re
import inspect
from functools import partial

import pandas as pd
import fairlearn as fm

def infer_sensitive_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Infers potentially sensitive features from a DataFrame.
    """
    sensitive_keywords = [
        "gender", "sex", "age", "race", "ethnicity", "income",
        "religion", "disability", "nationality", "language",
        "marital", "citizen", "veteran", "status", "orientation",
        "disease", "regimen", "disease_site"
    ]

    sensitive_features = {
        col for col in data.columns 
        if any(re.search(rf"\b{keyword}\b", col, re.IGNORECASE) for keyword in sensitive_keywords)
    }

    return data[sensitive_features]

def _get_metric(metric, sensitive_features=None):
    fn = getattr(fm, metric)
    params = inspect.signature(fn).parameters
    return partial(fn, sensitive_features=sensitive_features) if 'sensitive_features' in params and sensitive_features else fn
