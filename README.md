# scientific-ai

New generation AI

## Utilities

- `generate_zafsa_luse_stock.py`: generates a synthetic Lusaka Stock Exchange dataset and saves it to `data/zafsa_luse_stock_data.csv`.

## Data Pipeline

The `data_pipeline.py` script fetches market data from configurable API endpoints. Set the following environment variables before running:

- `STOCK_EXCHANGE_API` - API endpoint for generic stock data
- `GOLD_PRICE_API` - Endpoint for gold price data
- `INFLATION_DATA_API` - Endpoint for inflation data
- `LUSE_API_ENDPOINT` - Lusaka Stock Exchange API endpoint
- `STOCK_API_KEY`, `GOLD_API_KEY`, `INFLATION_API_KEY`, `LUSE_API_KEY` - API keys for each service

Run the pipeline:

```bash
python data_pipeline.py
```

## Environment Variables

Other scripts require API keys as well:

- `OPENAI_API_KEY` for OpenAI models
- `WEATHER_API_KEY` for `weather_dashboard.py`

Ensure these variables are set in your environment before execution.
