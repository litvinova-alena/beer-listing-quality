import pandas as pd

# explore datasets whether they have the same number of column
def compare_dataset_shapes(
        df_prague: pd.DataFrame,
        df_munich: pd.DataFrame,
        df_dublin: pd.DataFrame,
) -> pd.DataFrame:

    dataset_shapes = pd.DataFrame(
        {
            "city": ["Prague", "Munich", "Dublin"],
            "rows": [
                df_prague.shape[0],
                df_munich.shape[0],
                df_dublin.shape[0]
            ],
            "columns": [
                df_prague.shape[1],
                df_munich.shape[1],
                df_dublin.shape[1],
            ]
        }
    )

    print(dataset_shapes)

    return dataset_shapes

'''
Outcome:
     city  rows  columns
0  Prague  1204      303
1  Munich   890      341
2  Dublin   628      151
'''

def compare_columns(
    df_prague: pd.DataFrame,
    df_munich: pd.DataFrame,
    df_dublin: pd.DataFrame,
) -> pd.DataFrame:

    # since all DataFrames have different set of columns, we need to find the common ones
    common_columns = (
        set(df_prague.columns)
        & set(df_munich.columns)
        & set(df_dublin.columns)
    )

    common_columns = sorted(common_columns)

    print(f"Common columns: {len(common_columns)}")
    print(common_columns)

    '''
    Outcome: 93 columns
    ['@geometry', '@id', 'access', 'addr:city', 'addr:country', 'addr:floor', 'addr:housename', 'addr:housenumber', 
    'addr:postcode', 'addr:street', 'addr:suburb', 'air_conditioning', 'alt_name', 'amenity', 'brewery', 'building', 
    'building:levels', 'building:part', 'changing_table', 'check_date', 'check_date:opening_hours', 'city_source', 
    'cocktails', 'contact:email', 'contact:facebook', 'contact:instagram', 'contact:phone', 'contact:website', 'craft', 
    'cuisine', 'description', 'diet:vegan', 'diet:vegetarian', 'disused:amenity', 'drink:beer', 'drive_through', 'email',
     'fax', 'fixme', 'food', 'geometry', 'id', 'indoor_seating', 'internet_access', 'internet_access:fee', 'landuse', 
     'layer', 'level', 'lgbtq', 'live_music', 'microbrewery', 'min_age', 'name', 'name:en', 'name:zh', 'note', 
     'old_name', 'opening_hours', 'opening_hours:signed', 'operator', 'outdoor_seating', 'payment:cash', 
     'payment:credit_cards', 'payment:debit_cards', 'payment:mastercard', 'payment:visa', 'phone', 'product', 
     'ref:vatin', 'reservation', 'roof:colour', 'roof:material', 'roof:shape', 'shop', 'short_name', 'smoking', 
     'source', 'source_crs', 'sport', 'start_date', 'takeaway', 'toilets', 'toilets:access', 'toilets:wheelchair', 
     'tourism', 'type', 'website', 'website:menu', 'wheelchair', 'wheelchair:description', 'wikidata', 'wikimedia_commons', 
     'wikipedia']
    '''

    # some columns might have a slightly different name but still be useful, so we need to verify if we can apply a rule if any
    all_columns = sorted(
        set(df_prague.columns)
        | set(df_munich.columns)
        | set(df_dublin.columns)
    )

    print(f"All unique columns: {len(all_columns)}")
    '''
    Outcome: All unique columns: 508
    '''

    column_comparison = pd.DataFrame(
        {
            "column_name": all_columns,
        }
    )

    column_comparison["Prague"] = (
        column_comparison["column_name"]
        .isin(df_prague.columns)
    )

    column_comparison["Munich"] = (
        column_comparison["column_name"]
        .isin(df_munich.columns)
    )

    column_comparison["Dublin"] = (
        column_comparison["column_name"]
        .isin(df_dublin.columns)
    )

    print(column_comparison.to_string(index=False))

    '''
    Final list of columns we'll be working with:
    ---COMMON INFO---
    city_source,
    @id, 
    @geometry,
    name,
    ---ADDRESS---
    addr:housenumber, 
    addr:street,
    addr:city
    ---FOR FILTERING PURPOSES---
    amenity,
    bar (for Prague & Munich only),
    beer (for Prague only),
    beer_garden (for Prague only),
    brewery,
    drink:beer,
    microbrewery,
    ---LISTING INFO ASSESSMENT---
    contact:email, 
    email,
    contact:facebook,
    facebook (for Prague only),
    contact:instagram,
    instagram (for Munich only),
    contact:phone,
    phone,
    contact:website,
    website,
    description,
    description:cs (for Prague only),
    description:en (for Prague only),
    description:de (for Munich only),
    description:it (for Dublin only),
    min_age,
    opening_hours,
    payment* (since there is a huge combination of payment methods, we count the present values without looking into them),
    smoking,
    wheelchair,
    toilets:wheelchair,
    highway
    '''

    return column_comparison



# verify that a place is actually related to a beer drinking culture
def inspect_beer_tags(
    df_all_cities: pd.DataFrame
) -> None:
    print(df_all_cities["amenity"].value_counts(dropna=False))
    print(df_all_cities["bar"].value_counts(dropna=False))
    print(df_all_cities["beer"].value_counts(dropna=False))
    print(df_all_cities["beer_garden"].value_counts(dropna=False))
    print(df_all_cities["brewery"].value_counts(dropna=False))
    print(df_all_cities["drink_beer"].value_counts(dropna=False))
    print(df_all_cities["microbrewery"].value_counts(dropna=False))

# a tag is "positive" only if it's present AND not explicitly set to "no"
def has_positive_tag(series: pd.Series) -> pd.Series:
    return series.notna() & (series.astype(str).str.strip().str.lower() != "no")

def inspect_name_only_matches(
    df_all_cities: pd.DataFrame
) -> None:
    amenity_match = (
        df_all_cities["amenity"]
        .isin(["biergarten", "bar", "pub"])
    )

    # EDA showed that for the rest we are interested in all values but NA
    beer_category_match = (
            has_positive_tag(df_all_cities["bar"])
            | has_positive_tag(df_all_cities["beer"])
            | has_positive_tag(df_all_cities["beer_garden"])
            | has_positive_tag(df_all_cities["brewery"])
            | has_positive_tag(df_all_cities["drink_beer"])
            | has_positive_tag(df_all_cities["microbrewery"])
    )
    
    # use the name as an additional signal to find potential beer-related places
    beer_name_pattern = (
        r"\bbeer\b"
        r"|\bbrew"
        r"|\bpivo\b"
        r"|\bpivnice\b"
        r"|\bpivovar"
        r"|\bbier\b"
    )

    name_match = (
            df_all_cities["name"]
            .str.contains(
                beer_name_pattern,
                case=False,
                na=False,
                regex=True,
            )
            & df_all_cities["highway"].isna()
    )

    # identify records found only by the name-based filter
    # these records require manual validation
    name_only_matches = (
            name_match
            & ~amenity_match
            & ~beer_category_match
    )


    print(
        df_all_cities.loc[
            name_only_matches,
            [
                "city",
                "name",
                "osm_id",
                "amenity",
                "bar",
                "beer",
                "beer_garden",
                "brewery",
                "drink_beer",
                "microbrewery",
                "highway",
            ]
        ]
        .sort_values(["city", "name"])
        .to_string(index=False)
    )

# check the duplicates
def inspect_duplicates(
    df_beer_places: pd.DataFrame
) -> None:
    # based on osm_id. output: duplicates and NA values not found
    print(f'osm_id with NA values: {df_beer_places["osm_id"].isna().sum()}')
    print(f'osm_id duplicates: {df_beer_places["osm_id"].duplicated().sum()}')

    # based on geometry. output: duplicates not found
    print(f'geometry duplicates: {df_beer_places["geometry"].duplicated().sum()}')

    # based on name & city combination.
    # output: we've got 40 records => check if the addresses match as well or it's just another branch
    duplicate_names = (
        df_beer_places[
            df_beer_places["name"].notna()
        ]
        .groupby(["city", "name"])
        .size()
        .reset_index(name="count")
    )

    duplicate_names = duplicate_names[
        duplicate_names["count"] > 1
        ]

    print(duplicate_names)


    duplicates = df_beer_places.merge(
        duplicate_names[["city", "name"]],
        on=["city", "name"],
        how="inner",
    )

    print(
        duplicates[
            [
                "city",
                "name",
                "osm_id",
                "amenity",
                "street",
                "house_number",
                "postcode",
                "geometry",
            ]
        ]
        .sort_values(["city", "name"])
        .to_string(index=False)
    )

    '''upon manual verification we found that 
    Love Tempo in Dublin has 1 duplicate record (osm_id: way/1080799552, node/12101176582),
    The Bailey in Dublin has 1 duplicate record (osm_id: way/269759932, way/269759933),
    The Silver Penny in Dublin has 1 duplicate record (osm_id: way/233516827, way/657456424),
    Forschungsbrauerei in Munich has 1 duplicate record (osm_id: node/253247251, node/496923895),
    München '72 in Munich has 1 duplicate record (osm_id: node/409497629, node/2335083230),
    Paulaner Bräuhaus in Munich has 1 duplicate record (osm_id: way/126131342, node/307528347),
    el Tato in Munich has 1 duplicate record (osm_id: node/2255943604, node/12913994303);

    The following bars have either 1 or both records with NaN address. We'll verify the branch existance using Google Maps
    The Willows, - it's a bar chain
    The Full Shilling, - duplicate
    Isarflimmern, - duplicate
    M. C. Mueller, - duplicate
    Olympia-Alm, - duplicate
    KD Barikádníků, - duplicate
    Bohemia Goose, - duplicate
    Crazy Daisy, - duplicate
    Ferdinand, - it's a bar chain
    My People Bar, - duplicate
    Na Hřišti, - duplicate
    Na břehu Rhôny, - it's a bar chain
    Play House, - it's a bar chain
    Sportbar, - it's a bar chain
    Turnovská pivnice, - it's a bar chain
    U Sudu. - duplicate

    '''
