import geopandas as gpd
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)

# geojson to CSV: read GeoJSON, add the source city, convert geometry to WKT, and save the raw data to CSV
def geojson_to_raw_csv(
    input_filepath: str,
    output_filepath: str,
    city: str,
) -> pd.DataFrame:

    gdf = gpd.read_file(input_filepath)
    # add source
    gdf["city_source"] = city

    # keep the coordinates info as metadata
    gdf["source_crs"] = str(gdf.crs)

    # convert GeoDataFrame to a regular df
    df = pd.DataFrame(gdf.copy())

    # convert geometry objects to WKT strings
    df["geometry"] = gdf.geometry.to_wkt()

    df.to_csv(output_filepath, index=False, encoding="utf-8")

    return df

df_prague = geojson_to_raw_csv(
        input_filepath="data/raw/Prague.geojson",
        output_filepath="data/raw/Prague_raw.csv",
        city="Prague",
    )

df_munich = geojson_to_raw_csv(
        input_filepath="data/raw/Munchen.geojson",
        output_filepath="data/raw/Munich_raw.csv",
        city="Munich",
    )

df_dublin = geojson_to_raw_csv(
        input_filepath="data/raw/Dublin.geojson",
        output_filepath="data/raw/Dublin_raw.csv",
        city="Dublin",
    )

# due to language differences and specifics of local mapping, the value can be stored in one of multiple columns.
# standardize the structure of city datasets before merging them
def standardize_city_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # there are empty str, replace with NA in order to use .fillna later
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    standardized = pd.DataFrame(index=df.index)

    # basic info about the entity
    standardized["city"] = df["city_source"]
    standardized["osm_id"] = df["@id"]
    standardized["geometry"] = df["geometry"]
    standardized["name"] = df["name"]

    # address info
    standardized["street"] = df["addr:street"]
    standardized["house_number"] = df["addr:housenumber"]
    standardized["postcode"] = df["addr:postcode"]
    standardized["address_city"] = df["addr:city"]

    # data that can help to filter the beer-related entities
    standardized["amenity"] = df["amenity"]
    # ["bar"] only available in Prague and Minuch
    standardized["bar"] = (
        df["bar"] if "bar" in df.columns else pd.NA
    )
    # ["beer"] only available in Prague
    standardized["beer"] = (
        df["beer"] if "beer" in df.columns else pd.NA
    )
    # ["beer_garden"] only available in Prague
    standardized["beer_garden"] = (
        df["beer_garden"] if "beer_garden" in df.columns else pd.NA
    )
    standardized["brewery"] = df["brewery"]
    standardized["drink_beer"] = df["drink:beer"]
    standardized["microbrewery"] = df["microbrewery"]

    # contact info
    # check whether the data is available in a column, if not, replace it with the data from another one
    standardized["website"] = df["website"].fillna(
        df["contact:website"]
    )

    standardized["phone"] = df["phone"].fillna(
        df["contact:phone"]
    )

    standardized["email"] = df["email"].fillna(
        df["contact:email"]
    )

    standardized["facebook"] = df["contact:facebook"]

    if "facebook" in df.columns:
        standardized["facebook"] = (
            standardized["facebook"]
            .fillna(df["facebook"])
        )

    standardized["instagram"] = df["contact:instagram"]

    if "instagram" in df.columns:
        standardized["instagram"] = (
            standardized["instagram"]
            .fillna(df["instagram"])
        )

    # description
    standardized["description"] = df["description"]

    description_columns = [
        "description:cs",
        "description:en",
        "description:de",
        "description:it",
    ]

    for column in description_columns:
        if column in df.columns:
            standardized["description"] = (
                standardized["description"]
                .fillna(df[column])
            )

    # listing enriching info
    standardized["opening_hours"] = df["opening_hours"]
    standardized["wheelchair"] = df["wheelchair"]
    standardized["toilets_wheelchair"] = df["toilets:wheelchair"]
    standardized["smoking"] = df["smoking"]
    standardized["min_age"] = df["min_age"]

    # payment info. there are numerous methods available so we count the non-null value to standardize the outcome
    payment_columns = [
        column
        for column in df.columns
        if column.startswith("payment:")
    ]

    standardized["payment_methods_count"] = (
        df[payment_columns].notna().sum(axis=1)
    )

    # this will help to filter irrelevant geographic objects
    standardized["highway"] = (
        df["highway"] if "highway" in df.columns else pd.NA
    )

    return standardized

# apply function to all 3 dfs
df_prague_standardized = standardize_city_df(df_prague)
df_munich_standardized = standardize_city_df(df_munich)
df_dublin_standardized = standardize_city_df(df_dublin)

# verify if all data has been processed successfully
# check the df length for Prague
if len(df_prague_standardized) == len(df_prague):
    print("Prague: row count preserved.")
else:
    print("Prague: row count mismatch.")

# check the df length for Munich
if len(df_munich_standardized) == len(df_munich):
    print("Munich: row count preserved.")
else:
    print("Munich: row count mismatch.")

# check the df length for Dublin
if len(df_dublin_standardized) == len(df_dublin):
    print("Dublin: row count preserved.")
else:
    print("Dublin: row count mismatch.")

# save standardized datasets to CSVs
df_prague_standardized.to_csv("data/processed/Prague_standardized.csv", index=False, encoding="utf-8")
df_munich_standardized.to_csv("data/processed/Munich_standardized.csv", index=False, encoding="utf-8")
df_dublin_standardized.to_csv("data/processed/Dublin_standardized.csv", index=False, encoding="utf-8")

# concat dfs into one file
df_all_cities = pd.concat(
    [
        df_prague_standardized,
        df_munich_standardized,
        df_dublin_standardized,
    ],
    ignore_index=True,
)

# check if the merged CSV returns an expected number of rows
rows_number_to_return = (
    len(df_prague_standardized)
    + len(df_munich_standardized)
    + len(df_dublin_standardized)
)

if len(df_all_cities) == rows_number_to_return:
    print("df_all_cities merge completed successfully.")
else:
    print("df_all_cities merge failed.")

# save merged CSV
df_all_cities.to_csv("data/processed/All_cities_standardized.csv", index=False, encoding="utf-8",)

# a tag is "positive" only if it's present AND not explicitly set to "no"
def has_positive_tag(series: pd.Series) -> pd.Series:
    return series.notna() & (series.astype(str).str.strip().str.lower() != "no")

amenity_match = (
    df_all_cities["amenity"]
    .isin(["biergarten", "bar", "pub"])
)

beer_category_match = (
    has_positive_tag(df_all_cities["bar"])
    | has_positive_tag(df_all_cities["beer"])
    | has_positive_tag(df_all_cities["beer_garden"])
    | has_positive_tag(df_all_cities["brewery"])
    | has_positive_tag(df_all_cities["drink_beer"])
    | has_positive_tag(df_all_cities["microbrewery"])
)


# manually validated beer-related places
# for more info on validation check eda.py
manual_include_osm_ids = {
    "node/8638179435",
    "way/525723347",
    "node/8638179434",
    "node/4243300486",
    "node/13787014302",
    "node/1722092770",
    "node/8873226491",
    "node/1946542433",
    "node/11039851463",
    "relation/14981653",
    "node/330643006",
    "node/12088464755",
    "node/3620482763",
    "node/13435036495",
    "node/305079222",
    "node/3761143840",
    "node/3900293198",
    "node/3393593685",
    "node/3740683728",
    "node/11936540091",
    "node/3278080262",
    "way/379800530",
    "node/350569091",
    "node/611414004",
    "node/6622281477",
    "node/3726743656",
    "node/6924755785",
    "node/296760797",
    "way/62147117",
    "node/13423839001",
    "node/5996532329",
    "node/585219608",
    "node/296778915",
    "node/1096063711",
    "node/5116818696",
}

manual_include_match = (
    df_all_cities["osm_id"]
    .isin(manual_include_osm_ids)
)

# final beer-related filter
beer_filter = (
    amenity_match
    | beer_category_match
    | manual_include_match
)


# save to one df
df_beer_places = df_all_cities[beer_filter].copy()

# check if the number of rows and amentiy distribution make sense
# output: rows are ok, amenity returns 21 records with NaN. those were affected by the combination with other categories
print("All places:", len(df_all_cities))
print("Beer places (before deduplication):", len(df_beer_places))

#print(df_beer_places["amenity"].value_counts(dropna=False))

# make cross-check between amenity=restaurant and filtered_beer_places
'''
print(
    df_beer_places.loc[
        df_beer_places["amenity"] == "restaurant",
        [
            "city",
            "name",
            "amenity",
            "bar",
            "beer",
            "beer_garden",
            "brewery",
            "drink_beer",
            "microbrewery",
        ]
    ].to_string(index=False)
)
'''

# remove records with missing or empty names
df_beer_places = df_beer_places[
    df_beer_places["name"].notna()
    & (df_beer_places["name"].str.strip() != "")
].copy()

print(f"Records after removing missing names: {len(df_beer_places)}")

# duplicates confirmed by manual review. dict - duplicate: canonical
canonical_mapping = {
    # Dublin
    "way/1080799552": "node/12101176582",   # Love Tempo
    "way/269759932": "way/269759933",       # The Bailey
    "way/657456424": "way/233516827",       # The Silver Penny
    "way/1022471505": "way/296153007",      # The Full Shilling

    # Munich
    "node/253247251": "node/496923895",     # Forschungsbrauerei
    "node/409497629": "node/2335083230",    # München '72
    "node/307528347": "way/126131342",      # Paulaner Bräuhaus
    "node/2255943604": "node/12913994303",  # el Tato
    "node/277253196": "node/508830396",     # Isarflimmern
    "way/821822141": "node/409497601",      # M. C. Mueller
    "node/13755435903": "way/502190647",    # Olympia-Alm

    # Prague
    "node/3247900661": "way/1084115534",    # KD Barikádníků
    "node/7116196387": "node/13653818501",  # Bohemia Goose
    "node/9726178174": "node/4958181423",   # Crazy Daisy
    "node/7102061556": "node/13013839901",  # My People Bar
    "node/1409474794": "node/13595671942",  # Na Hřišti
    "node/5649349113": "node/3019724721",   # U Sudu
}

# remove manually confirmed duplicates
df_beer_places = df_beer_places[
    ~df_beer_places["osm_id"].isin(canonical_mapping.keys())
].copy()

print(f"Records after removing name&city duplicates: {len(df_beer_places)}")

remaining_duplicates = (
    df_beer_places["osm_id"]
    .isin(canonical_mapping.keys())
    .sum()
)

print(f"Remaining duplicated osm_ids: {remaining_duplicates}")

# final check
print(f"All OSM objects: {len(df_all_cities)}")
print(f"Beer-related places: {len(df_beer_places)}")
print(df_beer_places.groupby("city").size())

# save df_beer_places to a csv
df_beer_places.to_csv(
    "data/processed/beer_places.csv",
    index=False,
    encoding="utf-8"
)



from analysis import calculate_listing_score, calculate_city_scores
from visualization import create_visualizations
from database import upload_beer_places


# upload final cleaned dataset to PostgreSQL
upload_beer_places(df_beer_places)

# run analysis
df_beer_places_scored = calculate_listing_score(
    df_beer_places
)

city_scores = calculate_city_scores(
    df_beer_places_scored
)

# add visualizations
create_visualizations(
    city_scores
)
