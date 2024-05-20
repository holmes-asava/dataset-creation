import csv
import json
file_name = 'result'
with open(f'{file_name}.jsonl', "r") as file:
    data = [json.loads(line) for line in file]

# Open the CSV file

with open(f'{file_name}'.csv, 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(['Answer', 'Topic and Sentiment'])

    # Loop through each dictionary in the list
    for item in data:
        # Get the content of the third message
        content = item['messages'][2]['content']
        # Parse the content as JSO

        # Loop through each key-value pair in the content
        # Write the key-value pair to the CSV file
        writer.writerow([item['messages'][1]['content'], content])
