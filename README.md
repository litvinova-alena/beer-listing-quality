# Beer Listing Quality Analysis

## Overview

This project analyzes the quality and completeness of beer-related place listings
across Prague, Munich, and Dublin using OpenStreetMap data.

The analysis focuses on identifying relevant beer-related venues, standardizing
data across cities, removing duplicate or irrelevant records, and evaluating
the completeness of listing information.

## Data

The project uses GeoJSON datasets for three cities:

- Prague
- Munich
- Dublin

The raw datasets contain OpenStreetMap objects and their associated tags.
Because the available attributes differ between cities, the datasets are
standardized before the analysis.

## Methodology

The analysis consists of several stages:

1. Load the raw GeoJSON datasets.
2. Convert the geographic data into a tabular format.
3. Identify attributes shared across the three city datasets.
4. Standardize city-specific fields into a common structure.
5. Identify beer-related places using:
   - amenity type;
   - beer-related OpenStreetMap tags;
   - brewery and microbrewery information;
   - beer-related venue names;
   - manual validation where necessary.
6. Remove records with missing names and manually confirmed duplicates.
7. Calculate listing quality metrics.
8. Aggregate the results by city.
9. Generate visualizations for the city comparison.

## Project Structure

```text
beer-listing-quality/
├── data/
│   ├── raw/
│   └── processed/
├── main.py
├── eda.py
├── database.py
├── analysis.py
├── visualization.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```
## Listing Quality Score

Each beer-related place receives a Listing Quality Score from 0 to 100.

### Discoverability — 30 points

- Primary category (`amenity`) — 20 points
- Additional beer-related classification — 10 points

### Information Completeness — 70 points

| Attribute | Points |
|---|---:|
| Address | 20 |
| Website | 12 |
| Opening hours | 12 |
| Phone | 8 |
| Description | 5 |
| Accessibility | 5 |
| Social media | 3 |
| Email | 2 |
| Other information | 3 |
| **Total** | **70** |

The final score is calculated as:

```text
Listing Quality Score =
Discoverability Score + Information Completeness Score
```

## Data Quality Considerations

OpenStreetMap data is community-generated and therefore varies in completeness
and tagging conventions between cities.

Several additional validation steps are used in this project, including:

combining alternative tags that represent the same type of information;
using multiple signals to identify beer-related places;
manually reviewing ambiguous name-based matches;
manually validating potential duplicate venues.

These steps reduce obvious inconsistencies but do not guarantee that all
relevant venues are present or correctly classified.

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root with your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=beer_places
DB_USER=your_user
DB_PASSWORD=your_password
```

## Running the Project

Run the complete pipeline with:

```bash
python main.py
```

## Results

| City   | Places | Mean Score | Median Score | Min Score | Max Score | Mean Discoverability | Mean Completeness |
|--------|-------:|-----------:|--------------:|----------:|----------:|-----------------------:|---------------------:|
| Munich |    661 |      51.74 |          52.0 |      13.0 |      96.0 |                  21.45 |                30.29 |
| Dublin |    548 |      48.94 |          48.0 |      12.0 |      91.0 |                  20.84 |                28.10 |
| Prague |    972 |      43.61 |          40.0 |       0.0 |      90.5 |                  19.96 |                23.66 |

**Munich** has the highest average listing quality score (51.74), leading on
both discoverability and information completeness. 

**Dublin** follows closely behind. 

**Prague**, despite having the largest number of identified places
(972), has the lowest average score — driven mainly by weaker information
completeness (23.66 vs. 30.29 in Munich) — indicating that a large share of
Prague listings are missing key details such as address, website, or opening
hours. Prague's minimum score of 0.0 suggests at least one listing has almost
no usable information beyond its beer-related classification.



## Visualizations
City scores comparison
![City scores comparison](data/processed/visualizations/city_scores_comparison.png)


Population vs area
![Population vs area](data/processed/visualizations/population_area_bubble.png)

