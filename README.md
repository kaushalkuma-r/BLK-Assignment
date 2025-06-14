# Municipal Bonds Portfolio Analysis

This project analyzes a municipal bonds portfolio to assess its characteristics and risks. The analysis includes sector distribution, credit risk assessment, rating coverage, outlook distribution, and geographic diversification.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── data/
│   ├── PortfolioX.xlsx
│   └── location_data.xlsx
├── src/
│   ├── analysis/
│   │   ├── sector_analysis.py
│   │   ├── credit_risk_analysis.py
│   │   ├── rating_analysis.py
│   │   ├── outlook_analysis.py
│   │   ├── obligor_analysis.py
│   │   ├── maturity_analysis.py
│   │   ├── jump_risk_analysis.py
│   │   └── geographic_analysis.py
│   └── visualization/
│       └── dashboard.py
└── notebooks/
    └── portfolio_analysis.ipynb
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Windows:
```bash
.\venv\Scripts\activate
```
- On Unix or MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Files

The project requires two Excel files:
1. `PortfolioX.xlsx` - Contains portfolio position data
2. `location_data.xlsx` - Contains data on obligor locations

Place these files in the `data/` directory.

## Running the Analysis

1. For interactive analysis, use the Jupyter notebook:
```bash
jupyter notebook notebooks/portfolio_analysis.ipynb
```
