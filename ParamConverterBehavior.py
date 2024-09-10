import os
import pandas as pd
import logging
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to open file dialog and select a file
def select_file(title):
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(title=title)
    if not filename:
        logging.error(f"No file selected for {title}")
        exit()
    logging.info(f"Selected file for {title}: {filename}")
    return filename

try:
    # Load the BehaviorTemplate.csv file from the 'template' folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = os.path.join(script_dir, 'template', 'BehaviorTemplate.csv')
    logging.info(f"Loading template file: {template_file}")
    template_df = pd.read_csv(template_file)

    # Select the CSV file to compare
    compare_file = select_file("Select CSV file to compare")
    logging.info(f"Selected file for comparison: {compare_file}")
    compare_df = pd.read_csv(compare_file)

    # Create a new DataFrame for the new params with the same columns as the template
    new_df = pd.DataFrame(columns=template_df.columns)

    # Iterate over the comparison file rows and update the template rows
    logging.info("Updating template parameters with comparison file values...")
    for index, compare_row in compare_df.iterrows():
        # Create a new row with the same columns as the template
        new_row = pd.Series(0, index=new_df.columns)
        
        # Fill in the values from the comparison file where the column names match
        for col in compare_df.columns:
            if col in new_row.index:
                new_row[col] = compare_row[col]
        
        # Append the new row to the new template DataFrame using pd.concat
        new_df = pd.concat([new_df, new_row.to_frame().T], ignore_index=True)
        logging.info(f"Processed row for ID: {compare_row['ID']}")

    # Fill missing values with 0
    logging.info("Filling missing values with 0...")
    new_df.fillna(0, inplace=True)

    # Set specific columns to the required values
    if 'pad2' in new_df.columns:
        new_df['pad2'] = '[0|0]'

    # Ensure no extra columns are added
    if 'Unnamed: 14' in new_df.columns:
        new_df.drop(columns=['Unnamed: 14'], inplace=True)

    # Rename the 'pad1' column to 'pad1,'
    if 'pad1' in new_df.columns:
        new_df.rename(columns={'pad1': 'pad1,'}, inplace=True)

    # Save the new template params to a new CSV file
    save_file = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save new CSV file")
    if save_file:
        logging.info(f"Saving new parameters to: {save_file}")
        new_df.to_csv(save_file, index=False)
        logging.info("File saved successfully.")
    else:
        logging.error("No file selected for saving. Exiting without saving.")

except Exception as e:
    logging.error(f"An error occurred: {e}")

# Wait for user input before exiting
input("Press Enter to exit...")