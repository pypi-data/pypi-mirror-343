# cnstats-py

[![Release](https://github.com/clsrfish/cnstats-py/actions/workflows/publish.yml/badge.svg?branch=master&event=release)](https://github.com/clsrfish/cnstats-py/actions/workflows/publish.yml)

A Python package to easily download macroeconomic data from the National Bureau of Statistics of China (<https://data.stats.gov.cn>).

## Installation

```bash
pip install cnstats-py
# or
pipenv install cnstats-py
```

## Basic Usage

```python
import cnstats

# Example: Get data for a specific indicator and year
data: pd.DataFrame = cnstats.query_data(DBCode.hgyd, "A01010G", "2024")
print(data.shape)
```

In terminal:

```bash
python -m cnstats --dbcode hgyd --indicator A01010G --sj 2024
```

## Features

- Fetch data from the National Bureau of Statistics of China
- Support for multiple databases and indicators
- Easy to use command line interface
- Data is returned as a pandas DataFrame for easy manipulation and analysis
- Support for multiple data formats (CSV, DTA, etc.)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
