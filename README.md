# HealthKart-Assignament

# 📊 Influencer Campaign Performance Dashboard

This project is a **Streamlit-based dashboard** for analyzing and monitoring influencer marketing campaigns using **MySQL** as the backend.

## ✅ Features

- **Real-time filters**:
  - Brand
  - Platform
  - Influencer Type
  - Date Range
- **Key Performance Indicators (KPIs)**:
  - Total Spend
  - Total Revenue
  - ROI (Return on Investment)
  - Incremental ROAS
  - Total Reach
- **Data Visualizations** (using Streamlit):
  - Top 5 Influencers by ROAS (bar chart)
  - Monthly Spend vs Revenue (line chart)
  - Revenue by Category (pie chart)
  - Platform Reach (area chart)
- **Detailed Table**: Complete performance metrics by influencer
- **Textual Insight**: Highlighting the top performer dynamically

## 🧩 Tech Stack

| Component     | Tech         |
|---------------|--------------|
| Dashboard     | Streamlit    |
| Language      | Python       |
| Data Querying | SQLAlchemy, MySQL |
| Data Handling | Pandas       |
| Visualization | Streamlit Charts |

## 📂 Folder Structure

```
.
├── app.py               # Main Streamlit app
├── queries.py           # All SQL queries and data functions
├── db_connection.py     # MySQL database connection setup
├── requirements.txt     # Project dependencies
└── README.md            # Documentation
```

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/influencer-dashboard.git
cd influencer-dashboard
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

If you haven't already, install:

```bash
pip install streamlit pymysql sqlalchemy pandas
```

### 3. Configure MySQL Connection

Edit `db_connection.py` with your credentials:

```python
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://username:password@localhost/db_name")
```

### 4. Run the App

```bash
streamlit run app.py
```

## 🧠 Assumptions

- The database contains these tables:
  - `tracking_data`
  - `posts`
  - `influencers`
  - `payouts`
- These tables should include appropriate columns like:
  - `revenue`, `reach`, `date`, `platform`, `product`, `total_payout`, etc.

## 📝 To Do

- Add export/download button
- Add user authentication (if needed)
- Enhance error handling and validations
