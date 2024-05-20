import csv
import json
import os
import random
import re

from openai import OpenAI

# Open the CSV file
answer_path = "input_data/answer_list.csv"
topics_list_path = "input_data/predefined_topics_v1.txt"
result_path = "output.jsonl"

with open("topics_list.txt", "r") as file:
    topics = json.load(file)
os.environ["OPENAI_API_KEY"] = ("sk-test-...")
client = OpenAI()


def get_result_from_openai(feedback: str, data: list) -> None:
    selected_topics = random.sample(topics, 10)
    messages = [
        {
            "role": "system",
            "content": "You are a language model trained to parse, analyze, and understand text. Your capabilities include sentiment analysis and topic modeling. You're tasked with interpreting a set of customer feedback comments, group them into topics and assessing the general sentiment (positive, neutral, negative) of available topic with following json,{'topic1':'sentiment2','topic2':'sentiment2'}"
        },
        {
            "role": "user",
            "content": f"Available topics: {selected_topics}. Customer feedback: {feedback}",
        },
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo-0125", messages=messages)
    content = response.choices[0].message.content
    # Replace parentheses with curly braces
    content = re.sub(r"\(", "{", content)
    content = re.sub(r"\)", "}", content)
    messages.append({"role": "assistant", "content": content})
    data.append({"messages": messages})


def replace_instruction(messages: list):
    messages = messages['messages']
    messages[0]['content'] = 'you are simplesat bot'
    return {'messages': messages}


data = []
with open(answer_path, 'r') as file:
    reader = csv.reader(file)
    round_per_feedback = 10
    # Loop through each row in the file
    for row in reader:
        feedback = row[0]
        for num in range(round_per_feedback):
            get_result_from_openai(feedback, data)


data = list(map(replace_instruction, data))
with open(result_path, "w") as file:
    for line in data:
        json.dump(line, file)
        file.write("\n")
