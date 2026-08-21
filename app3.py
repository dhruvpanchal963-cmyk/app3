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

/* =====================================================
   KEEP ORIGINAL DARK DASHBOARD
===================================================== */

.stApp {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =====================================================
   HEADINGS
===================================================== */

h1, h2, h3 {
    color: #ffffff !important;
}


/* =====================================================
   KPI CARDS
   ONLY THESE CARDS ARE WHITE
===================================================== */

[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 15px !important;
    padding: 20px !important;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.20);
}


/* =====================================================
   KPI LABEL = BLACK
===================================================== */

[data-testid="stMetricLabel"] {
    color: #000000 !important;
}


/* =====================================================
   KPI VALUE = BLACK
===================================================== */

[data-testid="stMetricValue"] {
    color: #000000 !important;
}


/* =====================================================
   KPI DELTA = BLACK
===================================================== */

[data-testid="stMetricDelta"] {
    color: #000000 !important;
}


/* =====================================================
   SIDEBAR
===================================================== */

[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] p {
    color: #ffffff !important;
}

[data-testid="stSidebar"] label {
    color: #ffffff !important;
}


/* =====================================================
   SIDEBAR INPUT LABELS
===================================================== */

.stSlider label,
.stMultiSelect label,
.stSelectbox label,
.stTextInput label {
    color: #ffffff !important;
}


/* =====================================================
   TABS
===================================================== */

button[data-baseweb="tab"] {
    color: #d1d5db !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
}


/* =====================================================
   DOWNLOAD BUTTON
===================================================== */

.stDownloadButton button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
}

.stDownloadButton button:hover {
    background-color: #1d4ed8 !important;
}


/* =====================================================
   DIVIDER
===================================================== */

hr {
    border-color: #374151 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_name = "AllMoviesDetails_20MB.xlsx"

    df = pd.read_excel(
        file_name,
        engine="openpyxl"
    )

    # -----------------------------------------------------
    # Convert numeric columns
    # -----------------------------------------------------

    numeric_columns = [
        "budget",
        "revenue",
        "runtime",
        "popularity",
        "vote_average",
        "vote_count"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # -----------------------------------------------------
    # Release date
    # -----------------------------------------------------

    if "release_date" in df.columns:

        df["release_date"] = pd.to_datetime(
            df["release_date"],
            errors="coerce"
        )

        df["release_year"] = (
            df["release_date"].dt.year
        )

    # -----------------------------------------------------
    # Text columns
    # -----------------------------------------------------

    text_columns = [
        "title",
        "original_title",
        "genres",
        "status",
        "original_language"
    ]

    for column in text_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .fillna("Unknown")
                .astype(str)
            )

    return df


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
        f"❌ Error loading dataset: {e}"
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


# =========================================================
# YEAR FILTER
# =========================================================

st.sidebar.markdown("### 📅 Release Year")

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
# LANGUAGE FILTER
# =========================================================

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


# =========================================================
# STATUS FILTER
# =========================================================

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


# =========================================================
# RATING FILTER
# =========================================================

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


# Total Movies

total_movies = len(filtered_df)

col1.metric(
    "🎬 Total Movies",
    f"{total_movies:,}"
)


# Average Rating

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


# Average Popularity

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


# Total Revenue

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


# Average Runtime

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


# Highest Rating

if "vote_average" in filtered_df.columns:

    highest_rating = filtered_df[
        "vote_average"
    ].max()

else:

    highest_rating = 0


a1.metric(
    "🏆 Highest Rating",
    f"{highest_rating:.2f}"
)


# Highest Popularity

if "popularity" in filtered_df.columns:

    highest_popularity = filtered_df[
        "popularity"
    ].max()

else:

    highest_popularity = 0


a2.metric(
    "🔥 Highest Popularity",
    f"{highest_popularity:.2f}"
)


# Average Votes

if "vote_count" in filtered_df.columns:

    average_votes = filtered_df[
        "vote_count"
    ].mean()

else:

    average_votes = 0


a3.metric(
    "👥 Average Votes",
    f"{average_votes:,.0f}"
)


# Missing Values

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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📈 Trends",
        "⭐ Ratings",
        "🎭 Genres",
        "💰 Finance",
        "🌍 Languages",
        "📋 Dataset"
    ]
)


# =========================================================
# TAB 1 - TRENDS
# =========================================================

with tab1:

    st.header("📈 Movie Release Trends")


    # Movies per year

    if "release_year" in filtered_df.columns:

        yearly_movies = (
            filtered_df
            .dropna(
                subset=["release_year"]
            )
            .groupby("release_year")
            .size()
            .reset_index(
                name="Movies"
            )
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


    rating_col1, rating_col2 = st.columns(2)


    # Rating Distribution

    with rating_col1:

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
                yaxis_title="Number of Movies"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Votes vs Rating

    with rating_col2:

        required = {
            "vote_count",
            "vote_average",
            "popularity"
        }

        if required.issubset(
            filtered_df.columns
        ):

            if len(filtered_df) > 0:

                sample = filtered_df.sample(
                    min(
                        5000,
                        len(filtered_df)
                    ),
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


    # Top Rated Movies

    st.subheader(
        "🏆 Top Rated Movies"
    )


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
            .str.replace(
                ",",
                "|",
                regex=False
            )
        )

        genre_series = (
            genre_data
            .str.split("|")
            .explode()
            .str.strip()
        )

        genre_counts = (
            genre_series
            .replace(
                "",
                "Unknown"
            )
            .value_counts()
            .head(20)
            .reset_index()
        )

        genre_counts.columns = [
            "Genre",
            "Movies"
        ]


        genre_col1, genre_col2 = st.columns(2)


        # Bar chart

        with genre_col1:

            fig = px.bar(
                genre_counts.sort_values(
                    "Movies"
                ),
                x="Movies",
                y="Genre",
                orientation="h",
                title="🎭 Most Common Genres"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # Pie chart

        with genre_col2:

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


        st.subheader(
            "📋 Genre Statistics"
        )

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


        finance1, finance2, finance3 = st.columns(3)


        finance1.metric(
            "💵 Total Budget",
            f"${finance['budget'].sum():,.0f}"
        )


        finance2.metric(
            "💰 Total Revenue",
            f"${finance['revenue'].sum():,.0f}"
        )


        finance3.metric(
            "📈 Total Profit",
            f"${finance['profit'].sum():,.0f}"
        )


        st.divider()


        if len(finance) > 0:

            sample = finance.sample(
                min(
                    5000,
                    len(finance)
                ),
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
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.subheader(
                "🏆 Most Profitable Movies"
            )


            profit_columns = [
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
                [profit_columns]
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

    st.header(
        "🌍 Original Language Analysis"
    )


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
# TAB 6 - DATASET EXPLORER
# =========================================================

with tab6:

    st.header(
        "📋 Movie Dataset Explorer"
    )


    search = st.text_input(
        "🔎 Search Movie by Title"
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
        display_df[
            available_columns
        ],
        use_container_width=True,
        height=550,
        hide_index=True
    )


    # Download CSV

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv_data,
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


available_correlation = [
    column
    for column in correlation_columns
    if column in filtered_df.columns
]


if len(available_correlation) >= 2:

    correlation = (
        filtered_df[
            available_correlation
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
    "🎬 Movie Analytics Dashboard | "
    "Python • Streamlit • Pandas • Plotly"
)
