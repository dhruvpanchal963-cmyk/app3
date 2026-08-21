# 🎬 Movie Data Analysis Dashboard

An interactive **Movie Data Analysis Dashboard** built with **Python, Streamlit, Pandas, Plotly, and OpenPyXL**.

The dashboard performs exploratory data analysis (EDA) on a large movie dataset and provides interactive visualizations, filters, statistics, financial analysis, rating analysis, genre analysis, language analysis, and data exploration.

---

## 📊 Project Overview

This project analyzes movie data and converts it into an interactive web-based dashboard.

The dashboard helps users understand:

* Movie release trends
* Movie ratings
* Movie popularity
* Movie genres
* Movie languages
* Movie budgets
* Movie revenue
* Movie profitability
* Vote counts
* Runtime
* Relationships between numerical variables
* Missing data and data quality

---

## ✨ Main Features

### 📌 Dataset Overview

The dashboard displays important KPIs such as:

* 🎬 Total Movies
* ⭐ Average Rating
* 🔥 Average Popularity
* 💰 Total Revenue
* ⏱️ Average Runtime
* Highest Rating
* Highest Popularity
* Average Vote Count
* Missing Values

---

### 🎛️ Interactive Filters

Users can filter the movie dataset using:

* Release year
* Original language
* Movie status
* Rating range

All analysis and visualizations update automatically according to the selected filters.

---

## 📈 Movie Trend Analysis

The dashboard provides interactive charts showing:

* Number of movies released by year
* Average movie rating by year

These visualizations help identify changes and trends in movie production and ratings over time.

---

## ⭐ Rating Analysis

The rating section includes:

* Movie rating distribution
* Vote count vs rating
* Popularity vs rating
* Top-rated movies

Users can explore how ratings and audience votes are distributed across the dataset.

---

## 🎭 Genre Analysis

The genre section analyzes movie categories.

It includes:

* Most common movie genres
* Genre distribution
* Top 10 genres
* Genre statistics

The dashboard handles movies containing multiple genres.

---

## 💰 Financial Analysis

The financial section analyzes movie economics.

It includes:

* Total production budget
* Total revenue
* Total profit
* Budget vs revenue visualization
* Most profitable movies

Profit is calculated as:

```text
Profit = Revenue - Budget
```

---

## 🌍 Language Analysis

The language section analyzes the original languages of movies.

It provides:

* Movies by original language
* Top movie languages
* Language statistics

---

## 📋 Dataset Explorer

Users can explore the filtered dataset directly inside the dashboard.

Features include:

* Movie title search
* Interactive data table
* Movie details
* Filtered results
* CSV download

Users can download the currently filtered dataset using the **Download Filtered Data** button.

---

## 🔗 Correlation Analysis

The dashboard includes a correlation matrix for numerical variables such as:

* Budget
* Revenue
* Runtime
* Popularity
* Vote Average
* Vote Count

This helps identify relationships between different movie attributes.

---

## 🧹 Data Quality Analysis

The dashboard also provides a data-quality section showing:

* Column names
* Missing values
* Missing-value percentage

This helps identify incomplete fields in the dataset.

---

# 🛠️ Technologies Used

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Application development      |
| Streamlit  | Interactive dashboard        |
| Pandas     | Data processing and analysis |
| Plotly     | Interactive charts           |
| OpenPyXL   | Reading Excel dataset        |

---

# 📂 Project Structure

```text
app3/
│
├── app3.py
├── AllMoviesDetails_20MB.xlsx
├── requirements.txt
└── README.md
```

---

# 📄 Dataset

The dashboard uses:

```text
AllMoviesDetails_20MB.xlsx
```

The Excel file contains a subset of the original movie dataset prepared for dashboard deployment.

The application reads the Excel file using:

```python
pd.read_excel(
    "AllMoviesDetails_20MB.xlsx",
    engine="openpyxl"
)
```

---

# ⚙️ Installation

## 1. Download or clone the repository

Download the project from GitHub.

---

## 2. Open the project folder

Open Command Prompt or Terminal inside the project directory.

---

## 3. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Dashboard

Start the Streamlit application using:

```bash
streamlit run app3.py
```

The application will open in your browser.

Usually the local address is:

```text
http://localhost:8501
```

---

# ☁️ Deploy on Streamlit Cloud

The repository should contain all required files:

```text
app3.py
AllMoviesDetails_20MB.xlsx
requirements.txt
README.md
```

When deploying:

1. Connect the GitHub repository to Streamlit Cloud.
2. Select `app3.py` as the main application file.
3. Deploy the application.
4. Streamlit will install the packages listed in `requirements.txt`.
5. The application will load `AllMoviesDetails_20MB.xlsx`.

---

# ⚠️ Important File Requirement

The Excel filename must remain exactly:

```text
AllMoviesDetails_20MB.xlsx
```

The file must be in the **same directory as `app3.py`**.

Correct:

```text
app3/
├── app3.py
└── AllMoviesDetails_20MB.xlsx
```

Incorrect:

```text
app3/
├── app3.py
└── data/
    └── AllMoviesDetails_20MB.xlsx
```

unless the Python file is changed to use the `data/` path.

---

# 📦 Requirements

The project requires:

```text
streamlit
pandas
plotly
openpyxl
```

These packages are listed in:

```text
requirements.txt
```

---

# 🔄 Dashboard Workflow

```text
Excel Dataset
      ↓
Pandas Data Loading
      ↓
Data Cleaning
      ↓
Interactive Filters
      ↓
Exploratory Data Analysis
      ↓
Charts & KPIs
      ↓
Financial Analysis
      ↓
Correlation Analysis
      ↓
Data Quality Analysis
      ↓
Filtered Dataset Download
```

---

# 🎯 Project Objective

The main objective of this project is to transform raw movie data into an interactive analytical dashboard.

The dashboard can be used to identify patterns, trends, relationships, and insights within the movie dataset without requiring users to manually analyze the Excel file.

---

# 👨‍💻 Project

**Movie Data Analysis Dashboard**

Built using:

**Python + Streamlit + Pandas + Plotly + OpenPyXL**

---

## 📜 License

This project is intended for educational, analytical, and demonstration purposes.
