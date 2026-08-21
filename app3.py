import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Movie Data Analysis Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

h1 {
    font-weight: 800;
}

h2 {
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    # IMPORTANT:
    # CSV must be in the SAME GitHub folder as this app.py
    df = pd.read_csv(
        "AllMoviesDetailsCleaned.csv",
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    # Convert numeric columns
    numeric_columns = [
        "budget",
        "revenue",
        "runtime",
        "popularity",
        "vote_average",
        "vote_count"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Date
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(
            df["release_date"],
            errors="coerce"
        )

        df["release_year"] = df[
            "release_date"
        ].dt.year

    # Missing values
    for col in ["title", "genres", "status", "original_language"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


# =========================================================
# TRY LOADING DATA
# =========================================================

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "❌ AllMoviesDetailsCleaned.csv was not found."
    )

    st.markdown("""
    ### Fix this on GitHub

    Your repository should contain:

    ```
    app3/
    ├── app3.py
    ├── AllMoviesDetailsCleaned.csv
    └── requirements.txt
    ```

    Make sure the CSV filename is EXACTLY:

    `AllMoviesDetailsCleaned.csv`

    Then commit and push the CSV to GitHub and restart the Streamlit app.
    """)

    st.stop()

except Exception as e:

    st.error(f"Error loading dataset: {e}")
    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title("🎬 Movie Data Analysis Dashboard")

st.markdown(
    "### Interactive Exploratory Data Analysis of the Movie Dataset"
)

st.caption(
    f"Dataset contains {len(df):,} movie records and "
    f"{len(df.columns)} variables."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎛️ Analysis Controls")

st.sidebar.markdown("### Filters")


# ---------------- YEAR ----------------

if "release_year" in df.columns:

    years = df["release_year"].dropna()

    if len(years) > 0:

        min_year = int(years.min())
        max_year = int(years.max())

        year_range = st.sidebar.slider(
            "Release Year",
            min_year,
            max_year,
            (min_year, max_year)
        )

    else:
        year_range = None

else:
    year_range = None


# ---------------- LANGUAGE ----------------

if "original_language" in df.columns:

    languages = sorted(
        df["original_language"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_languages = st.sidebar.multiselect(
        "Original Language",
        languages
    )

else:

    selected_languages = []


# ---------------- STATUS ----------------

if "status" in df.columns:

    statuses = sorted(
        df["status"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_status = st.sidebar.multiselect(
        "Movie Status",
        statuses
    )

else:

    selected_status = []


# ---------------- RATING ----------------

if "vote_average" in df.columns:

    rating_range = st.sidebar.slider(
        "Rating",
        0.0,
        10.0,
        (0.0, 10.0),
        0.1
    )

else:

    rating_range = (0.0, 10.0)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered = df.copy()


if year_range is not None:

    filtered = filtered[
        filtered["release_year"].between(
            year_range[0],
            year_range[1]
        )
    ]


if selected_languages:

    filtered = filtered[
        filtered["original_language"].isin(
            selected_languages
        )
    ]


if selected_status:

    filtered = filtered[
        filtered["status"].isin(
            selected_status
        )
    ]


filtered = filtered[
    filtered["vote_average"].between(
        rating_range[0],
        rating_range[1]
    )
]


# =========================================================
# KPI ANALYSIS
# =========================================================

st.header("📊 Dataset Overview")

c1, c2, c3, c4, c5 = st.columns(5)


# Total movies

c1.metric(
    "🎬 Movies",
    f"{len(filtered):,}"
)


# Average rating

avg_rating = filtered[
    "vote_average"
].mean()

c2.metric(
    "⭐ Average Rating",
    f"{avg_rating:.2f}"
)


# Average popularity

avg_popularity = filtered[
    "popularity"
].mean()

c3.metric(
    "🔥 Avg Popularity",
    f"{avg_popularity:.2f}"
)


# Total revenue

total_revenue = filtered[
    "revenue"
].sum()

c4.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.0f}"
)


# Average runtime

avg_runtime = filtered[
    "runtime"
].mean()

c5.metric(
    "⏱️ Avg Runtime",
    f"{avg_runtime:.0f} min"
)


# =========================================================
# DATASET INFORMATION
# =========================================================

st.divider()

st.header("🔍 Dataset Analysis")

a1, a2, a3 = st.columns(3)

with a1:

    st.metric(
        "Rows",
        f"{len(df):,}"
    )

with a2:

    st.metric(
        "Columns",
        len(df.columns)
    )

with a3:

    missing_values = int(
        df.isna().sum().sum()
    )

    st.metric(
        "Missing Values",
        f"{missing_values:,}"
    )


# =========================================================
# TAB STRUCTURE
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Trends",
    "⭐ Ratings",
    "🎭 Genres",
    "💰 Finance",
    "🌍 Languages",
    "📋 Data"
])


# =========================================================
# TAB 1 - TRENDS
# =========================================================

with tab1:

    st.subheader("📈 Movie Release Trends")

    yearly = (
        filtered
        .dropna(subset=["release_year"])
        .groupby("release_year")
        .size()
        .reset_index(
            name="movie_count"
        )
    )

    fig = px.line(
        yearly,
        x="release_year",
        y="movie_count",
        markers=True,
        title="Movies Released by Year"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Movies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Average rating over time

    st.subheader(
        "⭐ Average Rating Over Time"
    )

    rating_year = (
        filtered
        .dropna(subset=["release_year"])
        .groupby("release_year")[
            "vote_average"
        ]
        .mean()
        .reset_index()
    )

    fig2 = px.line(
        rating_year,
        x="release_year",
        y="vote_average",
        markers=True,
        title="Average Movie Rating by Year"
    )

    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Rating"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# =========================================================
# TAB 2 - RATINGS
# =========================================================

with tab2:

    st.subheader("⭐ Rating Analysis")

    r1, r2 = st.columns(2)

    with r1:

        fig = px.histogram(
            filtered,
            x="vote_average",
            nbins=30,
            title="Rating Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with r2:

        sample = filtered.sample(
            min(5000, len(filtered)),
            random_state=42
        )

        fig = px.scatter(
            sample,
            x="vote_count",
            y="vote_average",
            size="popularity",
            hover_name="title",
            title="Vote Count vs Rating"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Top rated

    st.subheader("🏆 Top Rated Movies")

    top_rated = (
        filtered
        .sort_values(
            "vote_average",
            ascending=False
        )
        [["title", "vote_average", "vote_count"]]
        .head(20)
    )

    st.dataframe(
        top_rated,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 3 - GENRES
# =========================================================

with tab3:

    st.subheader("🎭 Genre Analysis")

    genre_data = (
        filtered["genres"]
        .dropna()
        .astype(str)
        .str.split("|")
        .explode()
        .str.strip()
    )

    genre_counts = (
        genre_data
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
            title="Most Common Genres"
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
            title="Top 10 Genre Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 4 - FINANCE
# =========================================================

with tab4:

    st.subheader("💰 Financial Analysis")

    financial = filtered[
        (filtered["budget"] > 0) &
        (filtered["revenue"] > 0)
    ].copy()


    f1, f2 = st.columns(2)

    with f1:

        st.metric(
            "Total Budget",
            f"${financial['budget'].sum():,.0f}"
        )


    with f2:

        st.metric(
            "Total Revenue",
            f"${financial['revenue'].sum():,.0f}"
        )


    if len(financial) > 0:

        sample = financial.sample(
            min(5000, len(financial)),
            random_state=42
        )

        fig = px.scatter(
            sample,
            x="budget",
            y="revenue",
            size="popularity",
            hover_name="title",
            log_x=True,
            log_y=True,
            title="Budget vs Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # Most profitable

        financial["profit"] = (
            financial["revenue"] -
            financial["budget"]
        )

        st.subheader(
            "💵 Highest Profit Movies"
        )

        profitable = (
            financial
            .sort_values(
                "profit",
                ascending=False
            )
            [["title", "budget", "revenue", "profit"]]
            .head(20)
        )

        st.dataframe(
            profitable,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# TAB 5 - LANGUAGES
# =========================================================

with tab5:

    st.subheader(
        "🌍 Original Language Analysis"
    )

    language_data = (
        filtered[
            "original_language"
        ]
        .value_counts()
        .head(20)
        .reset_index()
    )

    language_data.columns = [
        "Language",
        "Movies"
    ]

    fig = px.bar(
        language_data,
        x="Language",
        y="Movies",
        title="Movies by Original Language"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 6 - DATA
# =========================================================

with tab6:

    st.subheader(
        "📋 Movie Dataset"
    )


    # Search

    search = st.text_input(
        "🔎 Search movie title"
    )


    display_data = filtered.copy()


    if search:

        display_data = display_data[
            display_data["title"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    st.write(
        f"Showing {len(display_data):,} movies"
    )


    st.dataframe(
        display_data,
        use_container_width=True,
        height=550,
        hide_index=True
    )


    # Download

    csv = filtered.to_csv(
        index=False,
        sep=";"
    ).encode("utf-8")


    st.download_button(
        "📥 Download Analysis Dataset",
        csv,
        "filtered_movies.csv",
        "text/csv"
    )


# =========================================================
# CORRELATION ANALYSIS
# =========================================================

st.divider()

st.header("🔗 Numerical Correlation Analysis")

correlation_columns = [
    "budget",
    "revenue",
    "runtime",
    "popularity",
    "vote_average",
    "vote_count"
]

available_columns = [
    col for col in correlation_columns
    if col in filtered.columns
]

correlation = filtered[
    available_columns
].corr()


fig_corr = px.imshow(
    correlation,
    text_auto=True,
    aspect="auto",
    title="Correlation Matrix"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎬 Movie Data Analysis Dashboard | "
    "Python • Pandas • Streamlit • Plotly"
)
