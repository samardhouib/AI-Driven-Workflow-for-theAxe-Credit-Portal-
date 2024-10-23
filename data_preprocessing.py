import pandas as pd
import json

# Load Excel file
excel_file = 'C:/Users/HP/Desktop/axe_stage/django_app_for_axe_model/testcases.xlsx'

# Assuming each sheet name represents a dataset split
sheet_names = pd.ExcelFile(excel_file).sheet_names
print("Sheet names found:", sheet_names)

data = {}
for sheet_name in sheet_names:
    # Read each sheet into a DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Convert DataFrame to list of dictionaries
    records = df.to_dict(orient='records')

    # Store in the dictionary under the sheet name
    data[sheet_name] = records


# Combine all sheets data into one list with "instruction" and "output" format
combined_data = []
for sheet_name, sheet_data in data.items():
    for record in sheet_data:
        # Assuming the instruction is in a column named 'instruction'
        # and the output is in a column named 'output'
        combined_data.append({
            'instruction': record['Actions'],
            'output': record['Code Groovy']
        })

# Save as JSON files
with open('train_data2.json', 'w') as f:
    json.dump(combined_data, f)


