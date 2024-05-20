import pandas as pd

# read data from cluster data
df = pd.read_csv('cluster.csv')

# Define the number of samples you want for each cluster
n_samples = 10

# Sample n_samples rows for each unique value in the 'Cluster' column
sampled_df = df.groupby('Cluster', group_keys=False).apply(
    lambda x: x.sample(min(len(x), n_samples))
)

sampled_df['answer'].to_csv('testing_list.csv', index=False, header=False)
