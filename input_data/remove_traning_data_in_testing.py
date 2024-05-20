import pandas as pd

train_df = pd.read_csv('traning_dataset.csv')
testing_df = pd.read_csv('testing_dataset.csv')
testing_list = testing_df.values.tolist()
train_list = train_df.values.tolist()

# Assuming 'testing_list' and 'train_list' are your lists
testing_list = [item for item in testing_list if item not in train_list]
pd.DataFrame(testing_list).to_csv('cleaned_testing_dataset.csv', index=False, header=False)
