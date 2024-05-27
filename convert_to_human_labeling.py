import json

import pandas as pd

df = pd.read_csv('output_data/test_mock_clustering_result.csv')


def convert_items_to_colums_values(topics_items,index,is_topic=True):
    try:
        topics,sentiment = topics_items[index]
        if is_topic:
            return topics
        return sentiment
    except:
        return None


df['topics'] = df['topics'].apply(json.loads)

# Convert dictionaries to lists of tuples
df['topics'] = df['topics'].apply(lambda d: list(d.items()))
df['topics_amount'] = df['topics'].apply(lambda x: len(x))
max_topics = df['topics_amount'].max()
# Create columns for each topic

for i in range(max_topics):
    df[f'topic_{i}'] = df['topics'].apply(lambda x: convert_items_to_colums_values(x,i))
    df[f'sentiment_{i}'] = df['topics'].apply(lambda x: convert_items_to_colums_values(x,i,is_topic=False))
df.drop(columns=['topics', 'topics_amount']).to_csv(
    'output_data/test_mock_clustering_result_2.csv', index=False
)
