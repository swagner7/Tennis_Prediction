import os
import pandas as pd

# Define the folder containing the Excel files and the output CSV file
data_folder = '/Users/swagner/VSCode/Tennis_Prediction/src/data'
output_csv = os.path.join(data_folder, 'consolidated_data.csv')

def consolidate_excel_files_to_csv(data_folder, output_csv):
    # Initialize an empty list to store dataframes
    dataframes = []

    # Loop through all files in the data folder
    for root, dirs, files in os.walk(data_folder):
        for file_name in files:
            if file_name.endswith(('.xlsx', '.xls')):
                file_path = os.path.join(data_folder, file_name)
                # Read the Excel file and append it to the list
                df = pd.read_excel(file_path)
                dataframes.append(df)

    # Concatenate all dataframes into one
    if dataframes:
        consolidated_df = pd.concat(dataframes, ignore_index=True)
        
        # Sort the DataFrame by the 'date' column
        if 'Date' in consolidated_df.columns:
            consolidated_df['Date'] = pd.to_datetime(consolidated_df['Date'], errors='coerce')  # Ensure 'date' is in datetime format
            consolidated_df = consolidated_df.sort_values(by='Date')

        # Save the consolidated dataframe to a CSV file
        consolidated_df.to_csv(output_csv, index=False)
        print(f"Consolidated data saved to {output_csv}")
    else:
        print("No Excel files found in the data folder.")

if __name__ == "__main__":
    consolidate_excel_files_to_csv(data_folder, output_csv)