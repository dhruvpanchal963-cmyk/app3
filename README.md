# 🎬 Movie Analytics Dashboard

A fully interactive **Movie Analytics Dashboard** built using **Streamlit, Pandas, and Plotly**.
The dashboard allows users to explore a large movie dataset through interactive filters, charts, KPIs, and detailed movie information.

---

## 📌 Project Overview

This project analyzes a movie dataset containing information about movies, including:

* Movie title
* Original title
* Release date
* Genres
* Original language
* Movie status
* Runtime
* Ratings
* Vote count
* Popularity
* Budget
* Revenue

The Streamlit dashboard converts this raw dataset into an interactive visual analytics application.

---

## 🚀 Features

### 📊 Dashboard KPIs

The dashboard displays:

* 🎬 Total number of movies
* ⭐ Average movie rating
* 🔥 Average popularity
* 💰 Total revenue
* ⏱️ Average runtime

### 🎛️ Interactive Filters

Users can filter the dataset by:

* Release year
* Genre
* Original language
* Movie status
* Rating range

All charts and tables update according to the selected filters.

### 🏆 Movie Rankings

The dashboard provides:

* Highest-rated movies
* Most popular movies

### 📅 Release Trend

An interactive line chart shows the number of movies released over different years.

### 🎭 Genre Analysis

The dashboard includes:

* Top movie genres
* Genre distribution
* Genre frequency analysis

### ⭐ Rating Analysis

Users can explore:

* Movie rating distribution
* Vote count vs. rating
* Popularity comparison

### 💰 Financial Analysis

The dashboard visualizes:

* Movie budget
* Movie revenue
* Budget vs. revenue relationship

### 🌍 Language Analysis

The dashboard displays the most common original movie languages.

### 🔎 Movie Search

Users can search for movies by title.

### 📋 Movie Details Table

A detailed interactive table displays:

* Movie ID
* Title
* Original language
* Release date
* Genres
* Runtime
* Rating
* Vote count
* Popularity
* Budget
* Revenue
* Status

### 📥 Download Data

Users can download the **filtered dataset as a CSV file** directly from the dashboard.

---

## 🛠️ Technologies Used

| Technology | Purpose                       |
| ---------- | ----------------------------- |
| Python     | Programming language          |
| Streamlit  | Dashboard and web application |
| Pandas     | Data processing and analysis  |
| Plotly     | Interactive visualizations    |

---

## 📂 Project Structure

```text
Movie-Dashboard/
│
├── app.py
├── AllMoviesDetailsCleaned.csv
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone or download the project

Download the project files to your computer.

### 2. Open the project directory

Open Command Prompt or Terminal inside the project folder.

### 3. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Dashboard

Run the following command:

```bash
streamlit run app.py
```

After running the command, Streamlit will provide a local URL such as:

```text
http://localhost:8501
```

Open this URL in your browser.

---

## 📄 Dataset

The dashboard uses:

```text
AllMoviesDetailsCleaned.csv
```

The CSV file is expected to use a **semicolon (`;`) delimiter**.

The application loads the dataset using:

```python
pd.read_csv(
    "AllMoviesDetailsCleaned.csv",
    sep=";"
)
```

---

## 📈 Dashboard Workflow

```text
Movie Dataset
      ↓
Load CSV using Pandas
      ↓
Data Cleaning
      ↓
Interactive Streamlit Filters
      ↓
Data Analysis
      ↓
Plotly Visualizations
      ↓
Movie Search & Details
      ↓
Filtered CSV Download
```

---

## 💡 Key Insights Available

The dashboard can help users understand:

* Which movies have the highest ratings
* Which movies are most popular
* How movie production changes over time
* Which genres are most common
* Which languages dominate the dataset
* How ratings are distributed
* Relationship between movie budgets and revenue
* How many movies exist for different release periods

---

## 📦 Requirements

The project requires:

```text
streamlit
pandas
plotly
```

These dependencies are also available in:

```text
requirements.txt
```

---

## 🔧 Troubleshooting

### CSV file not found

Make sure the CSV file is in the same directory as `app.py`:

```text
app.py
AllMoviesDetailsCleaned.csv
```

### Streamlit command not recognized

Try:

```bash
python -m streamlit run app.py
```

### Dashboard is slow

The dataset contains a large number of records. Large scatter plots are sampled to improve dashboard performance.

---

## 👨‍💻 Author

**Movie Analytics Dashboard**

Built using Python, Streamlit, Pandas, and Plotly.

---

## 📜 License

This project is intended for educational, analytical, and demonstration purposes.
