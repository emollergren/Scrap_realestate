import pandas as pd
import json
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the Excel file and the output JSON file relative to the script's location
excel_file_path = os.path.join(script_dir, 'Mail.xlsx')
json_file_path = os.path.join(script_dir, 'mail.json')

def normalize_phone(phone):
    if pd.isna(phone):
        return ""
    digits = ''.join(filter(str.isdigit, str(phone)))
    return digits if digits else ""

try:
    # Read the Excel file into a pandas DataFrame
    # The engine 'openpyxl' is needed for .xlsx files.
    df = pd.read_excel(excel_file_path, engine='openpyxl')

    # Define the specific columns you want to keep
    columns_to_keep = ['username', 'name', 'office', 'company', 'bio', 'email', 'phone1', 'phone2']
    
    # Filter the DataFrame to keep only the specified columns that exist in the file
    df_filtered = df[[col for col in columns_to_keep if col in df.columns]]

    # Normalize phone1 and phone2 columns to string of digits
    for col in ['phone1', 'phone2']:
        if col in df_filtered.columns:
            df_filtered[col] = df_filtered[col].apply(normalize_phone)

    # Convert the DataFrame to a list of dictionaries
    # 'records' orientation creates a list of dictionaries, one for each row.
    data = df_filtered.to_dict(orient='records')

    # Write the data to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Successfully converted {excel_file_path} to {json_file_path}")

except FileNotFoundError:
    print(f"Error: The file {excel_file_path} was not found.")
except KeyError as e:
    print(f"Error: A required column was not found in the Excel file: {e}")
except ImportError:
    print("Error: pandas or openpyxl is not installed. Please install them using 'pip install pandas openpyxl'")
except Exception as e:
    print(f"An error occurred: {e}")
