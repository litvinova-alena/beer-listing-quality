import pandas as pd

def calculate_listing_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # 1. DISCOVERABILITY SCORE: max 30 points
    # primary OSM category: max 20 points
    df["score_primary_category"] = (
        df["amenity"]
        .isin(["pub", "bar", "biergarten"])
        .astype(int)
        * 20
    )

    # additional beer-related classification: max 10 points
    # we award the points once if at least one additional beer-related tag is present.
    beer_category_columns = [
        "bar",
        "beer",
        "beer_garden",
        "brewery",
        "drink_beer",
        "microbrewery",
    ]

    df["score_beer_classification"] = (
            df[beer_category_columns]
            .apply(lambda col: col.notna() & (col.astype(str).str.lower() != "no"))
            .any(axis=1)
            .astype(int)
            * 10
    )

    df["discoverability_score"] = (
        df["score_primary_category"]
        + df["score_beer_classification"]
    )

    # 2. INFORMATION COMPLETENESS SCORE: max 70 points
    # address: max 20 points
    df["score_address"] = (
        df["street"].notna().astype(int) * 7
        + df["house_number"].notna().astype(int) * 7
        + df["postcode"].notna().astype(int) * 3
        + df["address_city"].notna().astype(int) * 3
    )

    # website: max 12 points
    df["score_website"] = (
        df["website"].notna().astype(int) * 12
    )

    # opening hours: max 12 points
    df["score_opening_hours"] = (
        df["opening_hours"].notna().astype(int) * 12
    )

    # phone: max 8 points
    df["score_phone"] = (
        df["phone"].notna().astype(int) * 8
    )

    # description: max 5 points
    df["score_description"] = (
        df["description"].notna().astype(int) * 5
    )

    # accessibility: max 5 points
    df["score_accessibility"] = (
        df["wheelchair"].notna().astype(int) * 3
        + df["toilets_wheelchair"].notna().astype(int) * 2
    )

    # social media: max 3 points
    df["score_social_media"] = (
        df["facebook"].notna().astype(int) * 1.5
        + df["instagram"].notna().astype(int) * 1.5
    )

    # email: max 2 points
    df["score_email"] = (
        df["email"].notna().astype(int) * 2
    )

    # other useful information: max 3 points
    df["score_other"] = (
        (df["payment_methods_count"] > 0).astype(int) * 1
        + df["smoking"].notna().astype(int) * 1
        + df["min_age"].notna().astype(int) * 1
    )

    df["information_completeness_score"] = (
        df["score_address"]
        + df["score_website"]
        + df["score_opening_hours"]
        + df["score_phone"]
        + df["score_description"]
        + df["score_accessibility"]
        + df["score_social_media"]
        + df["score_email"]
        + df["score_other"]
    )

    # 3. FINAL LISTING QUALITY SCORE: max 100 points
    df["listing_quality_score"] = (
        df["discoverability_score"]
        + df["information_completeness_score"]
    )

    return df



# calculate score for each city
def calculate_city_scores(
    df_beer_places_scored: pd.DataFrame
    ) -> pd.DataFrame:

    # ensure min and max values are within the expected range. outcome: all is valid
    #print(df_beer_places_scored["listing_quality_score"].describe())

    city_scores = (
        df_beer_places_scored
        .groupby("city")
        .agg(
            places=("osm_id", "count"),
            mean_score=("listing_quality_score", "mean"),
            median_score=("listing_quality_score", "median"),
            min_score=("listing_quality_score", "min"),
            max_score=("listing_quality_score", "max"),
            mean_discoverability=("discoverability_score", "mean"),
            mean_completeness=(
                "information_completeness_score",
                "mean"
            ),
        )
        .round(2)
        .sort_values(
            "mean_score",
            ascending=False
        )
    )

    print(city_scores)

    return city_scores

