import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 1.5rem;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 17px;
    margin-bottom: 25px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    file_path = "AllMoviesDetailsCleaned.csv"

    df = pd.read_csv(
        file_path,
        sep=";",
        encoding="utf-8-sig",
        low_memory=False
    )

    # Convert date
    df["release_date"] = pd.to_datetime(
        df["release_date"],
        dayfirst=True,
        errors="coerce"
    )

    # Convert popularity to numeric
    df["popularity"] = pd.to_numeric(
        df["popularity"],
        errors="coerce"
    )

    # Release year
    df["release_year"] = df["release_date"].dt.year

    # Replace empty values
    df["genres"] = df["genres"].fillna("Unknown")
    df["original_language"] = df["original_language"].fillna("Unknown")
    df["status"] = df["status"].fillna("Unknown")
    df["title"] = df["title"].fillna(df["original_title"])

    return df


df = load_data()


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    '<div class="dashboard-title">🎬 Movie Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Explore movie ratings, popularity, revenue, genres and release trends.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("🎛️ Dashboard Filters")

# Year filter
valid_years = df["release_year"].dropna()

if len(valid_years) > 0:

    min_year = int(valid_years.min())
    max_year = int(valid_years.max())

    selected_years = st.sidebar.slider(
        "Release Year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

else:
    selected_years = None


# Genre filter

genre_series = (
    df["genres"]
    .dropna()
    .str.split("|")
    .explode()
    .str.strip()
)

genre_options = sorted(
    genre_series[
        genre_series != ""
    ].dropna().unique()
)

selected_genres = st.sidebar.multiselect(
    "Genre",
    genre_options
)


# Language filter

language_options = sorted(
    df["original_language"]
    .dropna()
    .unique()
)

selected_languages = st.sidebar.multiselect(
    "Original Language",
    language_options
)


# Status filter

status_options = sorted(
    df["status"]
    .dropna()
    .unique()
)

selected_status = st.sidebar.multiselect(
    "Movie Status",
    status_options
)


# Rating filter

rating_range = st.sidebar.slider(
    "Rating",
    min_value=0.0,
    max_value=10.0,
    value=(0.0, 10.0),
    step=0.1
)


# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

filtered_df = df.copy()

if selected_years:

    filtered_df = filtered_df[
        filtered_df["release_year"].between(
            selected_years[0],
            selected_years[1]
        )
    ]


if selected_genres:

    pattern = "|".join(selected_genres)

    filtered_df = filtered_df[
        filtered_df["genres"].str.contains(
            pattern,
            case=False,
            na=False
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


filtered_df = filtered_df[
    filtered_df["vote_average"].between(
        rating_range[0],
        rating_range[1]
    )
]


# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

total_movies = len(filtered_df)

avg_rating = (
    filtered_df["vote_average"].mean()
    if len(filtered_df) > 0
    else 0
)

avg_popularity = (
    filtered_df["popularity"].mean()
    if len(filtered_df) > 0
    else 0
)

total_revenue = filtered_df["revenue"].sum()

avg_runtime = (
    filtered_df["runtime"].mean()
    if len(filtered_df) > 0
    else 0
)


# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "🎬 Total Movies",
    f"{total_movies:,}"
)

col2.metric(
    "⭐ Average Rating",
    f"{avg_rating:.2f}"
)

col3.metric(
    "🔥 Avg Popularity",
    f"{avg_popularity:.2f}"
)

col4.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.0f}"
)

col5.metric(
    "⏱️ Avg Runtime",
    f"{avg_runtime:.0f} min"
)


st.divider()


# ---------------------------------------------------
# TOP MOVIES
# ---------------------------------------------------

st.subheader("🏆 Top Movies")

top_col1, top_col2 = st.columns(2)


with top_col1:

    st.markdown("### ⭐ Highest Rated Movies")

    top_rated = (
        filtered_df[
            filtered_df["vote_count"] >= 50
        ]
        .sort_values(
            "vote_average",
            ascending=False
        )
        .head(10)
        [["title", "vote_average", "vote_count"]]
    )

    st.dataframe(
        top_rated,
        use_container_width=True,
        hide_index=True
    )


with top_col2:

    st.markdown("### 🔥 Most Popular Movies")

    top_popular = (
        filtered_df
        .sort_values(
            "popularity",
            ascending=False
        )
        .head(10)
        [["title", "popularity", "vote_average"]]
    )

    st.dataframe(
        top_popular,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------
# RELEASE TREND
# ---------------------------------------------------

st.subheader("📅 Movies Released Over Time")

year_data = (
    filtered_df
    .dropna(subset=["release_year"])
    .groupby("release_year")
    .size()
    .reset_index(name="movie_count")
)

fig_year = px.line(
    year_data,
    x="release_year",
    y="movie_count",
    markers=True,
    title="Number of Movies Released Each Year"
)

fig_year.update_layout(
    xaxis_title="Release Year",
    yaxis_title="Number of Movies",
    hovermode="x unified"
)

st.plotly_chart(
    fig_year,
    use_container_width=True
)


# ---------------------------------------------------
# GENRE ANALYSIS
# ---------------------------------------------------

st.subheader("🎭 Genre Analysis")

genre_data = (
    filtered_df[
        ["genres"]
    ]
    .dropna()
)

genre_data = (
    genre_data["genres"]
    .str.split("|")
    .explode()
    .str.strip()
)

genre_counts = (
    genre_data
    .value_counts()
    .reset_index()
)

genre_counts.columns = [
    "genre",
    "movie_count"
]

genre_counts = genre_counts.head(15)


genre_col1, genre_col2 = st.columns(2)


with genre_col1:

    fig_genre = px.bar(
        genre_counts,
        x="movie_count",
        y="genre",
        orientation="h",
        title="Top Movie Genres"
    )

    fig_genre.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig_genre,
        use_container_width=True
    )


with genre_col2:

    fig_pie = px.pie(
        genre_counts.head(10),
        values="movie_count",
        names="genre",
        title="Genre Distribution"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


# ---------------------------------------------------
# RATING DISTRIBUTION
# ---------------------------------------------------

st.subheader("⭐ Rating Analysis")

rating_col1, rating_col2 = st.columns(2)


with rating_col1:

    fig_rating = px.histogram(
        filtered_df,
        x="vote_average",
        nbins=30,
        title="Movie Rating Distribution"
    )

    fig_rating.update_layout(
        xaxis_title="Rating",
        yaxis_title="Number of Movies"
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )


with rating_col2:

    fig_votes = px.scatter(
        filtered_df.sample(
            min(5000, len(filtered_df))
        ),
        x="vote_count",
        y="vote_average",
        size="popularity",
        hover_name="title",
        title="Votes vs Rating",
        opacity=0.6
    )

    st.plotly_chart(
        fig_votes,
        use_container_width=True
    )


# ---------------------------------------------------
# BUDGET VS REVENUE
# ---------------------------------------------------

st.subheader("💰 Budget vs Revenue")

financial_df = filtered_df[
    (filtered_df["budget"] > 0) &
    (filtered_df["revenue"] > 0)
].copy()

if len(financial_df) > 0:

    sample_size = min(
        5000,
        len(financial_df)
    )

    financial_sample = financial_df.sample(
        sample_size,
        random_state=42
    )

    fig_finance = px.scatter(
        financial_sample,
        x="budget",
        y="revenue",
        size="popularity",
        hover_name="title",
        title="Movie Budget vs Revenue",
        log_x=True,
        log_y=True
    )

    fig_finance.update_layout(
        xaxis_title="Budget ($)",
        yaxis_title="Revenue ($)"
    )

    st.plotly_chart(
        fig_finance,
        use_container_width=True
    )

else:

    st.info(
        "No movies with both budget and revenue data "
        "are available for the selected filters."
    )


# ---------------------------------------------------
# LANGUAGE ANALYSIS
# ---------------------------------------------------

st.subheader("🌍 Movie Languages")

language_data = (
    filtered_df[
        "original_language"
    ]
    .value_counts()
    .head(15)
    .reset_index()
)

language_data.columns = [
    "language",
    "movie_count"
]

fig_language = px.bar(
    language_data,
    x="language",
    y="movie_count",
    title="Top Original Languages"
)

st.plotly_chart(
    fig_language,
    use_container_width=True
)


# ---------------------------------------------------
# MOVIE SEARCH
# ---------------------------------------------------

st.subheader("🔎 Search Movies")

search_text = st.text_input(
    "Search by movie title"
)

if search_text:

    search_results = filtered_df[
        filtered_df["title"]
        .str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

else:

    search_results = filtered_df


# ---------------------------------------------------
# MOVIE TABLE
# ---------------------------------------------------

display_columns = [
    "id",
    "title",
    "original_language",
    "release_date",
    "genres",
    "runtime",
    "vote_average",
    "vote_count",
    "popularity",
    "budget",
    "revenue",
    "status"
]

display_columns = [
    c for c in display_columns
    if c in search_results.columns
]

st.subheader(
    f"🎞️ Movies ({len(search_results):,})"
)

st.dataframe(
    search_results[
        display_columns
    ].sort_values(
        "vote_average",
        ascending=False
    ),
    use_container_width=True,
    height=500,
    hide_index=True
)


# ---------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------

st.subheader("⬇️ Download Data")

csv_data = filtered_df.to_csv(
    index=False,
    sep=";"
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_movies.csv",
    mime="text/csv"
)


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "🎬 Movie Analytics Dashboard | Built with Streamlit, Pandas and Plotly"
)
