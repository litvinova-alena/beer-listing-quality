import matplotlib.pyplot as plt
import pandas as pd
import os

# the 1st viz combines 3 charts: 1. Average Listing Quality Score, 2. Average Discoverability Score,
# and 3. Average Information Completeness Score

def create_visualizations(
    city_scores: pd.DataFrame,
        output_dir: str = "data/processed/visualizations",
) -> None:
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(
        nrows=1,
        ncols=3,
        figsize=(18, 6)
    )

    # 1. Average Listing Quality Score
    bars = axes[0].bar(
        city_scores.index,
        city_scores["mean_score"],
        color="#2E7D32",
        edgecolor="black",
        linewidth=0.8
    )

    for bar in bars:
        height = bar.get_height()

        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    axes[0].set_title(
        "Average Beer Place Listing Quality Score by City",
        fontsize=12,
        fontweight="bold",
        pad=15
    )

    axes[0].set_xlabel(
        "City",
        fontsize=12
    )

    axes[0].set_ylabel(
        "Average score (0–100)",
        fontsize=12
    )

    axes[0].set_ylim(
        0,
        100
    )

    axes[0].grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    # 2. Average Discoverability Score
    bars = axes[1].bar(
        city_scores.index,
        city_scores["mean_discoverability"],
        color="#2E7D32",
        edgecolor="black",
        linewidth=0.8
    )

    for bar in bars:
        height = bar.get_height()

        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.4,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    axes[1].set_title(
        "Average Discoverability Score by City",
        fontsize=12,
        fontweight="bold",
        pad=15
    )

    axes[1].set_xlabel(
        "City",
        fontsize=12
    )

    axes[1].set_ylabel(
        "Average score (0–30)",
        fontsize=12
    )

    axes[1].set_ylim(
        0,
        30
    )

    axes[1].grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)

    # 3. Average Information Completeness Score
    bars = axes[2].bar(
        city_scores.index,
        city_scores["mean_completeness"],
        color="#2E7D32",
        edgecolor="black",
        linewidth=0.8
    )

    for bar in bars:
        height = bar.get_height()

        axes[2].text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.8,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    axes[2].set_title(
        "Average Information Completeness Score by City",
        fontsize=12,
        fontweight="bold",
        pad=15
    )

    axes[2].set_xlabel(
        "City",
        fontsize=12
    )

    axes[2].set_ylabel(
        "Average score (0–70)",
        fontsize=12
    )

    axes[2].set_ylim(
        0,
        70
    )

    axes[2].grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    axes[2].spines["top"].set_visible(False)
    axes[2].spines["right"].set_visible(False)


    plt.tight_layout(
        w_pad=3
    )

    scores_comparison_path = os.path.join(
        output_dir, "city_scores_comparison.png"
    )

    fig.savefig(
        scores_comparison_path,
        dpi=150,
        bbox_inches="tight"
    )

    #plt.show()

    # the 2nd viz shows a scatter plot where x = population, y = area, bubble size = N of beer places

    # city characteristics df
    city_info = pd.DataFrame({
        "city": ["Prague", "Dublin", "Munich"],
        "population": [1405000, 554554, 1561000],
        "area_km2": [496, 318, 311]
    }).set_index("city")

    city_scores = city_scores.join(city_info)
    #print(city_scores)

    bubble_fig = plt.figure(figsize=(9,7))

    bubble_size = city_scores["places"] * 3

    plt.scatter(
        city_scores["population"],
        city_scores["area_km2"],
        s=bubble_size,
        color="#2E7D32",
        edgecolors="black",
        linewidth=1,
        alpha=0.75
    )

    for city, row in city_scores.iterrows():
        plt.annotate(
            f"{int(row['places'])} places",
            (row["population"], row["area_km2"]),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=11
        )

    plt.title(
        "Distribution of Beer Places by City Population and Area",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    plt.xlabel(
        "Population",
        fontsize=12
    )

    plt.ylabel(
        "City area (km²)",
        fontsize=12
    )

    plt.grid(
        linestyle="--",
        alpha=0.4
    )

    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    bubble_path = os.path.join(
        output_dir, "population_area_bubble.png"
    )

    bubble_fig.savefig(
        bubble_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()

'''
Prague leads in the total number of identified places, 
Munich combines a large population with a comparatively compact geographical area, 
while Dublin has fewer establishments in absolute terms but a high concentration relative to its population.
'''