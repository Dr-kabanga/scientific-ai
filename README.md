# scientific-ai
New generation AI

## Data Pipeline
The repository includes a `data_pipeline.py` script that fetches market data and prepares it for analysis. It now supports optional integration with the Lusaka Stock Exchange (LUSE) and ZAFSA data sources. To enable these integrations, set the following environment variables before running the pipeline:

- `STOCK_API_KEY` – API key for the generic stock exchange endpoint
- `GOLD_API_KEY` – API key for gold price data
- `INFLATION_API_KEY` – API key for inflation data
- `LUSE_API_KEY` – API key for LUSE stock data
- `ZAFSA_API_KEY` – API key for ZAFSA market data

Run the pipeline with:

```bash
python data_pipeline.py
```

The processed data is saved in the `data/` directory.
