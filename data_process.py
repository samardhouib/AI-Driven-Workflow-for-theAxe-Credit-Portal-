import pandas as pd
import json
from itertools import combinations
from tqdm import tqdm


def excel_to_json(excel_file, json_file, max_combination_size=None):
    # Load the Excel file
    excel_data = pd.ExcelFile(excel_file)


instructions = []

# Iterate through each sheet in the Excel file
for sheet_name in tqdm(excel_data.sheet_names, desc="Sheets"):
    # Read the sheet into a DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Convert the DataFrame to a list of dictionaries
data = df.to_dict('records')

# Initialize progress bar for combinations
if max_combination_size is None:
    max_combination_size = len(data)
else:
    max_combination_size = min(max_combination_size, len(data))

total_combinations = sum(len(list(combinations(data, r))) for r in range(1, max_combination_size + 1))
progress_bar = tqdm(total=total_combinations, desc=f"Processing {sheet_name}")

# Generate combinations of actions and their corresponding code
for r in range(1, max_combination_size + 1):
    for combo in combinations(data, r):
        actions = ' '.join(item['Actions'] for item in combo)
        codes = '\n'.join(item['Code Groovy'] for item in combo)
        instruction = {
            "instruction": actions,
            "output": codes
        }
        instructions.append(instruction)
        progress_bar.update(1)

# Close the progress bar
progress_bar.close()

# Convert the list of instructions to JSON format
with open(json_file, 'w') as json_out:
    json.dump(instructions, json_out, indent=4)

# Example usage with a limit on the maximum combination size
excel_to_json('/kaggle/input/amaamammamam/data.xlsx', 'output.json', max_combination_size=4)