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
    # Load the NpcThinkParamTemplate.csv file from the 'template' folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = os.path.join(script_dir, 'template', 'NpcThinkParamTemplate.csv')
    logging.info(f"Loading template file: {template_file}")
    template_df = pd.read_csv(template_file)

    # Select the CSV file to compare
    compare_file = select_file("Select CSV file to compare")
    logging.info(f"Selected file for comparison: {compare_file}")
    compare_df = pd.read_csv(compare_file)

    # Create a new DataFrame for the new params with the same columns as the template
    new_df = pd.DataFrame(columns=template_df.columns)

    # Columns to be filled with -1
    columns_to_fill_with_minus_one = [
        'soundBehaviorId01', 'soundBehaviorId02', 'soundBehaviorId03', 'soundBehaviorId04',
        'soundBehaviorId05', 'soundBehaviorId06', 'soundBehaviorId07', 'soundBehaviorId08',
        'weaponOffSpecialEffectId', 'weaponOnSpecialEffectId', 'weaponOffAnimId', 'weaponOnAnimId',
        'surpriseAnimId'
    ]

    # Iterate over the comparison file rows and update the template rows
    logging.info("Updating template parameters with comparison file values...")
    for index, compare_row in compare_df.iterrows():
        # Create a new row with the same columns as the template
        new_row = pd.Series(-1, index=new_df.columns)
        
        # Fill in the values from the comparison file where the column names match
        for col in compare_df.columns:
            if col in new_row.index:
                new_row[col] = compare_row[col]
        
        # Set specified columns to -1
        for col in columns_to_fill_with_minus_one:
            if col in new_row.index:
                new_row[col] = -1

        # Set pad3 to [0|0|0|0]
        if 'pad3' in new_row.index:
            new_row['pad3'] = '[0|0|0|0]'

        # Set pad4 to [0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0]
        if 'pad4' in new_row.index:
            new_row['pad4'] = '[0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0]'

        # Set disableParamReserve2 to [0|0|0]
        if 'disableParamReserve2' in new_row.index:
            new_row['disableParamReserve2'] = '[0|0|0]'

        # Set enableNaviFlg_reserve1 to [0|0|0]
        if 'enableNaviFlg_reserve1' in new_row.index:
            new_row['enableNaviFlg_reserve1'] = '[0|0|0]'
        
        # Append the new row to the new template DataFrame using pd.concat
        new_df = pd.concat([new_df, new_row.to_frame().T], ignore_index=True)
        logging.info(f"Processed row for ID: {compare_row['ID']}")

    # Fill missing values with -1
    logging.info("Filling missing values with -1...")
    new_df.fillna(-1, inplace=True)

    # Turn everything from -1 to 0 except for the specified columns
    for col in new_df.columns:
        if col not in columns_to_fill_with_minus_one and col not in ['pad3', 'pad4', 'disableParamReserve2', 'enableNaviFlg_reserve1']:
            new_df[col] = new_df[col].replace(-1, 0)

    # Ensure no extra columns are added
    if 'Unnamed: 106' in new_df.columns:
        new_df.drop(columns=['Unnamed: 106'], inplace=True)

    # Rename the 'surpriseAnimId' column to 'surpriseAnimId,'
    if 'surpriseAnimId' in new_df.columns:
        new_df.rename(columns={'surpriseAnimId': 'surpriseAnimId,'}, inplace=True)

    # Save the new template params to a new CSV file
    save_file = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save new CSV file")
    if save_file:
        logging.info(f"Saving new parameters to: {save_file}")
        new_df.to_csv(save_file, index=False)
        logging.info("File saved successfully.")
    else:
        logging.error("No file selected for saving. Exiting without saving.")

    # Add a warning message
    logging.warning("Careful, a lot of values have been set to 0. Please make sure to edit them.")

except Exception as e:
    logging.error(f"An error occurred: {e}")

# Wait for user input before exiting
input("Press Enter to exit...")