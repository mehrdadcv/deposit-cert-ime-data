# IME Deposit Certificate Data Collector

A Python script for downloading commodity deposit certificate trade data from [Iran Mercantile Exchange](https://www.ime.co.ir).

The script can filter trade data by commodity and save it as a CSV file.

## Description

An example of gold bar trade data is available on the [IME Gold Transaction Statistics](https://gold.ime.co.ir/Main/TransactionStatistics) page.

The script connects to an IME API that provides data for several commodities, including gold bars, silver bars, and gold coins.
Because the API may return multiple commodities for a specified date range, the script filters the response and only keeps the selected commodity.

The API accepts a limited date range for each request. The script is designed to divide a longer collection period into smaller windows and send a separate POST request for each one.

Configuration is read from `settings.yaml`, including:

- the commodity to keep
- the date from which data collection should begin
- the name of the output CSV file

## Requirements

- Python 3.14+
- pandas 3.0.5
- PyYAML 6.0.3
- requests 2.34.2
- python-dateutil 2.9.0.post0

All dependencies are listed in `requirements.txt`. install them with:

```bash
pip install -r requirements.txt
```

## Configuration

Edit `settings.yaml` to configure the start date, commodity filter, and output filename:

```yaml
start_collection_from: "2026-01-01"
filter_commodity: 2
output_file_name: "deposit_cert_data.csv"
```
