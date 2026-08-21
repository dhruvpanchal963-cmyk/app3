import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Movie Data Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1.5rem;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
}

.dashboard-subtitle {
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 25px;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD EXCEL DATA
# ============================================================

@st.cache_data
def load_data():

    file_name = "AllMoviesDetails_20MB.xlsx"

    df = pd.read_excel(
        file_name,
        engine="openpyxl"
    )

    # --------------------------------------------------------
    # Convert numerical columns
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Convert release date
    # --------------------------------------------------------

    if "release_date" in df.columns:

        df["release_date"] = pd.to_datetime(
            df["release_date"],
            errors="coerce"
        )

        df["release_year"] = (
            df["release_date"].dt.year
        )


    # --------------------------------------------------------
    # Handle missing text
    # --------------------------------------------------------

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


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "❌ AllMoviesDetails_20MB.xlsx was not found."
    )

    st.info("""
    Make sure your GitHub repository contains:

    app3.py
    AllMoviesDetails_20MB.xlsx
    requirements.txt
    README.md
    """)

    st.stop()


except Exception as error:

    st.error(
        f"❌ Error loading Excel file: {error}"
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    '🎬 Movie Data Analysis Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive Exploratory Data Analysis of the Movie Dataset'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Dataset: {len(df):,} movies • "
    f"{len(df.columns)} variables"
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Analysis Filters")

st.sidebar.markdown("### Release Year")


# ------------------------------------------------------------
# YEAR FILTER
# ------------------------------------------------------------

if "release_year" in df.columns:

    valid_years = (
        df["release_year"]
        .dropna()
    )

    if len(valid_years) > 0:

        min_year = int(valid_years.min())
        max_year = int(valid_years.max())

        year_range = st.sidebar.slider(
            "Select Year",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )

    else:

        year_range = None

else:

    year_range = None


# ------------------------------------------------------------
# LANGUAGE FILTER
# ------------------------------------------------------------

st.sidebar.markdown("### Language")

languages = sorted(
    df["original_language"]
    .dropna()
    .unique()
)

selected_languages = st.sidebar.multiselect(
    "Original Language",
    languages
)


# ------------------------------------------------------------
# STATUS FILTER
# ------------------------------------------------------------

st.sidebar.markdown("### Movie Status")

statuses = sorted(
    df["status"]
    .dropna()
    .unique()
)

selected_status = st.sidebar.multiselect(
    "Status",
    statuses
)


# ------------------------------------------------------------
# RATING FILTER
# ------------------------------------------------------------

st.sidebar.markdown("### Rating")

rating_range = st.sidebar.slider(
    "Vote Average",
    min_value=0.0,
    max_value=10.0,
    value=(0.0, 10.0),
    step=0.1
)


# ============================================================
# APPLY FILTERS
# ============================================================

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
        filtered_df[
            "original_language"
        ].isin(selected_languages)
    ]


if selected_status:

    filtered_df = filtered_df[
        filtered_df[
            "status"
        ].isin(selected_status)
    ]


filtered_df = filtered_df[
    filtered_df["vote_average"].between(
        rating_range[0],
        rating_range[1]
    )
]


# ============================================================
# KPI SECTION
# ============================================================

st.header("📊 Dataset Overview")

k1, k2, k3, k4, k5 = st.columns(5)


# Total movies

k1.metric(
    "🎬 Total Movies",
    f"{len(filtered_df):,}"
)


# Average rating

average_rating = filtered_df[
    "vote_average"
].mean()

k2.metric(
    "⭐ Average Rating",
    f"{average_rating:.2f}"
)


# Average popularity

average_popularity = filtered_df[
    "popularity"
].mean()

k3.metric(
    "🔥 Avg Popularity",
    f"{average_popularity:.2f}"
)


# Revenue

total_revenue = filtered_df[
    "revenue"
].sum()

k4.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.0f}"
)


# Runtime

average_runtime = filtered_df[
    "runtime"
].mean()

k5.metric(
    "⏱️ Avg Runtime",
    f"{average_runtime:.0f} min"
)


# ============================================================
# SECOND KPI ROW
# ============================================================

st.markdown("### 📌 Additional Statistics")

s1, s2, s3, s4 = st.columns(4)


# Highest rated

highest_rating = filtered_df[
    "vote_average"
].max()

s1.metric(
    "Highest Rating",
    f"{highest_rating:.2f}"
)


# Highest popularity

highest_popularity = filtered_df[
    "popularity"
].max()

s2.metric(
    "Highest Popularity",
    f"{highest_popularity:,.2f}"
)


# Average votes

average_votes = filtered_df[
    "vote_count"
].mean()

s3.metric(
    "Average Votes",
    f"{average_votes:,.0f}"
)


# Missing values

missing_values = int(
    filtered_df.isna().sum().sum()
)

s4.metric(
    "Missing Values",
    f"{missing_values:,}"
)


st.divider()


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Trends",
    "⭐ Ratings",
    "🎭 Genres",
    "💰 Finance",
    "🌍 Languages",
    "📋 Dataset"
])


# ============================================================
# TAB 1 - TRENDS
# ============================================================

with tab1:

    st.header("📈 Movie Release Trends")


    # --------------------------------------------------------
    # Movies per year
    # --------------------------------------------------------

    yearly_movies = (
        filtered_df
        .dropna(
            subset=["release_year"]
        )
        .groupby("release_year")
        .size()
        .reset_index(
            name="movie_count"
        )
    )


    fig_year = px.line(
        yearly_movies,
        x="release_year",
        y="movie_count",
        markers=True,
        title="Number of Movies Released by Year"
    )

    fig_year.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Movies"
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )


    # --------------------------------------------------------
    # Average rating by year
    # --------------------------------------------------------

    st.subheader(
        "⭐ Average Rating by Year"
    )

    yearly_rating = (
        filtered_df
        .dropna(
            subset=["release_year"]
        )
        .groupby("release_year")[
            "vote_average"
        ]
        .mean()
        .reset_index()
    )


    fig_rating_year = px.line(
        yearly_rating,
        x="release_year",
        y="vote_average",
        markers=True,
        title="Average Movie Rating by Year"
    )

    fig_rating_year.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Average Rating"
    )

    st.plotly_chart(
        fig_rating_year,
        use_container_width=True
    )


# ============================================================
# TAB 2 - RATINGS
# ============================================================

with tab2:

    st.header("⭐ Movie Rating Analysis")


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # Rating distribution
    # --------------------------------------------------------

    with col1:

        fig = px.histogram(
            filtered_df,
            x="vote_average",
            nbins=30,
            title="Movie Rating Distribution"
        )

        fig.update_layout(
            xaxis_title="Rating",
            yaxis_title="Number of Movies"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # Vote count vs rating
    # --------------------------------------------------------

    with col2:

        if len(filtered_df) > 0:

            sample_size = min(
                5000,
                len(filtered_df)
            )

            sample = filtered_df.sample(
                sample_size,
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


    # --------------------------------------------------------
    # Top rated movies
    # --------------------------------------------------------

    st.subheader(
        "🏆 Top Rated Movies"
    )

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
                "vote_count",
                "popularity"
            ]
        ]
        .head(20)
    )

    st.dataframe(
        top_movies,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 3 - GENRES
# ============================================================

with tab3:

    st.header("🎭 Genre Analysis")


    genre_series = (
        filtered_df["genres"]
        .dropna()
        .astype(str)
        .str.split("|")
        .explode()
        .str.strip()
    )


    genre_counts = (
        genre_series
        .value_counts()
        .head(20)
        .reset_index()
    )


    genre_counts.columns = [
        "Genre",
        "Movies"
    ]


    g1, g2 = st.columns(2)


    # --------------------------------------------------------
    # Bar chart
    # --------------------------------------------------------

    with g1:

        fig = px.bar(
            genre_counts.sort_values(
                "Movies"
            ),
            x="Movies",
            y="Genre",
            orientation="h",
            title="Most Common Movie Genres"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # Pie chart
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Genre table
    # --------------------------------------------------------

    st.subheader(
        "📋 Genre Statistics"
    )

    st.dataframe(
        genre_counts,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 4 - FINANCE
# ============================================================

with tab4:

    st.header("💰 Financial Analysis")


    financial_df = filtered_df[
        (filtered_df["budget"] > 0) &
        (filtered_df["revenue"] > 0)
    ].copy()


    f1, f2, f3 = st.columns(3)


    total_budget = financial_df[
        "budget"
    ].sum()

    total_revenue_finance = financial_df[
        "revenue"
    ].sum()

    total_profit = (
        total_revenue_finance -
        total_budget
    )


    f1.metric(
        "💵 Total Budget",
        f"${total_budget:,.0f}"
    )

    f2.metric(
        "💰 Total Revenue",
        f"${total_revenue_finance:,.0f}"
    )

    f3.metric(
        "📈 Total Profit",
        f"${total_profit:,.0f}"
    )


    st.divider()


    # --------------------------------------------------------
    # Budget vs Revenue
    # --------------------------------------------------------

    if len(financial_df) > 0:

        sample_size = min(
            5000,
            len(financial_df)
        )

        financial_sample = (
            financial_df
            .sample(
                sample_size,
                random_state=42
            )
        )


        fig = px.scatter(
            financial_sample,
            x="budget",
            y="revenue",
            size="popularity",
            hover_name="title",
            log_x=True,
            log_y=True,
            title="Budget vs Revenue"
        )

        fig.update_layout(
            xaxis_title="Budget ($)",
            yaxis_title="Revenue ($)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ----------------------------------------------------
        # Profit calculation
        # ----------------------------------------------------

        financial_df["profit"] = (
            financial_df["revenue"] -
            financial_df["budget"]
        )


        st.subheader(
            "🏆 Most Profitable Movies"
        )


        profitable_movies = (
            financial_df
            .sort_values(
                "profit",
                ascending=False
            )
            [
                [
                    "title",
                    "budget",
                    "revenue",
                    "profit"
                ]
            ]
            .head(20)
        )


        st.dataframe(
            profitable_movies,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TAB 5 - LANGUAGES
# ============================================================

with tab5:

    st.header(
        "🌍 Original Language Analysis"
    )


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
        title="Movies by Original Language"
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


# ============================================================
# TAB 6 - DATASET
# ============================================================

with tab6:

    st.header(
        "📋 Movie Dataset Explorer"
    )


    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    search = st.text_input(
        "🔎 Search movie by title"
    )


    display_df = filtered_df.copy()


    if search:

        display_df = display_df[
            display_df[
                "title"
            ]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    st.write(
        f"Showing {len(display_df):,} movies"
    )


    # --------------------------------------------------------
    # Columns to display
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="📥 Download Filtered Data",
        data=csv_data,
        file_name="movie_analysis_filtered.csv",
        mime="text/csv"
    )


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

st.divider()

st.header(
    "🔗 Correlation Analysis"
)


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

    correlation_matrix = (
        filtered_df[
            available_correlation
        ]
        .corr()
    )


    fig_corr = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Movie Dataset Correlation Matrix"
    )


    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )


# ============================================================
# DATA QUALITY ANALYSIS
# ============================================================

st.divider()

st.header(
    "🧹 Data Quality Analysis"
)


missing_data = (
    df.isna()
    .sum()
    .sort_values(
        ascending=False
    )
    .reset_index()
)


missing_data.columns = [
    "Column",
    "Missing Values"
]


missing_data["Missing %"] = (
    missing_data["Missing Values"] /
    len(df) *
    100
).round(2)


st.dataframe(
    missing_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎬 Movie Data Analysis Dashboard | "
    "Built with Python • Pandas • Streamlit • Plotly"
)
