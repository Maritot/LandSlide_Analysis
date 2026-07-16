# LandSlide_Analysis# 🌍 Landslide Disaster Impact & Emergency Response Analytics

## 📖 Project Overview

This project focuses on analyzing **landslide disaster events** and **emergency response operations** using data analytics techniques. It integrates environmental, disaster impact, emergency response, and recovery datasets into a single analytical model to uncover actionable insights for disaster management agencies.

The project follows a complete Data Analytics workflow including **Data Cleaning, SQL Analysis, Exploratory Data Analysis (EDA), Statistical Analysis, and Power BI Dashboard Development**.

---

# 🏢 Domain

**Disaster Management & Risk Analytics**

### Problem Area

**Integrated Disaster Management Analytics**

---

# 🎯 Problem Statement

Landslide event data and emergency response data are often stored separately, making comprehensive disaster analysis difficult.

This project integrates both datasets into a unified analytical model to:

- Identify high-risk regions
- Analyze environmental factors contributing to landslides
- Evaluate emergency response efficiency
- Optimize disaster resource allocation
- Assess disaster recovery performance
- Support data-driven decision making

---

# 🎯 Project Objectives

- Integrate multiple disaster datasets
- Clean and preprocess raw data
- Perform Exploratory Data Analysis (EDA)
- Discover relationships between disaster impact and emergency response
- Build SQL queries for business analysis
- Develop interactive Power BI dashboards
- Generate business insights and recommendations

---

# 📂 Repository Structure

```
LANDSLIDE_ANALYSIS/
│
├── data/
│   ├── Raw_Dataset.xlsx
│   ├── Merged_Landslide_Data.csv
│   └── Cleaned_Landslide_Data.csv
│
├── sql/
│   ├── schema.sql
│   ├── queries.sql
│   ├── views.sql
│   └── README.md
│
├── notebooks/
│   ├── 01_Data_Cleaning.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_Statistical_Analysis.ipynb
│   └── 04_Correlation_Analysis.ipynb
│
├── dashboard/
│   ├── Landslide_Analytics.pbix
│   ├── Dashboard.pdf
│   └── Screenshots/
│
├── docs/
│   ├── Data_Dictionary.xlsx
│   ├── Profiling_Report.pdf
│   ├── Cleaning_Log.pdf
│   ├── Project_Report.pdf
│   └── Presentation.pptx
│
└── README.md
```

---

# 📊 Dataset Information

The project uses a merged dataset consisting of **52 features**, combining two related datasets through **Event_ID**.

## Dataset 1 — Landslide Event

Contains information related to:

- Event Details
- Geographic Location
- Environmental Conditions
- Disaster Severity
- Infrastructure Damage
- Human Impact
- Economic Loss

Example Features

- Event_ID
- Date
- State
- District
- Latitude
- Longitude
- Rainfall_mm
- Elevation_m
- Slope_Degree
- Soil_Type
- NDVI
- Temperature_C
- Humidity
- Distance_to_River_km
- Historical_Landslide_Count
- Casualties
- Injured
- Houses_Damaged
- Economic_Loss_INR

---

## Dataset 2 — Emergency Response

Contains operational response information including:

- Response Time
- Rescue Operations
- Human Resources
- Equipment Deployment
- Relief Activities
- Recovery Metrics

Example Features

- Response_ID
- Event_ID
- Response_Time_Min
- Rescue_Duration_Hours
- Human_Resources_Deployed
- Rescue_Teams
- NDRF_Teams
- SDRF_Teams
- Volunteers
- Ambulances
- Helicopters
- Excavators
- Relief_Camps
- Evacuated_People
- Aid_Amount_INR
- Recovery_Days
- Power_Outage_Hours

---

# 🔄 Data Analytics Workflow

```
Raw Dataset
      │
      ▼
Data Profiling
      │
      ▼
Data Cleaning
      │
      ▼
Data Integration
      │
      ▼
Exploratory Data Analysis
      │
      ▼
Statistical Analysis
      │
      ▼
SQL Analysis
      │
      ▼
Power BI Dashboard
      │
      ▼
Business Insights
```

---

# 📈 Exploratory Data Analysis

The project includes:

- Dataset Profiling
- Missing Value Analysis
- Duplicate Detection
- Data Type Validation
- Outlier Detection
- Descriptive Statistics
- Skewness Analysis
- Correlation Analysis
- Correlation Heatmaps
- Cross-table Relationship Analysis

---

# 📊 Business Analysis

## Disaster Impact Analysis

- Highest casualties by state
- District-wise economic losses
- Seasonal fatalities
- Population affected
- Infrastructure damage

## Environmental Risk Analysis

- Rainfall vs Landslide Impact
- Historical Landslide Trends
- Soil Type Analysis
- Slope & Elevation Analysis
- Weather Impact Analysis

## Emergency Response Analysis

- Average response time
- Rescue duration
- Response time vs casualties
- Rescue personnel deployment
- District-wise emergency response

## Resource Allocation Analysis

- Human resource deployment
- Equipment utilization
- Regional resource allocation
- Aid distribution
- Relief camp analysis

## Recovery Analysis

- Recovery duration
- Economic loss vs aid
- Power restoration
- Relief operation effectiveness

---

# 📊 Statistical Analysis

The project performs:

- Mean
- Median
- Mode
- Standard Deviation
- Variance
- Skewness
- Kurtosis
- Correlation Matrix
- Correlation Heatmaps

---

# 📊 Power BI Dashboard

The dashboard will include:

### Executive Overview

- Total Events
- Total Casualties
- Total Economic Loss
- Average Response Time

### Disaster Impact

- State-wise Analysis
- District-wise Analysis
- Seasonal Trends

### Emergency Response

- Response Efficiency
- Rescue Teams
- Resource Deployment

### Resource Planning

- Equipment Utilization
- Human Resources
- Aid Allocation

### Recovery Analysis

- Recovery Days
- Relief Performance
- Utility Restoration

---

# 💻 Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- MySQL
- Power BI
- Microsoft Excel
- Jupyter Notebook
- Git
- GitHub

---

# 📅 Project Roadmap

This project follows a **21-Day Data Analytics Sprint**, covering:

- Data Understanding
- Data Profiling
- Data Cleaning
- Excel Analysis
- SQL Analysis
- Python EDA
- Statistical Analysis
- Power BI Dashboard Development
- Business Insights
- Documentation
- Final Presentation

---

# 📈 Expected Outcomes

The project aims to deliver:

- Cleaned and validated datasets
- SQL-based analytical reports
- Python EDA notebooks
- Statistical insights
- Interactive Power BI dashboards
- Business recommendations
- GitHub portfolio showcasing an end-to-end data analytics workflow

---

# 🚀 Future Enhancements

- Machine Learning-based Landslide Risk Prediction
- GIS-based Interactive Maps
- Real-time Weather Data Integration
- Early Warning System
- Predictive Resource Allocation
- Automated Disaster Monitoring

---

# 👨‍💻 Author

**Tharun**

**Project:** Landslide Disaster Impact & Emergency Response Analytics

**Domain:** Disaster Management & Risk Analytics

**Tools:** Python | SQL | Excel | Power BI | Git | GitHub