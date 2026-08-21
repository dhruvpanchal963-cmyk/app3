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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ================================
   MAIN APPLICATION
================================ */

.stApp {
    background-color: #0e1117;
    color: #ffffff;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ================================
   HEADINGS
================================ */

h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

h2 {
    color: #ffffff !important;
    font-weight: 750 !important;
}

h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
}


/* ================================
   NORMAL TEXT
================================ */

p {
    color: #d1d5db !important;
}


/* ================================
   KPI CARDS
================================ */

[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 15px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.20);
}


/* KPI LABEL */

[data-testid="stMetricLabel"] {
    color: #374151 !important;
    font-weight: 700 !important;
}


/* KPI VALUE */

[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 800 !important;
}


/* KPI DELTA */

[data-testid="stMetricDelta"] {
    color: #374151 !important;
}


/* ================================
   SIDEBAR
================================ */

[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #e5e7eb !important;
}


/* ================================
   INPUT BOXES
================================ */

.stSelectbox label,
.stMultiSelect label,
.stSlider label,
.stTextInput label {
    color: #ffffff !important;
    font-weight: 600 !important;
}


/* ================================
   TABS
================================ */

button[data-baseweb="tab"] {
    color: #d1d5db !important;
    font-weight: 600 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
}


/* ================================
   DATAFRAME
================================ */

[data-testid="stDataFrame"] {
    border-radius: 12px !important;
}


/* ================================
   DIVIDER
================================ */

hr {
    border-color: #374151 !important;
}


/* ================================
   DOWNLOAD BUTTON
================================ */

.stDownloadButton button {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 10px 18px !important;
}

.stDownloadButton button:hover {
    background-color: #1d4ed8 !important;
}


/* ================================
   INFO / ERROR
================================ */

[data-testid="stAlert"] {
    border-radius: 10px;
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

    # -----------------------------------------
    # Numeric columns
    # -----------------------------------------

    numeric_columns = [
        "budget",
        "revenue",
        "runtime",
        "popularity",
        "vote_average",
        "vote_count"
    ]

    for column in numeric_columns:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )


    # -----------------------------------------
    # Release date
    # -----------------------------------------

    if "release_date" in data.columns:

        data["release_date"] = pd.to_datetime(
            data["release_date"],
            errors="coerce"
        )

        data["release_year"] = (
            data["release_date"].dt.year
        )


    # -----------------------------------------
    # Text columns
    # -----------------------------------------

    text_columns = [
        "title",
        "original_title",
        "genres",
        "status",
        "original_language"
    ]

    for column in text_columns:

        if column in data.columns:

            data[column] = (
                data[column]
                .fillna("Unknown")
                .astype(str)
            )

    return data


# =========================================================
# LOAD DATA SAFELY
# =========================================================

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "❌ AllMoviesDetails_20MB.xlsx was not found."
    )

    st.info(
        "Make sure AllMoviesDetails_20MB.xlsx "
        "is in the same GitHub folder as app3.py."
    )

    st.stop()

except Exception as e:

    st.error(
        f"❌ Unable to load dataset: {e}"
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title("🎬 Movie Analytics Dashboard")

st.markdown(
    "### Interactive Movie Data Analysis & Exploration"
)

st.caption(
    f"📊 {len(df):,} movies • "
    f"{len(df.columns)} columns"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown(
    "### 📅 Release Year"
)


# ---------------------------------------------------------
# YEAR
# ---------------------------------------------------------

if "release_year" in df.columns:

    years = df["release_year"].dropna()

    if len(years) > 0:

        min_year = int(years.min())
        max_year = int(years.max())

        year_range = st.sidebar.slider(
            "Select Year Range",
            min_year,
            max_year,
            (min_year, max_year)
        )

    else:

        year_range = None

else:

    year_range = None


# ---------------------------------------------------------
# LANGUAGE
# ---------------------------------------------------------

st.sidebar.markdown("### 🌍 Language")

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


# ---------------------------------------------------------
# STATUS
# ---------------------------------------------------------

st.sidebar.markdown("### 🎥 Movie Status")

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


# ---------------------------------------------------------
# RATING
# ---------------------------------------------------------

st.sidebar.markdown("### ⭐ Rating")

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


col1, col2, col3, col4, col5 = st.columns(5)


# ---------------------------------------------------------
# TOTAL MOVIES
# ---------------------------------------------------------

col1.metric(
    "🎬 Total Movies",
    f"{len(filtered_df):,}"
)


# ---------------------------------------------------------
# AVERAGE RATING
# ---------------------------------------------------------

if "vote_average" in filtered_df.columns:

    avg_rating = filtered_df[
        "vote_average"
    ].mean()

else:

    avg_rating = 0


col2.metric(
    "⭐ Average Rating",
    f"{avg_rating:.2f}"
)


# ---------------------------------------------------------
# POPULARITY
# ---------------------------------------------------------

if "popularity" in filtered_df.columns:

    avg_popularity = filtered_df[
        "popularity"
    ].mean()

else:

    avg_popularity = 0


col3.metric(
    "🔥 Avg Popularity",
    f"{avg_popularity:.2f}"
)


# ---------------------------------------------------------
# REVENUE
# ---------------------------------------------------------

if "revenue" in filtered_df.columns:

    total_revenue = filtered_df[
        "revenue"
    ].sum()

else:

    total_revenue = 0


col4.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.0f}"
)


# ---------------------------------------------------------
# RUNTIME
# ---------------------------------------------------------

if "runtime" in filtered_df.columns:

    avg_runtime = filtered_df[
        "runtime"
    ].mean()

else:

    avg_runtime = 0


col5.metric(
    "⏱️ Avg Runtime",
    f"{avg_runtime:.0f} min"
)


# =========================================================
# ADDITIONAL STATISTICS
# =========================================================

st.subheader("📌 Additional Statistics")


a1, a2, a3, a4 = st.columns(4)


# Highest rating

highest_rating = (
    filtered_df["vote_average"].max()
    if "vote_average" in filtered_df.columns
    else 0
)

a1.metric(
    "🏆 Highest Rating",
    f"{highest_rating:.2f}"
)


# Highest popularity

highest_popularity = (
    filtered_df["popularity"].max()
    if "popularity" in filtered_df.columns
    else 0
)

a2.metric(
    "🔥 Highest Popularity",
    f"{highest_popularity:.2f}"
)


# Average votes

average_votes = (
    filtered_df["vote_count"].mean()
    if "vote_count" in filtered_df.columns
    else 0
)

a3.metric(
    "👥 Average Votes",
    f"{average_votes:,.0f}"
)


# Missing values

missing_values = int(
    filtered_df.isna().sum().sum()
)

a4.metric(
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
# TAB 1 - TRENDS
# =========================================================

with tab1:

    st.header("📈 Movie Release Trends")


    if "release_year" in filtered_df.columns:

        yearly_movies = (
            filtered_df
            .dropna(subset=["release_year"])
            .groupby("release_year")
            .size()
            .reset_index(name="Movies")
        )

        fig = px.line(
            yearly_movies,
            x="release_year",
            y="Movies",
            markers=True,
            title="🎬 Movies Released by Year"
        )

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Release Year",
            yaxis_title="Number of Movies"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Average rating by year

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

        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Release Year",
            yaxis_title="Average Rating"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 2 - RATINGS
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

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Rating",
                yaxis_title="Movies"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Vote count vs rating

    with r2:

        if {
            "vote_count",
            "vote_average",
            "popularity"
        }.issubset(filtered_df.columns):

            sample = filtered_df.sample(
                min(5000, len(filtered_df)),
                random_state=42
            )

            fig = px.scatter(
                sample,
                x="vote_count",
                y="vote_average",
                size="popularity",
                hover_name="title"
                if "title" in sample.columns
                else None,
                title="👥 Votes vs Rating"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Top rated

    st.subheader("🏆 Top Rated Movies")


    if {
        "title",
        "vote_average",
        "vote_count"
    }.issubset(filtered_df.columns):

        top_rated = (
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
            top_rated,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# TAB 3 - GENRES
# =========================================================

with tab3:

    st.header("🎭 Genre Analysis")


    if "genres" in filtered_df.columns:

        genre_data = (
            filtered_df["genres"]
            .fillna("Unknown")
            .astype(str)
        )

        # Handle different possible separators

        genre_data = genre_data.str.replace(
            ",",
            "|",
            regex=False
        )

        genre_series = (
            genre_data
            .str.split("|")
            .explode()
            .str.strip()
        )

        genre_counts = (
            genre_series
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
                title="🎭 Most Popular Genres"
            )

            fig.update_layout(
                template="plotly_dark"
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
                title="🎬 Top 10 Genre Distribution"
            )

            fig.update_layout(
                template="plotly_dark"
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
# TAB 4 - FINANCE
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
            finance["revenue"] -
            finance["budget"]
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


        st.divider()


        if len(finance) > 0:

            sample = finance.sample(
                min(5000, len(finance)),
                random_state=42
            )


            fig = px.scatter(
                sample,
                x="budget",
                y="revenue",
                size="popularity"
                if "popularity" in sample.columns
                else None,
                hover_name="title"
                if "title" in sample.columns
                else None,
                log_x=True,
                log_y=True,
                title="💰 Budget vs Revenue"
            )

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Budget",
                yaxis_title="Revenue"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.subheader(
                "🏆 Most Profitable Movies"
            )


            columns = [
                column
                for column in [
                    "title",
                    "budget",
                    "revenue",
                    "profit"
                ]
                if column in finance.columns
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
# TAB 5 - LANGUAGES
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

        fig.update_layout(
            template="plotly_dark"
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
# TAB 6 - DATASET
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
        column
        for column in preferred_columns
        if column in display_df.columns
    ]


    st.dataframe(
        display_df[available_columns],
        use_container_width=True,
        height=550,
        hide_index=True
    )


    csv_file = display_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        "📥 Download Filtered CSV",
        data=csv_file,
        file_name="movie_analysis_filtered.csv",
        mime="text/csv"
    )


# =========================================================
# CORRELATION ANALYSIS
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


available_columns = [
    column
    for column in correlation_columns
    if column in filtered_df.columns
]


if len(available_columns) >= 2:

    correlation = (
        filtered_df[
            available_columns
        ]
        .corr()
    )


    fig = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="🔗 Movie Variable Correlation"
    )

    fig.update_layout(
        template="plotly_dark"
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
    missing["Missing Values"] /
    len(df) *
    100
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
