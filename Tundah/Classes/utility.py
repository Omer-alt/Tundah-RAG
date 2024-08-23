import os
import json
import torch

import pandas as pd

class Utility:

    def __init__(self):
        self.languages = [
            'en',  # English
            'fr',  # French
            'ar',  # Arabic
            'es',  # Spanish
            'zh',  # Chinese
            'sw',  # Swahili (widely spoken in East Africa)
            'ha',  # Hausa (widely spoken in West Africa)
            'am',  # Amharic (spoken in Ethiopia)
            'pt',  # Portuguese (spoken in Mozambique and Angola)
            'yo',  # Yoruba (spoken in Nigeria)
            'zu'   # Zulu (spoken in South Africa)
        ]
        

    def create_dir(self, output_dir): 
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
            
    def load_json_to_dataframe(self, json_path):
        """
        Loads a JSON file into a Pandas DataFrame.

        Parameters:
        - json_path: Path to the JSON file.

        Returns:
        - df: DataFrame containing the data from the JSON file.
        """
        # Load the JSON data
        with open(json_path, 'r') as file:
            data = json.load(file)
        
        # Convert the JSON data into a Pandas DataFrame
        df = pd.DataFrame(data)
        
        return df, data
    
    def append_to_json(self, file_path, new_data):
        """
        Appends new data to an existing JSON file. If the file doesn't exist, it creates one.
        
        Parameters:
        - file_path: Path to the JSON file.
        - new_data: List of dictionaries containing the new data to be appended.
        """
        # Load existing data if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as infile:
                existing_data = json.load(infile)
        else:
            existing_data = []

        # Append the new data to the existing data
        combined_data = existing_data + new_data

        # Save the combined data back into the JSON file
        with open(file_path, 'w') as outfile:
            json.dump(combined_data, outfile, indent=4)
            
    def file_pdf_paths(self, docs_path ):
        
        files_path = []
        try:
            # Traverse the folder and collect all file paths
            for file in os.listdir(docs_path):
                file_path = os.path.join(docs_path, file)
                if os.path.isfile(file_path):
                    files_path.append(file_path)
                    
            return  files_path      
        except Exception as e : 
            print(e)
      
      
    @staticmethod      
    def get_device():
        # Define device
        if torch.backends.mps.is_available():
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        return device