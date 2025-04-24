def bacen_url(series, start_date, end_date):
    """
    Generates URLs to query time series from the Central Bank of Brazil's API (SGS).

    This function receives a list of time series codes and a date range,
    and returns the corresponding URLs for JSON requests to the Bacen API.

    Parameters:
    ----------
    series : list of int
        List of desired time series codes.
    
    start_date : str
        Start date in the format 'dd/mm/yyyy'.
    
    end_date : str
        End date in the format 'dd/mm/yyyy'.

    Returns:
    -------
    list of str
        List of formatted URLs for querying the Central Bank API.
    """
    if isinstance(series, int):
        series = [series]

    base_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.'
    urls = []

    for s in series:
        full_url = f'{base_url}{s}/dados?formato=json&dataInicial={start_date}&dataFinal={end_date}'
        urls.append(full_url)

    return urls
