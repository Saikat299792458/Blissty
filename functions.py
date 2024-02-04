import pandas as pd
import os
import cv2
import numpy as np

class functions:
    def __init__(self) -> None:
        self.path = os.getcwd() + '\\static\\uploads\\' # Windows only
        self.excel_file_path = self.path + 'log.xlsx'

        # If the Excel file doesn't exist, create it with headers
        if not os.path.exists(self.excel_file_path):
            headers = ['Timestamp', 'Device Name', 'Red', 'Green', 'Blue', 'Alpha', 'Intensity', 'Image Link']
            pd.DataFrame(columns=headers).to_excel(self.excel_file_path, index=False)
        
        # Read the existing data from the Excel file
        self.existing_data = pd.read_excel(self.excel_file_path)
    
    def update_excel_file(self, timestamp, device_name, optical_condition, filename):
        # Create a DataFrame with the new data
        new_data = pd.DataFrame({
            'Timestamp': [timestamp],
            'Device Name': [device_name],
            'Optical Condition': [optical_condition],
            'Red': [self.Red],
            'Green': [self.Green],
            'Blue': [self.Blue],
            'Alpha': [self.alpha],
            'Intensity': [self.intensity],
            'Image Link': [f'=HYPERLINK("{self.path + filename}", "{filename}")']
        })

        try:
            # Concatenate the new data with the existing DataFrame in memory
            self.existing_data = pd.concat([self.existing_data, new_data], ignore_index=True)

            # Save the updated DataFrame back to the Excel file
            self.existing_data.to_excel(self.excel_file_path, index=False)

        except Exception as e:
            print(f"Error updating Excel file: {e}")

        

    def process_image(self, filename):
        # Load the image
        img = cv2.imread(self.path + filename)

        # Check if the image has an alpha channel
        if img.shape[2] == 3:
            # Image doesn't have an alpha channel, set transparency to N/A or any desired value
            self.alpha = 'N/A'
        else:
            # Extract Transparency values
            self.alpha = np.mean(img[:, :, 3])
        self.Red = np.mean(img[:, :, 2])
        self.Green = np.mean(img[:, :, 1])
        self.Blue = np.mean(img[:, :, 0])
        self.intensity = np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

        # Pack and return
        rgba_values = {
            '1.Red': self.Red,
            '2.Green': self.Green,
            '3.Blue': self.Blue,
            '4.Alpha': self.alpha,
            '5.Intensity': self.intensity
        }
        return rgba_values