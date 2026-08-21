import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CLEAN CSS
# ONLY KPI CARDS ARE CUSTOMIZED
# =========================================================

st.markdown("""
<style>

/* =========================
   KPI CARDS
========================= */

[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e1e1e1 !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}


/* KPI LABEL */

[data-testid="stMetricLabel"] {
    color: #000000 !important;
    opacity: 1 !important;
}


/* KPI NUMBER */

[data-testid="stMetricValue"] {
    color: #000000 !important;
    opacity: 1 !important;
}


/* KPI DELTA */

[data-testid="stMetricDelta"] {
    opacity: 1 !important;
}


/* =========================
   DOWNLOAD BUTTON
========================= */

.stDownloadButton button {
    font-weight: 600 !important;
}


/* =========================
   TABLE
========================= */

[data-testid="stDataFrame"] {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_name = "AllMoviesDetails_20MB.xlsx"

    data = pd.read_excel(
        file_name,
        engine="openpyxl"
    )

    # Numeric columns
    numeric_columns = [
        "budget",
        "revenue",
        "runtime",
        "popularity",
        "vote_average",
        "vote_count"
    ]

    for col in numeric_columns:

        if col in data.columns:

            data[col] = pd.to_numeric(
                data[col],
                errors="coerce"
            )

    # Release date
    if "release_date" in data.columns:

        data["release_date"] = pd.to_datetime(
            data["release_date"],
            errors="coerce"
        )

        data["release_year"] = (
            data["release_date"].dt.year
        )

    # Text columns
    text_columns = [
        "title",
        "original_title",
        "genres",
        "status",
        "original_language"
    ]

    for col in text_columns:

        if col in data.columns:

            data[col] = (
                data[col]
                .fillna("Unknown")
                .astype(str)
            )

    return data


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "❌ AllMoviesDetails_20MB.xlsx was not found."
    )

    st.info(
        "Keep AllMoviesDetails_20MB.xlsx "
        "in the same folder as app3.py."
    )

    st.stop()

except Exception as e:

    st.error(
        f"❌ Error loading Excel file: {e}"
    )

    st.stop()


# =========================================================
# TITLE
# =========================================================

st.title("🎬 Movie Analytics Dashboard")

st.subheader(
    "Interactive Movie Data Analysis & Exploration"
)

st.caption(
    f"📊 {len(df):,} movies • {len(df.columns)} columns"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎛️ Dashboard Filters")


# =========================================================
# YEAR FILTER
# =========================================================

st.sidebar.subheader("📅 Release Year")

if "release_year" in df.columns:

    valid_years = df["release_year"].dropna()

    if len(valid_years) > 0:

        min_year = int(valid_years.min())
        max_year = int(valid_years.max())

        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )

    else:

        year_range = None

else:

    year_range = None


# =========================================================
# LANGUAGE
# =========================================================

st.sidebar.subheader("🌍 Language")

if "original_language" in df.columns:

    languages = sorted(
        df["original_language"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_languages = st.sidebar.multiselect(
        "Original Language",
        languages
    )

else:

    selected_languages = []


# =========================================================
# STATUS
# =========================================================

st.sidebar.subheader("🎥 Movie Status")

if "status" in df.columns:

    statuses = sorted(
        df["status"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_status = st.sidebar.multiselect(
        "Status",
        statuses
    )

else:

    selected_status = []


# =========================================================
# RATING
# =========================================================

st.sidebar.subheader("⭐ Rating")

rating_range = st.sidebar.slider(
    "Rating Range",
    min_value=0.0,
    max_value=10.0,
    value=(0.0, 10.0),
    step=0.1
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if year_range is not None:

    filtered_df = filtered_df[
        filtered_df["release_year"].between(
            year_range[0],
            year_range[1]
        )
    ]


if selected_languages:

    filtered_df = filtered_df[
        filtered_df["original_language"].isin(
            selected_languages
        )
    ]


if selected_status:

    filtered_df = filtered_df[
        filtered_df["status"].isin(
            selected_status
        )
    ]


if "vote_average" in filtered_df.columns:

    filtered_df = filtered_df[
        filtered_df["vote_average"].between(
            rating_range[0],
            rating_range[1]
        )
    ]


# =========================================================
# DATASET OVERVIEW
# =========================================================

st.header("📊 Dataset Overview")


c1, c2, c3, c4, c5 = st.columns(5)


# Total movies

c1.metric(
    "🎬 Total Movies",
    f"{len(filtered_df):,}"
)


# Average rating

if "vote_average" in filtered_df.columns:

    avg_rating = filtered_df["vote_average"].mean()

else:

    avg_rating = 0


c2.metric(
    "⭐ Average Rating",
    f"{avg_rating:.2f}"
)


# Average popularity

if "popularity" in filtered_df.columns:

    avg_popularity = filtered_df["popularity"].mean()

else:

    avg_popularity = 0


c3.metric(
    "🔥 Avg Popularity",
    f"{avg_popularity:.2f}"
)


# Revenue

if "revenue" in filtered_df.columns:

    total_revenue = filtered_df["revenue"].sum()

else:

    total_revenue = 0


c4.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.0f}"
)


# Runtime

if "runtime" in filtered_df.columns:

    avg_runtime = filtered_df["runtime"].mean()

else:

    avg_runtime = 0


c5.metric(
    "⏱️ Avg Runtime",
    f"{avg_runtime:.0f} min"
)


# =========================================================
# ADDITIONAL STATISTICS
# =========================================================

st.subheader("📌 Additional Statistics")


s1, s2, s3, s4 = st.columns(4)


# Highest rating

highest_rating = (
    filtered_df["vote_average"].max()
    if "vote_average" in filtered_df.columns
    else 0
)

s1.metric(
    "🏆 Highest Rating",
    f"{highest_rating:.2f}"
)


# Highest popularity

highest_popularity = (
    filtered_df["popularity"].max()
    if "popularity" in filtered_df.columns
    else 0
)

s2.metric(
    "🔥 Highest Popularity",
    f"{highest_popularity:.2f}"
)


# Average votes

average_votes = (
    filtered_df["vote_count"].mean()
    if "vote_count" in filtered_df.columns
    else 0
)

s3.metric(
    "👥 Average Votes",
    f"{average_votes:,.0f}"
)


# Missing values

missing_values = int(
    filtered_df.isna().sum().sum()
)

s4.metric(
    "⚠️ Missing Values",
    f"{missing_values:,}"
)


st.divider()


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Trends",
    "⭐ Ratings",
    "🎭 Genres",
    "💰 Finance",
    "🌍 Languages",
    "📋 Dataset"
])


# =========================================================
# TRENDS
# =========================================================

with tab1:

    st.header("📈 Movie Release Trends")


    if "release_year" in filtered_df.columns:

        yearly = (
            filtered_df
            .dropna(subset=["release_year"])
            .groupby("release_year")
            .size()
            .reset_index(name="Movies")
        )

        fig = px.line(
            yearly,
            x="release_year",
            y="Movies",
            markers=True,
            title="🎬 Movies Released by Year"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    if {
        "release_year",
        "vote_average"
    }.issubset(filtered_df.columns):

        yearly_rating = (
            filtered_df
            .dropna(
                subset=[
                    "release_year",
                    "vote_average"
                ]
            )
            .groupby("release_year")[
                "vote_average"
            ]
            .mean()
            .reset_index()
        )

        fig = px.line(
            yearly_rating,
            x="release_year",
            y="vote_average",
            markers=True,
            title="⭐ Average Rating by Year"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# RATINGS
# =========================================================

with tab2:

    st.header("⭐ Rating Analysis")

    r1, r2 = st.columns(2)


    # Rating distribution

    with r1:

        if "vote_average" in filtered_df.columns:

            fig = px.histogram(
                filtered_df,
                x="vote_average",
                nbins=30,
                title="⭐ Rating Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Votes vs rating

    with r2:

        required = {
            "vote_count",
            "vote_average"
        }

        if required.issubset(filtered_df.columns):

            sample = filtered_df.sample(
                min(5000, len(filtered_df)),
                random_state=42
            )

            fig = px.scatter(
                sample,
                x="vote_count",
                y="vote_average",
                hover_name=(
                    "title"
                    if "title" in sample.columns
                    else None
                ),
                title="👥 Vote Count vs Rating"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    st.subheader("🏆 Top Rated Movies")


    if {
        "title",
        "vote_average",
        "vote_count"
    }.issubset(filtered_df.columns):

        top_movies = (
            filtered_df
            .sort_values(
                "vote_average",
                ascending=False
            )
            [
                [
                    "title",
                    "vote_average",
                    "vote_count"
                ]
            ]
            .head(20)
        )

        st.dataframe(
            top_movies,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# GENRES
# =========================================================

with tab3:

    st.header("🎭 Genre Analysis")


    if "genres" in filtered_df.columns:

        genres = (
            filtered_df["genres"]
            .fillna("Unknown")
            .astype(str)
            .str.replace(
                ",",
                "|",
                regex=False
            )
            .str.split("|")
            .explode()
            .str.strip()
        )

        genre_counts = (
            genres
            .replace("", "Unknown")
            .value_counts()
            .head(20)
            .reset_index()
        )

        genre_counts.columns = [
            "Genre",
            "Movies"
        ]


        g1, g2 = st.columns(2)


        with g1:

            fig = px.bar(
                genre_counts.sort_values(
                    "Movies"
                ),
                x="Movies",
                y="Genre",
                orientation="h",
                title="🎭 Most Common Genres"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        with g2:

            fig = px.pie(
                genre_counts.head(10),
                values="Movies",
                names="Genre",
                title="🎬 Top 10 Genres"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        st.subheader("📋 Genre Statistics")

        st.dataframe(
            genre_counts,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# FINANCE
# =========================================================

with tab4:

    st.header("💰 Financial Analysis")


    if {
        "budget",
        "revenue"
    }.issubset(filtered_df.columns):

        finance = filtered_df[
            (filtered_df["budget"] > 0) &
            (filtered_df["revenue"] > 0)
        ].copy()


        finance["profit"] = (
            finance["revenue"]
            - finance["budget"]
        )


        f1, f2, f3 = st.columns(3)


        f1.metric(
            "💵 Total Budget",
            f"${finance['budget'].sum():,.0f}"
        )


        f2.metric(
            "💰 Total Revenue",
            f"${finance['revenue'].sum():,.0f}"
        )


        f3.metric(
            "📈 Total Profit",
            f"${finance['profit'].sum():,.0f}"
        )


        if len(finance) > 0:

            sample = finance.sample(
                min(5000, len(finance)),
                random_state=42
            )


            fig = px.scatter(
                sample,
                x="budget",
                y="revenue",
                hover_name=(
                    "title"
                    if "title" in sample.columns
                    else None
                ),
                title="💰 Budget vs Revenue"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.subheader(
                "🏆 Most Profitable Movies"
            )


            columns = [
                c
                for c in [
                    "title",
                    "budget",
                    "revenue",
                    "profit"
                ]
                if c in finance.columns
            ]


            top_profit = (
                finance
                .sort_values(
                    "profit",
                    ascending=False
                )
                [columns]
                .head(20)
            )


            st.dataframe(
                top_profit,
                use_container_width=True,
                hide_index=True
            )


# =========================================================
# LANGUAGES
# =========================================================

with tab5:

    st.header("🌍 Language Analysis")


    if "original_language" in filtered_df.columns:

        language_counts = (
            filtered_df[
                "original_language"
            ]
            .value_counts()
            .head(20)
            .reset_index()
        )

        language_counts.columns = [
            "Language",
            "Movies"
        ]


        fig = px.bar(
            language_counts,
            x="Language",
            y="Movies",
            title="🌍 Movies by Original Language"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.subheader(
            "📋 Language Statistics"
        )

        st.dataframe(
            language_counts,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# DATASET EXPLORER
# =========================================================

with tab6:

    st.header("📋 Movie Dataset Explorer")


    search = st.text_input(
        "🔎 Search Movie Title"
    )


    display_df = filtered_df.copy()


    if search and "title" in display_df.columns:

        display_df = display_df[
            display_df["title"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    st.write(
        f"Showing **{len(display_df):,}** movies"
    )


    preferred_columns = [
        "id",
        "title",
        "original_title",
        "release_date",
        "release_year",
        "genres",
        "original_language",
        "runtime",
        "vote_average",
        "vote_count",
        "popularity",
        "budget",
        "revenue",
        "status"
    ]


    available_columns = [
        c
        for c in preferred_columns
        if c in display_df.columns
    ]


    st.dataframe(
        display_df[available_columns],
        use_container_width=True,
        height=550,
        hide_index=True
    )


    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        "📥 Download Filtered CSV",
        data=csv_data,
        file_name="movie_analysis_filtered.csv",
        mime="text/csv"
    )


# =========================================================
# CORRELATION
# =========================================================

st.divider()

st.header("🔗 Correlation Analysis")


correlation_columns = [
    "budget",
    "revenue",
    "runtime",
    "popularity",
    "vote_average",
    "vote_count"
]


available_corr = [
    c
    for c in correlation_columns
    if c in filtered_df.columns
]


if len(available_corr) >= 2:

    correlation = (
        filtered_df[
            available_corr
        ]
        .corr()
    )


    fig = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="🔗 Movie Variable Correlation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DATA QUALITY
# =========================================================

st.divider()

st.header("🧹 Data Quality Analysis")


missing = (
    df.isna()
    .sum()
    .sort_values(
        ascending=False
    )
    .reset_index()
)


missing.columns = [
    "Column",
    "Missing Values"
]


missing["Missing %"] = (
    missing["Missing Values"]
    / len(df)
    * 100
).round(2)


st.dataframe(
    missing,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎬 Movie Analytics Dashboard • "
    "Python • Streamlit • Pandas • Plotly"
)
