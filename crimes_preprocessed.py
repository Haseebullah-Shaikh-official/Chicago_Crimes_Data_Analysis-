import pandas as pd


def get_data_preprocess():
    chicago_crimes_df = pd.read_csv('Crimes_-_2001_to_Present.csv')
    columns_to_drop = ['Case Number', 'IUCR', 'Description', 'FBI Code', 'X Coordinate', 
                   'Y Coordinate', 'Updated On', 'Location', ]

    chicago_crimes_df.drop(columns=columns_to_drop, inplace=True) 
    # Create a mapping of blocks to their respective community areas and wards
    block_to_community_mapping = chicago_crimes_df.dropna(subset=['Community Area', 'Block']).set_index('Block')['Community Area'].to_dict()
    block_to_ward_mapping = chicago_crimes_df.dropna(subset=['Ward', 'Block']).set_index('Block')['Ward'].to_dict()

    # Fill NaN values in 'Community Area' and 'Ward' columns using the mappings
    chicago_crimes_df['Community Area'] = chicago_crimes_df.apply(lambda row: block_to_community_mapping.get(row['Block']) if pd.isna(row['Community Area']) else row['Community Area'], axis=1)
    chicago_crimes_df['Ward'] = chicago_crimes_df.apply(lambda row: block_to_ward_mapping.get(row['Block']) if pd.isna(row['Ward']) else row['Ward'], axis=1)

    chicago_crimes_df['Location Description'].fillna("not specified", inplace=True)
    chicago_crimes_df['Longitude'].fillna("not specified", inplace=True)
    chicago_crimes_df['Latitude'].fillna("not specified", inplace=True)
    chicago_crimes_df['Community Area'].fillna(100, inplace=True)
    chicago_crimes_df['Ward'].fillna(100, inplace=True)
    chicago_crimes_df['District'].fillna(100, inplace=True)

    chicago_crimes_df.to_csv("preprocessed_crimes.csv")

get_data_preprocess()