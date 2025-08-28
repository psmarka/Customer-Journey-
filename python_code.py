#Adding a title to this for demo purposes.
#Adding another line for merging purposes.

import csv
import openai

# Set your OpenAI API key here
openai.api_key = 'your-api-key-here'  # Replace with your actual OpenAI API key

# Function to generate a prompt for ChatGPT based on the comment and industry
def generate_prompt(comment, industry):
    return f"""
You are an expert in customer experience for the {industry} industry.
Analyze the following survey comment and tag it with the appropriate customer journey stage:
(Awareness, Consideration, Purchase, Retention, Advocacy)

Comment: "{comment}"

Respond with only the customer journey stage.
"""

# Define input and output file paths
input_file = 'survey_comments.csv'       # Input CSV file containing survey comments
output_file = 'tagged_comments.csv'      # Output CSV file to store tagged results

# Open the input file for reading and output file for writing
with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    # Create a CSV reader to parse the input file
    reader = csv.DictReader(infile)

    # Add a new column for the customer journey tag
    fieldnames = reader.fieldnames + ['CustomerJourneyTag']

    # Create a CSV writer to write to the output file
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header row to the output file

    # Process each row in the input file
    for row in reader:
        comment = row['Comment']  # Extract the survey comment
        industry = row.get('Industry', 'general')  # Extract industry or default to 'general'

        # Generate a prompt for ChatGPT using the comment and industry
        prompt = generate_prompt(comment, industry)

        # Send the prompt to ChatGPT using the ChatCompletion API
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # Specify the model to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the customer journey tag from the response
        tag = response['choices'][0]['message']['content'].strip()

        # Add the tag to the current row
        row['CustomerJourneyTag'] = tag

        # Write the updated row to the output file
        writer.writerow(row)

# Print a message when processing is complete
print(f"Tagged survey comments have been saved to '{output_file}'.")
