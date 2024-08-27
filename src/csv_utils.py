import pandas as pd

def load_data():
    df = pd.read_csv('climbing_gyms.csv')  # Replace 'your_file.csv' with the path to your CSV file
    return df