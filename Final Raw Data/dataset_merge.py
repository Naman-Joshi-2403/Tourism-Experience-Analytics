import pandas as pd
import os

config = {
    "files": {
        "transaction": "Transaction.xlsx",
        "user": "User.xlsx",
        "city": "City.xlsx",
        "item": "Item.xlsx",
        "type": "Type.xlsx",
        "mode": "Mode.xlsx",
        "continent": "Continent.xlsx",
        "country": "Country.xlsx",
        "region": "Region.xlsx"
    },
    "output_file": "Tourism_Final_Master_Analytical.csv",
    "base_path": r"C:/Users/naman/OneDrive/Desktop/Guvi_Projects/Tourism-Experience-Analytics/Input"
}

def merge_tourism_data_complete(config):
    base = config["base_path"]
    f = config["files"]

    print("🚀 Starting Complete Data Integration...")
    
    # 1. Direct Load from Excel
    df_trans = pd.read_excel(os.path.join(base, f["transaction"]))
    df_user = pd.read_excel(os.path.join(base, f["user"]))
    df_city = pd.read_excel(os.path.join(base, f["city"]))
    df_item = pd.read_excel(os.path.join(base, f["item"]))
    df_type = pd.read_excel(os.path.join(base, f["type"]))
    df_mode = pd.read_excel(os.path.join(base, f["mode"]))
    df_continent = pd.read_excel(os.path.join(base, f["continent"]))
    df_country = pd.read_excel(os.path.join(base, f["country"]))
    df_region = pd.read_excel(os.path.join(base, f["region"]))

    # 2. Build Geography Reference (The "Names" Library)
    geo_ref = df_city.merge(df_country, on="CountryId", how="left")
    geo_ref = geo_ref.merge(df_region, on="RegionId", how="left")
    geo_ref = geo_ref.merge(df_continent, on="ContinentId", how="left")

    # 3. Enrich Traveler Data (Origin)
    # We keep the IDs for ML and add names for the Dashboard
    user_enriched = df_user.merge(geo_ref, on=["CityId", "CountryId", "RegionId", "ContinentId"], how="left")
    user_enriched = user_enriched.rename(columns={
        'CityName': 'Traveler_Home_City',
        'Country': 'Traveler_Home_Country',
        'Region': 'Traveler_Home_Region',
        'Continent': 'Traveler_Home_Continent'
    })

    # 4. Enrich Attraction Data (Destination)
    # Link item to Category Name
    item_full = df_item.merge(df_type, on="AttractionTypeId", how="left")
    
    # Link item to Destination Name (using AttractionCityId)
    # We bring in Country and Region names specifically for the destination spot
    item_dest = item_full.merge(
        geo_ref, 
        left_on="AttractionCityId", 
        right_on="CityId", 
        how="left",
        suffixes=('', '_dest')
    )
    
    item_dest = item_dest.rename(columns={
        'CityName': 'Destination_City_Name',
        'Country': 'Destination_Country_Name',
        'Region': 'Destination_Region_Name',
        'Continent': 'Destination_Continent_Name',
        'Attraction': 'Attraction_Name',
        'AttractionType': 'Attraction_Category'
    })

    # 5. Final Master Merge
    # Start with Transaction (Core Table)
    master_df = df_trans.merge(user_enriched, on="UserId", how="left")
    master_df = master_df.merge(item_dest, on="AttractionId", how="left")
    master_df = master_df.merge(df_mode, left_on="VisitMode", right_on="VisitModeId", how="left")

    # 6. Final Polishing
    # Rename technical columns for clarity
    master_df.rename(columns={
        'VisitYear': 'Year_of_Visit',
        'VisitMonth': 'Month_of_Visit',
        'VisitMode_y': 'Traveler_Group_Type',
        'Rating': 'User_Rating',
        'AttractionAddress': 'Destination_Address'
    }, inplace=True)

    # 7. Quality Check: Drop absolute duplicates but keep ALL features for EDA/ML
    master_df = master_df.loc[:, ~master_df.columns.duplicated()]

    # Save the file
    master_df.to_csv(config["output_file"], index=False)
    print(f"\n✅ SUCCESS: Integrated Master Dataset saved as {config['output_file']}")
    print(f"Total Columns: {len(master_df.columns)}")
    print(f"Total Records: {len(master_df)}")
    
    return master_df

if __name__ == "__main__":
    df = merge_tourism_data_complete(config)