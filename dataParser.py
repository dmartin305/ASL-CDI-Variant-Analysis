import pandas as pd
import re


def find_matching_rows(label_file, data_file):
    # Load the CSV files into dataframes
    label_df = pd.read_csv(label_file)
    data_df = pd.read_csv(data_file)

    # Initialize a dictionary to store label mappings
    label_mapping = {}

    # Create a mapping of labels to their corresponding entries
    for index, row in label_df.iterrows():
        label = row['signs']
        label_mapping[label] = []

        for entry in data_df['Entry ID']:
            match = re.match(fr'{label}(_(\d+))?$', entry)
            if match:
                label_mapping[label].append(entry)

    # Create a new dataframe to store the matching rows
    matching_rows = pd.DataFrame(columns=data_df.columns)

    # Extract matching rows based on the label mapping
    for label, entries in label_mapping.items():
        matching_rows = matching_rows.append(
            data_df[data_df['Entry ID'].isin(entries)], ignore_index=True)
    matching_rows =  matching_rows.sort_values(by=['Entry ID'], key=lambda col: col.str.lower())
    matching_rows.to_csv("ASL_CDI_ASLLEX.csv", index=False)
    return matching_rows


# Replace with your actual CSV file paths
label_file_path = 'signs.csv'
data_file_path = 'ASLLEX.csv'

matching_rows = find_matching_rows(label_file_path, data_file_path)

# Print or manipulate the resulting dataframe as needed
print(matching_rows)
