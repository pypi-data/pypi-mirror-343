from jarvais import TrainerSupervised
import pandas as pd

df = pd.read_csv('data/a2rData_train_ED.csv')

trainer = TrainerSupervised(task='binary', output_dir='BRUHTEST')

trainer.run(data=df, target_variable='target_ED_visit', k_folds=2)