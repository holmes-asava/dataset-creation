# csv format for the dataset
# custom_id / text / cluster num
# 1_company-29853_session-9108360_question-76999 / text1 / 1
# 2_company-29853_session-9108360_question--76999 / text2 / 2
# 3_company-29853_session-9108360_question--80000 / text3 / 1
# 4_company-29853_session-9108360_question--80001 /  / 3

import json
import os

import pandas as pd
from openai import OpenAI

# Open the CSV file
input_path = 'input_data/mock_clustering_result.csv'
output_path = 'output_data/test_mock_clustering_result.csv'
topics_list_path = "input_data/predefined_topics_v1.txt"

os.environ["OPENAI_API_KEY"] = "sk-proj-..."
client = OpenAI()


with open(topics_list_path, "r") as file:
    topics = json.load(file)


def generate_topics_by_openai(feedback: str) -> json:
    messages = [
        {
            "role": "system",
            "content": "You are a language model trained to parse, analyze, and understand text. Your capabilities include sentiment analysis and topic modeling. You're tasked with interpreting a set of customer feedback comments, group them into topics and assessing the general sentiment (positive, neutral, negative) of "
            + f'{topics}'
            + " with following json,{'topic1':'sentiment2','topic2':'sentiment2'} {}. Do not create new topics. return as {} if find any issues",
        },
        {
            "role": "user",
            "content": f"Customer feedback: {feedback}",
        },
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo-0125", messages=messages)
    content = response.choices[0].message.content
    return content

csv = pd.read_csv(input_path)
csv['company'] = (
    csv['custom_id'].apply(lambda x: x.split('_')[1]).apply(lambda x: x.split('-')[-1])
)
csv['session'] = (
    csv['custom_id'].apply(lambda x: x.split('_')[2]).apply(lambda x: x.split('-')[-1])
)
csv['question'] = (
    csv['custom_id'].apply(lambda x: x.split('_')[3]).apply(lambda x: x.split('-')[-1])
)
csv['custom_id'] = csv['custom_id'].apply(lambda x: x.split('_')[0])
# Get the unique cluster numbers
clusters = csv['cluster_num'].unique()
prepared_dataset = pd.DataFrame(columns=[ 'text','topics'])

for cluster in clusters:
    # target sampling size
    target_size = 70
    current_size = 0
    # sampling data from each cluster
    cluster_data = csv[csv['cluster_num'] == cluster]
    # how to shuffle the data
    cluster_data = cluster_data.sample(frac=1).reset_index(drop=True)

    for _, row in cluster_data.iterrows():
        answer_df = csv[(csv['question'] == row['question']) & (csv['session'] == row['session'])].sort_values('custom_id')
        answer_text = ''.join(answer_df['text'])

        # check add answer_text if answer not in prepared_dataset
        if answer_text not in prepared_dataset['text'].values:

            topics = generate_topics_by_openai(answer_text)
            new_row = pd.DataFrame({'text': [answer_text], 'topics': topics})

            prepared_dataset = pd.concat([prepared_dataset, new_row], ignore_index=True)
            current_size += 1
        if current_size >= target_size:
            break

print(prepared_dataset)
