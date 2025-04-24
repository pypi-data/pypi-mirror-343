import requests
import pandas as pd

def bacen_series(urls):
    """
    Collects and organizes time series data from the Central Bank of Brazil's API (SGS).

    This function receives a list of URLs from the Bacen API (in JSON format),
    fetches the data for each series, processes and converts values to numeric type,
    transforms the dates into datetime objects, and returns a consolidated DataFrame
    containing all the series merged by the date column.

    Parameters:
    ----------
    urls : list of str
        List of API URLs generated using the `bacen_url` function.

    Returns:
    -------
    pandas.DataFrame
        A DataFrame containing the time series combined by date.
        Each column represents a different series, identified by its code.
        If no series is successfully retrieved, returns an empty DataFrame.
    """
    series_dict = {}

    for url in urls:
        code = url.split("bcdata.sgs.")[1].split("/")[0]
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data_json = response.json()
                df = pd.DataFrame(data_json)
                df['valor'] = df['valor'].str.replace(',', '.').astype(float)
                df['data'] = pd.to_datetime(df['data'], dayfirst=True)
                df = df[['data', 'valor']].rename(columns={'valor': code})
                series_dict[code] = df
                print(f'Successfully retrieved series {code}.')
            else:
                print(f'Error {response.status_code} while trying to retrieve series {code}.')
        except Exception as e:
            print(f'Connection error while retrieving series {code}: {e}.')

    if series_dict:
        # Progressive merge using the 'data' column as the key
        final_df = None
        for df in series_dict.values():
            if final_df is None:
                final_df = df
            else:
                final_df = pd.merge(final_df, df, on='data', how='outer')
        
        final_df = final_df.sort_values(by='data').reset_index(drop=True)
        return final_df
    else:
        print("No series was successfully retrieved.")
        return pd.DataFrame()
