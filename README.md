🩺 Diabetes Risk Factors Interactive Dashboard
📌 Project Overview

This project is an interactive data visualisation dashboard built using Streamlit and Plotly to explore the key factors influencing diabetes risk.

Rather than presenting raw statistics, the dashboard transforms a complex healthcare dataset into an intuitive, story-driven experience. Users can explore how different lifestyle, demographic, healthcare, and medical factors contribute to diabetes risk in a structured and interactive way.

🎯 Problem Statement

Diabetes is a growing global health concern, including in developed countries like Singapore. While large volumes of health data exist, they are often:

Too technical for the general public
Scattered across multiple sources
Difficult to interpret holistically

As a result, individuals and policymakers may struggle to understand what truly drives diabetes risk.

🎯 Project Goal

The goal of this dashboard is to:

Centralise key diabetes-related risk factors
Translate complex data into clear visual insights
Enable users to explore relationships interactively
Support better awareness and decision-making around diabetes prevention

🧠 Narrative Structure

The dashboard is structured as a progressive story, moving from least to most impactful risk factors:

Lifestyle Habits
Education & Demographics
Healthcare Access
Self-Rated Health
Pre-Existing Health Conditions

This progression helps users build understanding step-by-step before reaching deeper, more impactful insights.

📊 Dataset

The dataset used is the CDC Diabetes Health Indicators Dataset, sourced from the UCI Machine Learning Repository.

It includes:

22 health-related variables
Lifestyle behaviours (diet, exercise, smoking, etc.)
Demographics (age, income, education, BMI)
Healthcare access indicators
Medical history and pre-existing conditions

📎 Source: https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators

🧪 Hypotheses

Five hypotheses were derived from grouped variables:

H1: Lifestyle Habits → Diabetes Risk
H2: Education & Demographics → Diabetes Risk
H3: Healthcare Access → Diabetes Risk
H4: Self-Rated Health → Diabetes Risk
H5: Pre-Existing Conditions → Diabetes Risk

Each hypothesis is explored through multiple interactive visualisations.

📊 Dashboard Features

The dashboard includes:

Interactive Plotly charts
Dropdown filters for demographic exploration
Tab-based navigation per hypothesis
Comparative visual analysis across risk factors
Sankey diagram showing relationships between variables and conclusions
Clean UI styling with custom Streamlit components
🧭 How to Run the Project Locally
1. Clone the repository
git clone https://github.com/niingg/ICT305_Assignment2.git
cd ICT305_Assignment2
2. Install dependencies
pip install -r requirements.txt
3. Run the Streamlit app
streamlit run app.py
🛠️ Technologies Used
Python 🐍
Streamlit
Plotly
Pandas
NumPy
📌 Key Insights
Lifestyle habits significantly influence diabetes risk
Higher education levels are associated with healthier behaviours and lower risk
Healthcare access alone does not fully prevent diabetes
Self-rated health strongly correlates with actual diabetes prevalence
Pre-existing conditions are the strongest indicator of diabetes risk
👥 Team Members
Gizella
Natthida
Regina
Salwa
Yee Lin
📈 Conclusion

This dashboard demonstrates that diabetes is not caused by a single factor, but rather a combination of behavioural, social, and medical influences.

By visualising these relationships in an interactive format, the project helps users better understand not just who is at risk — but why.

📎 License

This project is developed for academic purposes as part of ICT305 coursework.
