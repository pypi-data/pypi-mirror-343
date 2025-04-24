import pandas as pd
import importlib.resources as pkg_resources

def bacen_search(keyword):
    """
    Searches for a keyword in the 'Full_Name' field of a local .txt file.

    Parameter:
        keyword (str): Keyword to search for.

    Returns:
        DataFrame with the filtered results.
    """
    # Simple file reading (adjust the separator if necessary)
    with pkg_resources.files("BacenAPI").joinpath("Date/dataset.txt").open("r", encoding="utf-8") as file:
        df = pd.read_csv(file, sep=";")
    
    # Filter by partial match (case-insensitive)
    results = df[df['Full_Name'].str.contains(keyword, case=False, na=False)].copy()
    
    # Select and adjust the desired columns
    results = results[['Code', 'Full_Name', 'Unit', 'Periodicity', 'Start_Date']]
    results['Full_Name'] = results['Full_Name'].str.slice(0, 50)
    
    return results
