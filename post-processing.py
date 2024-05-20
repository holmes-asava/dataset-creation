import json
import random
import json

topics_list_path = "input_data/predefined_topics_v1.txt"
output_path = "output.jsonl"
clean_dataset_path = "clean_output.jsonl"

with open(output_path, "r") as file:
    messages = [json.loads(line) for line in file]

# Assuming 'my_list' is your list of keys
with open(topics_list_path, "r") as file:
    topics_list = json.load(file)
topics_list = list(map(lambda x: x.lower(), topics_list))
error_count = 0
total_count = 0
error_message = []
new_topics = []
# Get a list of keys in json_dict that are not in my_list
for message in messages:
    result_json = message['messages'][2]['content']
    try:
        result_json = json.loads(result_json)
    except json.JSONDecodeError:
        # error_message.append(message)
        error_count += 1
        del message
        continue
    total_count += len(result_json.keys())
    keys_not_in_list = [key for key in result_json.keys() if key.lower() not in topics_list]
    if keys_not_in_list:
        for key in keys_not_in_list:
            if key not in new_topics:
                new_topics.append(key)
            error_count += 1
        del message


with open(clean_dataset_path, "w") as file:
    for line in messages:
        json.dump(line, file)
        file.write("\n")

# ---------------------------------------------------------------------------------------------------
# Train ans test split
# ---------------------------------------------------------------------------------------------------

# Define the split ratio
split_ratio = 0.8

# Read lines into a list
with open(clean_dataset_path, 'r') as f:
    lines = f.readlines()

# Shuffle the list
random.shuffle(lines)

# Determine the split index
split_index = int(len(lines) * split_ratio)

# Split the list
train_lines = lines[:split_index]
test_lines = lines[split_index:]

# Write the training set
with open('train.jsonl', 'w') as f:
    for line in train_lines:
        f.write(line)


# Write the testing set
with open('test.jsonl', 'w') as f:
    for line in test_lines:
        f.write(line)
# ---------------------------------------------------------------------------------------------------
