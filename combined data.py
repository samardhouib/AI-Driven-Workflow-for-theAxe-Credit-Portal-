import json

# Read the first JSON file
with open(r'C:\Users\HP\Desktop\axe_stage\django_app_for_axe_model\train_data (1).json', 'r') as f1:
    data1 = json.load(f1)

# Read the second JSON file
with open(r'C:\Users\HP\Desktop\axe_stage\django_app_for_axe_model\train_data2.json', 'r') as f2:
    data2 = json.load(f2)

# Combine the data
# Assuming both files contain dictionaries
combined_data = data1 + data2

# Write the combined data to a new JSON file
with open('combined.json', 'w') as f:
    json.dump(combined_data, f, indent=4)
