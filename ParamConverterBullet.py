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
    # Load the BulletTemplate.csv file from the 'template' folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = os.path.join(script_dir, 'template', 'BulletTemplate.csv')
    logging.info(f"Loading template file: {template_file}")
    elden_ring_df = pd.read_csv(template_file)

    # Select the CSV file to compare
    compare_file = select_file("Select CSV file to compare")
    logging.info(f"Selected file for comparison: {compare_file}")
    compare_df = pd.read_csv(compare_file)

    # Create a new DataFrame for the new Elden Ring params with the same columns as the template
    new_elden_ring_df = pd.DataFrame(columns=elden_ring_df.columns)

    # Columns to be filled with -1
    columns_to_fill_with_minus_one = [
        'assetNo_Hit', 'seId_Bullet1', 'seId_Bullet2', 'seId_Hit', 'seId_Flick', 'followDmypoly_forSfxPose'
    ]

    # Iterate over the comparison file rows and update the template rows
    logging.info("Updating template parameters with comparison file values...")
    for index, compare_row in compare_df.iterrows():
        # Create a new row with the same columns as the template
        new_row = pd.Series(0, index=new_elden_ring_df.columns)
        
        # Fill in the values from the comparison file where the column names match
        for col in compare_df.columns:
            if col in new_row.index:
                new_row[col] = compare_row[col]
        
        # Set specified columns to -1
        for col in columns_to_fill_with_minus_one:
            if col in new_row.index:
                new_row[col] = -1
        
        # Append the new row to the new template DataFrame using pd.concat
        new_elden_ring_df = pd.concat([new_elden_ring_df, new_row.to_frame().T], ignore_index=True)
        logging.info(f"Processed row for Name: {compare_row['Name']}")

    # Fill missing values with 0
    logging.info("Filling missing values with 0...")
    new_elden_ring_df.fillna(0, inplace=True)

    # Set the 'spBulletDistUpRate' column to 1
    if 'spBulletDistUpRate' in new_elden_ring_df.columns:
        new_elden_ring_df['spBulletDistUpRate'] = 1

    # Convert the specific column 'pad4' back to the original format
    if 'pad4' in new_elden_ring_df.columns:
        new_elden_ring_df['pad4'] = '[0|0|0|0|0|0|0|0]'

    # Ensure no extra columns are added
    if 'Unnamed: 122' in new_elden_ring_df.columns:
        new_elden_ring_df.drop(columns=['Unnamed: 122'], inplace=True)

    # Rename the 'pad4' column to 'pad4,'
    new_elden_ring_df.rename(columns={'pad4': 'pad4,'}, inplace=True)

    # Save the new template params to a new CSV file
    save_file = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save new CSV file")
    if save_file:
        logging.info(f"Saving new parameters to: {save_file}")
        new_elden_ring_df.to_csv(save_file, index=False)
        logging.info("File saved successfully.")
    else:
        logging.error("No file selected for saving. Exiting without saving.")

except Exception as e:
    logging.error(f"An error occurred: {e}")

# Wait for user input before exiting
input("Press Enter to exit...")