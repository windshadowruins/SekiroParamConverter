import os
import pandas as pd
import logging
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def convert(input_file):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Load the AtkParamNPCTemplate.csv file from the 'template' folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_file = os.path.join(script_dir, 'template', 'AtkParamNPCTemplate.csv')
        logging.info(f"Loading template file: {template_file}")
        template_df = pd.read_csv(template_file)

        # Load the comparison file
        compare_df = pd.read_csv(input_file)

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
            
            # Transfer knockbackDist_DirectHit to knockbackDist
            if 'knockbackDist_DirectHit' in compare_row and 'knockbackDist' in new_row.index:
                new_row['knockbackDist'] = compare_row['knockbackDist_DirectHit']
            
            # Append the new row to the new template DataFrame using pd.concat
            new_df = pd.concat([new_df, new_row.to_frame().T], ignore_index=True)
            logging.info(f"Processed row for ID: {compare_row['ID']}")

        # Fill missing values with 0
        logging.info("Filling missing values with 0...")
        new_df.fillna(0, inplace=True)

        # Set specific columns to the required values
        if 'pad4' in new_df.columns:
            new_df['pad4'] = '[0|0|0]'
        if 'pad7' in new_df.columns:
            new_df['pad7'] = '[0|0|0|0|0|0|0|0|0|0]'

        # Set AppearAiSoundId and HitAiSoundId to the required values
        if 'AppearAiSoundId' in new_df.columns:
            new_df['AppearAiSoundId'] = 2100
        if 'HitAiSoundId' in new_df.columns:
            new_df['HitAiSoundId'] = 2010

        # Ensure no extra columns are added
        if 'Unnamed: 213' in new_df.columns:
            new_df.drop(columns=['Unnamed: 213'], inplace=True)

        # Rename the 'pad7' column to 'pad7,'
        if 'pad7' in new_df.columns:
            new_df.rename(columns={'pad7': 'pad7,'}, inplace=True)

        # Ensure the output directory exists
        output_dir = os.path.join(script_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)

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

# Example usage
if __name__ == "__main__":
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    input_file = askopenfilename(title="Select CSV file to convert")
    if input_file:
        convert(input_file)
    else:
        logging.error("No file selected for conversion. Exiting.")