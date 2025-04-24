### 📄 `README.md`

````markdown
# BacenAPI

**BacenAPI** is a Python package designed to simplify the access and manipulation of time 
series data from the Central Bank of Brazil (Banco Central do Brasil - BCB), using its 
public API (SGS - Sistema Gerenciador de Séries Temporais).

---

## 📦 Features

- 🔍 **Search series** using keywords in the metadata
- 🔗 **Generate URLs** for one or more time series from BCB's SGS API
- 📊 **Download and structure** the time series data into a unified `pandas.DataFrame`
- 📁 Supports integration with local metadata files in `.txt` or `.parquet` formats

---

## 🚀 Installation

```bash
pip install BacenAPI
````

Or, if you're developing locally:

```bash
git clone https://github.com/LissandroSousa/BacenAPI.py.git
cd BacenAPI
pip install -e .
```

---

## 🧩 Dependencies

- `pandas`
- `requests`

---

## 🛠️ Usage Example

```python
from BacenAPI import bacen_search, bacen_url, bacen_series

# Search for time series by keyword
df_search = bacen_search("IPCA")
print(df_search)

# Get URLs for a specific set of series
urls = bacen_url(series=[433, 4440], start_date="01/01/2020", end_date="01/01/2024")

# Download the data and format as DataFrame
df = bacen_series(urls)
print(df.head())
```

---

## 📂 Project Structure

```
BacenAPI/
├── BacenAPI/
│   ├── __init__.py
│   ├── bacen_search.py
│   ├── bacen_url.py
│   ├── bacen_series.py
│   └── Date/
│       └── arquivo1.txt
├── setup.py
├── pyproject.toml
└── README.md

```

---

## 👥 Authors

- Paulo Andre
- Lissandro Costa de Sousa
- Prof. Francisco Gildemir Ferreira da Silva *(Supervisor)*

---

## 📄 License

This project is licensed under the **MIT License**. See the [`LICENSE`](./LICENSE) file for more details.

---

## 📫 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 🌐 Source and Documentation

- Official API: [https://dadosabertos.bcb.gov.br/dataset/serie-historica-dos-indicadores-economicos](https://dadosabertos.bcb.gov.br/dataset/serie-historica-dos-indicadores-economicos)
- SGS API Docs: [https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries](https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries)
