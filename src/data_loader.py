import pandas as pd
from datetime import datetime

def clean_data(df):
    
    df_clean = df.dropna(subset=["Latitude", "Longitude", "Obligor Name"])
    df_unique = df_clean.drop_duplicates(subset=["Obligor Name", "Latitude", "Longitude"])
    df_unique = df_unique.reset_index(drop=True)
    print(f"Final unique entries: {df_unique.shape[0]}")
    df_unique.head()
    return df_unique

def merge_portfolio_with_location(portfolio_data: pd.DataFrame, location_data: pd.DataFrame) -> pd.DataFrame:
    """
    Merges portfolio_data with location_data on 'Obligor Name' after uppercasing and stripping whitespace.
    
    Parameters:
        portfolio_data (pd.DataFrame): DataFrame containing portfolio information.
        location_data (pd.DataFrame): DataFrame containing obligor location details (lat, long, state, etc.).
        
    Returns:
        pd.DataFrame: Merged DataFrame with additional location fields.
    """
    portfolio_data = portfolio_data.copy()
    location_data = location_data.copy()
    
    portfolio_data['Obligor Name'] = portfolio_data['Obligor Name'].str.upper().str.strip()
    location_data['Obligor Name'] = location_data['Obligor Name'].str.upper().str.strip()
    merged_data = pd.merge(
        portfolio_data,
        location_data[['Obligor Name', 'County', 'State', 'ZIP', 'Latitude', 'Longitude']],
        on='Obligor Name',
        how='left'
    )
    unmatched = merged_data[merged_data['Latitude'].isna()]

    print(f"Unmatched rows: {len(unmatched)}")
    return merged_data



def load_data(portfolio_data_path='data/PortfolioX.xlsx',location_data_path='data/location_data.xlsx'):
    portfolio_data = pd.read_excel(portfolio_data_path)
    location_data = pd.read_excel(location_data_path)
    location_data=clean_data(location_data)
    df=merge_portfolio_with_location(portfolio_data,location_data)
    # Preprocessing
    # Preprocessing
    df['maturity'] = pd.to_datetime(df['maturity'])
    df['years_to_maturity'] = (df['maturity'] - datetime.now()).dt.days / 365
    
    # Create rating buckets
    df['Rating_Bucket'] = df['Rating'].str.extract(r'([A-Z]+)')[0]
    df['Rating_Bucket'] = df['Rating_Bucket'].replace({
        'AAA': 'AAA',
        'AA': 'AA',
        'A': 'A',
        'BBB': 'BBB',
        'BB': 'HY', 'B': 'HY', 'CCC': 'HY', 'CC': 'HY', 'C': 'HY', 'D': 'HY'
    }).fillna('Unrated')
    
    # Clean State column - convert to string and handle missing values
    df['State'] = df['State'].fillna('Unknown')
    df['State'] = df['State'].astype(str)
    
    # Clean Sector column
    df['Sector'] = df['Sector'].fillna('Unknown')
    
    # Create maturity buckets
    bins = [0, 5, 10, 15, 20, 30, 100]
    labels = ['<5', '5-10', '10-15', '15-20', '20-30', '30+']
    df['Maturity_Bucket'] = pd.cut(df['years_to_maturity'], bins=bins, labels=labels)
    
    # Clean Outlook column
    df['Outlook'] = df['Outlook'].fillna('Not Available')
    
    return df