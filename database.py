import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def upload_beer_places(df: pd.DataFrame) -> None:
    columns = [
        "city",
        "osm_id",
        "geometry",
        "name",
        "street",
        "house_number",
        "postcode",
        "address_city",
        "amenity",
        "bar",
        "beer",
        "beer_garden",
        "brewery",
        "drink_beer",
        "microbrewery",
        "website",
        "phone",
        "email",
        "facebook",
        "instagram",
        "description",
        "opening_hours",
        "wheelchair",
        "toilets_wheelchair",
        "smoking",
        "min_age",
        "payment_methods_count",
        "highway",
    ]

    df_to_upload = df[columns].copy()

    df_to_upload = df_to_upload.astype(object).where(
        pd.notna(df_to_upload),
        None
    )

    insert_query = """
        INSERT INTO beer_places (
            city,
            osm_id,
            geometry,
            name,
            street,
            house_number,
            postcode,
            address_city,
            amenity,
            bar,
            beer,
            beer_garden,
            brewery,
            drink_beer,
            microbrewery,
            website,
            phone,
            email,
            facebook,
            instagram,
            description,
            opening_hours,
            wheelchair,
            toilets_wheelchair,
            smoking,
            min_age,
            payment_methods_count,
            highway
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (osm_id) DO NOTHING;
    """

    records = list(
        df_to_upload.itertuples(
            index=False,
            name=None
        )
    )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.executemany(insert_query, records)
        connection.commit()

        print(
            f"{len(records)} beer places uploaded to PostgreSQL."
        )
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()