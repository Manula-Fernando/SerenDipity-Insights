# SerenDipity InsiGhts: Sri Lanka Tourism Dashboard 🌴

![Sri Lanka Tourism Banner](https://vignette.wikia.nocookie.net/logopedia/images/8/83/Srilanka_logo.png/revision/latest/scale-to-width-down/2000?cb=20150502050036)

## 🏖️ Overview

**SerenDipity InsiGhts** is an interactive data visualization platform built with Dash and Plotly that provides comprehensive analytics on tourist arrivals to Sri Lanka. This dashboard enables tourism stakeholders, policymakers, data analysts, and researchers to gain valuable insights into visitor patterns, key source markets, arrival dynamics, and the geographic distribution of tourists from 2019 to the present day.

### Built By
- **Dinil Bandara** - [LinkedIn](https://www.linkedin.com/in/dinil-bandara-533777283/)
- **Manula Fernando** - [LinkedIn](https://www.linkedin.com/in/manula-fernando-483875283/)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Dash](https://img.shields.io/badge/Dash-2.16-orange.svg)](https://dash.plotly.com/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18-green.svg)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.1-yellow.svg)](https://pandas.pydata.org/)

---

## ✨ Features

The dashboard is organized into five distinct, feature-rich tabs:

### 1. Overview 🏠
- **At-a-Glance KPIs:** High-level summary cards showing total current-year arrivals, latest monthly figures, and the top source market.
- **Live Economic Indicator:** Real-time LKR to USD exchange rate, updated daily via an API.
- **Trend Visualization:** A dynamic line and bar chart displaying the monthly arrivals trend for the current year.

### 2. Inbound Visitors 📊
- **Historical Analysis:** An interactive line chart for detailed time-series analysis of tourist arrivals.
- **Dual Metrics:** Toggle between viewing **Total Arrivals** and month-over-month **Percentage Change** to understand both volume and velocity.
- **Year-over-Year Comparison:** Easily switch between years (2019-2024) to compare tourism performance and identify long-term trends or anomalies.

### 3. Arrival Dynamics 💰
- **Correlation Analysis:** An interactive scatter plot to explore the relationship between total arrivals and arrivals for a specific purpose (Business, Pleasure/Vacation, or Health).
- **Statistical Insights:** A dynamically generated correlation coefficient provides a clear, quantitative measure of the relationship between travel types.
- **Outlier Robustness:** The plot automatically filters outliers to provide a cleaner and more accurate visualization of the core trend.

### 4. Top Markets 🌏
- **Holistic Market View:** An interactive treemap that visualizes the contribution of every source country to Sri Lanka's tourism.
- **Performance Ranking:** A clean, horizontal bar chart highlighting the **Top 10 Source Markets** for any selected year.
- **Dynamic Filtering:** All charts update instantly based on the selected year, allowing for quick identification of emerging or declining markets.

### 5. Geographic Analysis 🗺️
- **Global Arrivals Map:** An interactive choropleth world map where color intensity represents the volume of tourist arrivals from each country.
- **Drill-Down Capability:** Click on any country on the map to instantly generate a pie chart showing its specific monthly arrival distribution for the selected year.
- **Regional Insight:** Quickly identify key tourism-generating regions and countries across the globe.

---

## 🚀 Installation and Setup

### Prerequisites
- Python 3.9 or newer
- `pip` (Python package installer)

### Setup Instructions

#### Method 1: Automatic Setup (Windows Only)

For a quick and easy setup on Windows, simply double-click the `setup.bat` file located in the project's root directory. This script will:
1.  Create a Python virtual environment in a folder named `venv`.
2.  Activate the virtual environment.
3.  Install all required packages from `requirements.txt`.

#### Method 2: Manual Setup (All Operating Systems)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/SerenDipity-Insights.git
    cd SerenDipity-Insights
    ```
    *(Replace `your-username` with your actual GitHub username)*

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **On Windows (Command Prompt):**
        ```cmd
        .\venv\Scripts\activate
        ```
    -   **On macOS/Linux (Bash/Zsh):**
        ```sh
        source venv/bin/activate
        ```

4.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

---

### 🏃 Running the Application

-   **Windows:** Double-click the `run.bat` file.
-   **macOS/Linux:** Make sure your virtual environment is activated and run:
    ```bash
    python app.py
    ```

After running the command, open your web browser and navigate to the following URL:
**http://127.0.0.1:8050/**

---

## 🔧 Project Structure

The project is built with a modular and scalable architecture:

SerenDipity-Insights/
├── assets/ # CSS stylesheets and other static assets
├── data/ # All raw .csv data files
├── modules/ # Core application logic and layouts
│ ├── data_loader.py # Handles all data loading and cleaning
│ ├── layout_overview.py # Layout and callbacks for the Overview tab
│ ├── layout_arrivals.py # Layout and callbacks for Inbound Visitors
│ ├── layout_dynamics.py # Layout and callbacks for Arrival Dynamics
│ ├── layout_countries.py # Layout and callbacks for Top Markets
│ └── layout_geo.py # Layout and callbacks for Geographic Analysis
├── app.py # Main application entry point and server setup
├── requirements.txt # List of project dependencies
├── setup.bat # Windows script for automatic setup
├── run.bat # Windows script to run the application
└── README.md # You are here!


---

## 💡 Technical Implementation

-   **Backend & Visualization:** Python, Dash, Plotly, Pandas
-   **Frontend:** HTML, Tailwind CSS (for modern styling)
-   **Data Fetching:** The `requests` library is used to fetch live exchange rate data from an external API.
-   **Code Architecture:** The application is broken down into modules by feature (tabs), making the code clean, reusable, and easy to maintain or expand.

---

## 📝 Future Improvements

-   [ ] **Real-time Data Integration:** Connect to a live tourism database or API for up-to-the-minute analytics.
-   [ ] **Predictive Forecasting:** Implement time-series models (like ARIMA or Prophet) to forecast future tourist arrivals.
-   [ ] **Report Generation:** Add a feature to download visualizations or summary data as a PDF or CSV file.
-   [ ] **Performance Optimization:** For larger datasets, implement server-side caching or use more efficient data formats like Parquet.

---

*Experience the Wonder of Asia with Data-Driven Insights! 🇱🇰*
