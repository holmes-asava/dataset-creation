import csv
import json
import os
import random
import re

from openai import OpenAI

# Open the CSV file

topics_list_path = "input_data/predefined_topics_v1.txt"
testing_dataset_2 = "batch-testing/200_sample_testing_batch.jsonl"
with open(topics_list_path, "r") as file:
    topics_list = json.load(file)
topics_list = list(map(lambda x: x.lower(), topics_list))
os.environ["OPENAI_API_KEY"] = (
    "sk-test..."
)
client = OpenAI()


not_json_error_count = 0
new_topics = []
new_topics_count = 0
temperature = 0.2
model = "ft:gpt-3.5-turbo-0125:simplesat:predefine-topic-1:9PScBfqR"


def get_result_from_openai(
    feedback: str,
    data: list,
    new_topics_count,
    not_json_error_count,
    new_topics,
    model=model,
    temperature=temperature,
) -> None:
    messages = [
        {"role": "system", "content": "you are simplesat bot"},
        {
            "role": "user",
            "content": f"Available topics: {topics_list}.{feedback}",
        },
    ]
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature
    )
    content = response.choices[0].message.content
    content = content.replace("'", '"')
    messages.append({"role": "assistant", "content": content})

    data.append({"messages": messages})
    try:
        result_json = json.loads(content)
        keys_not_in_list = [key for key in result_json.keys() if key.lower() not in topics_list]

        if keys_not_in_list:
            for key in keys_not_in_list:
                if key not in new_topics:
                    new_topics.append(key)
                    new_topics_count += 1
    except json.JSONDecodeError:
        not_json_error_count += 1

    return error_count, 0, new_topics


with open(testing_dataset_2, 'r') as file:
    lines = [json.loads(line) for line in file]
    data = []
    for row in lines:
        feedback = row['body']['messages'][1]['content']
        error_count, not_json_error_count, new_topics = get_result_from_openai(
            feedback, data, new_topics_count, not_json_error_count, new_topics
        )


with open(f"exp4_testing_output_with_{error_count}_new_topics_{temperature}.jsonl", "w") as file:
    for line in data:
        json.dump(line, file)
        file.write("\n")

with open(f'exp4_testing_result_detail_{temperature}.txt', 'w') as file:
    file.write(f"temperature: {temperature}\n")
    file.write(f"model: {model}\n")
    file.write(f"error_count: {error_count}\n")
    file.write(f"not_json_error_count: {not_json_error_count}\n")
    file.write(f"new_topics: {new_topics}\n")
