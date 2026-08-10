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
├── analysis.py
├── database.py
├── visualization.py
├── requirements.txt
└── README.md
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

## Results
TBA

## Visualizations

