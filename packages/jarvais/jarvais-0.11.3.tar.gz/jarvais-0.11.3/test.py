from jarvais import Analyzer
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "faysalmiah1721758/breast-cancer-data",
        'breast-cancer-data.csv',
    )

analyzer = Analyzer(data=df, output_dir='BRUH', target_variable='class')

analyzer.run()