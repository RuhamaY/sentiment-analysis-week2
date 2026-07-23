# Financial News Sentiment & Stock Movement Analysis

Nova Financial Solutions project analyzing FNSPID financial news headlines and their relationship with stock price movements.

## Business Objectives

- **Sentiment analysis**: Quantify headline tone with NLP (TextBlob/NLTK)
- **Correlation analysis**: Measure statistical links between news sentiment and daily stock returns
- **Investment insights**: Derive actionable strategies from sentiment–price relationships

## Project Structure

```
├── .github/workflows/
│   └── unittests.yml          # CI pipeline
├── .vscode/
│   └── settings.json          # Editor / pytest config
├── data/
│   ├── raw/                   # FNSPID news CSV (not committed)
│   └── stocks/                # OHLCV CSV per ticker
├── notebooks/
│   ├── task-1/eda.ipynb       # EDA: headlines, publishers, time series
│   ├── task-2/                # TA-Lib indicators & PyNance metrics
│   └── task-3/                # Sentiment scoring & correlation
├── scripts/
│   └── fetch_stock_data.py    # Download stock data via yfinance
├── src/                       # Reusable Python modules
│   ├── data_loader.py
│   ├── indicators.py
│   ├── metrics.py
│   ├── sentiment.py
│   ├── correlation.py
│   └── utils.py
├── tests/
│   └── test_analysis.py
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/RuhamaY/sentiment-analysis-week2
cd sentiment-analysis-week2
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download NLTK corpora for TextBlob (first run only)
python -m textblob.download_corpora
```

### Data

1. Place the FNSPID news file at `data/raw/raw_analyst_ratings.csv`
2. Fetch stock prices:

```bash
python scripts/fetch_stock_data.py AAPL MSFT GOOG AMZN NVDA TSLA --start 2020-01-01
```

## Tasks

| Task | Branch   | Notebook(s) | Focus |
|------|----------|-------------|-------|
| 1    | `task-1` | `notebooks/task-1/eda.ipynb` | EDA, publisher & date analysis, topic keywords |
| 2    | `task-2` | `notebooks/task-2/technical_analysis.ipynb` | TA-Lib (MA, RSI, MACD), PyNance metrics |
| 3    | `task-3` | `notebooks/task-3/sentiment_return_correlation.ipynb` | Sentiment scoring, daily returns, Pearson correlation |

## Running Tests

```bash
pytest tests/ -v
```

## Tools

Python, Pandas, NLTK, TextBlob, TA-Lib, yfinance, scikit-learn, GitHub Actions

## Workflow

1. Create branch `task-1`, complete EDA, open PR to `main`
2. Create branch `task-2`, merge task-1 via PR, add technical analysis
3. Create branch `task-3`, merge task-2 via PR, run sentiment–return correlation
