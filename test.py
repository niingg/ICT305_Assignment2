import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# dataset
df = pd.read_csv('diabetes.csv')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-','_')

# helper functions for graph 1 for H1
def wilson(success, n, z=1.96):
    if n == 0: return (np.nan, np.nan)
    p = success / n
    denom = 1 + z**2/n
    center = (p + z**2/(2*n)) / denom
    half = (z*np.sqrt((p*(1-p) + z**2/(4*n)) / n)) / denom
    return center - half, center + half

def row_stats(df, col, risk_value):
    # with risk
    a = df[df[col] == risk_value]['diabetes_binary']
    n1, c1 = a.count(), a.sum()
    p1 = c1 / n1 if n1 else np.nan
    lo1, hi1 = wilson(c1, n1)
    # without risk
    b = df[df[col] != risk_value]['diabetes_binary']
    n0, c0 = b.count(), b.sum()
    p0 = c0 / n0 if n0 else np.nan
    lo0, hi0 = wilson(c0, n0)
    return p1, lo1, hi1, n1, int(c1), p0, lo0, hi0, n0, int(c0)

# graph for H1
def lifestyle_factors_chart(df):
    FACTOR_ORDER = [ 
        ("smoker", "Smoking"),
        ("physactivity", "No Physical Activity"), 
        ("fruits", "Low Fruit Intake"),            
        ("veggies", "Low Veggie Intake"),         
    ]
    RISK_VALUE = {"smoker": 1, "physactivity": 0, "fruits": 0, "veggies": 0}

    rows = []
    for col, label in FACTOR_ORDER:
        p1, lo1, hi1, n1, c1, p0, lo0, hi0, n0, c0 = row_stats(df, col, RISK_VALUE[col])
        rows.append({
            "Factor": label,
            "with_prev": p1, "with_lo": lo1, "with_hi": hi1, "with_n": n1, "with_cases": c1,
            "without_prev": p0, "without_lo": lo0, "without_hi": hi0, "without_n": n0, "without_cases": c0
        })
    tbl = pd.DataFrame(rows)

    ymax = float(pd.concat([tbl["with_prev"], tbl["without_prev"]]).max()) * 1.25
    ymax = max(0.05, ymax)

    fig = go.Figure()

    for i, y0 in enumerate(np.arange(0, ymax, 0.10)):
        if i % 2 == 0:
            fig.add_hrect(y0=y0, y1=min(y0+0.10, ymax),
                          fillcolor="#F2F4F7", line_width=0, layer="below")

    hover = "Factor: %{x}<br>%{fullData.name}: %{y:.1%}<br>n=%{customdata[0]}  cases=%{customdata[1]}<extra></extra>"

    fig.add_bar(
        name="With Risk", legendgroup="With Risk",
        x=tbl["Factor"], y=tbl["with_prev"],
        error_y=dict(type="data", array=tbl["with_hi"]-tbl["with_prev"],
                     arrayminus=tbl["with_prev"]-tbl["with_lo"], thickness=1),
        text=tbl["with_prev"].map(lambda v:f"{v:.1%}"), textposition="outside",
        marker=dict(color="#A64A47", line=dict(color="rgba(0,0,0,0.15)", width=1)),
        customdata=np.stack([tbl["with_n"], tbl["with_cases"]], axis=-1),
        hovertemplate=hover,
    )

    fig.add_bar(
        name="Without Risk", legendgroup="Without Risk",
        x=tbl["Factor"], y=tbl["without_prev"],
        error_y=dict(type="data", array=tbl["without_hi"]-tbl["without_prev"],
                     arrayminus=tbl["without_prev"]-tbl["without_lo"], thickness=1),
        text=tbl["without_prev"].map(lambda v:f"{v:.1%}"), textposition="outside",
        marker=dict(color="#E8C6AE", line=dict(color="rgba(0,0,0,0.12)", width=1)),
        customdata=np.stack([tbl["without_n"], tbl["without_cases"]], axis=-1),
        hovertemplate=hover,
    )

    fig.update_traces(cliponaxis=False, textfont_size=11)

    fig.update_layout(
        title=dict(text="Individual Lifestyle Factors<br><sup>Diabetes rate with vs without risk</sup>", x=0.02, xanchor="left"),
        barmode="group", bargap=0.28, bargroupgap=0.14,
        xaxis=dict(title="", showgrid=False, tickangle=0),
        yaxis=dict(title="Diabetes Rate (%)", tickformat=".0%", dtick=0.10,
                   range=[0, ymax], showgrid=False),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18),
        template="simple_white",
        paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=70, r=30, t=80, b=90)
    )

    return fig

# UI
# --- Page setup ---
st.set_page_config(page_title="Diabetes Risk Factors Dashboard", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Introduction", "**H1**: Lifestyle Habits and diabetes", "**H2**: Education and diabetes prevention", "**H3**: Healthcare access and diabetes", "**H4**: Self-rated health and diabetes", "**H5**: Pre-existing health conditions and diabetes", "Conclusion"])

# --- Header ---
st.markdown("<h1 style='text-align: center;'>Diabetes Risk Factors Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")  # a line separator

# --- Page content logic ---
if page == "Introduction":
    st.subheader("Introduction")
    st.write("Welcome to the Diabetes Risk Factors Dashboard. Here you can explore various factors associated with diabetes risk.")
    st.write("SALWA AND REGINA TO TWEAK THIS SECTION")

    st.subheader("Case Introduction")
    st.write("""
    Diabetes is a chronic medical condition that occurs when the body cannot properly regulate blood sugar (glucose) levels. 
    If left unmanaged, it can lead to serious health complications such as heart disease, kidney failure, and nerve damage. 

    Understanding the **risk factors** associated with diabetes is crucial for early detection and prevention. 
    This dashboard explores key health indicators and their relationship with the likelihood of developing diabetes.
    """)

    st.markdown("---")

    st.subheader("Dataset Overview")
    st.write("""
    The dataset used in this analysis is derived from the **Pima Indians Diabetes Database**, 
    which contains medical diagnostic measurements of women aged 21 and above. 
    It includes various features such as glucose concentration, BMI, blood pressure, insulin levels, and age.  

    The dataset will be used to explore five hypotheses regarding potential diabetes risk factors.
    """)

    # Display a sample of the dataset
    st.write("Here’s a glimpse of the data:")
    st.dataframe(df.head())

    # Display some basic stats
    st.write("**Basic Dataset Information:**")
    st.write(f"- Number of records: {df.shape[0]}")
    st.write(f"- Number of features: {df.shape[1]}")

    st.markdown("---")
    st.info("Use the sidebar to explore each hypothesis and see how these factors relate to diabetes risk.")
    
elif page == "**H1**: Lifestyle Habits and diabetes":
    st.subheader("Hypothesis 1: Lifestyle Habits and diabetes")
    st.write("**Hypothesis**: Modifiable behaviours – including smoking, physical inactivity, insufficient fruit and vegetable intake, and heavy alcohol consumption – are associated with a higher risk of diabetes.")
    st.write("Let's explore all variables first. The graph below shows how each lifestyle habit relates to diabetes prevalence in the dataset.")
    # st.write("Rationale: Lifestyle factors are the most modifiable determinants of health. Demonstrating their impact provides evidence for targeted prevention campaigns and behavioural interventions.")

    # Add optional filters
    age_group = st.selectbox("Select Age Group:", options=["All"] + list(df["age"].unique()))
    education = st.selectbox("Select Education Level:", options=["All"] + list(df["education"].unique()))

    filtered_df = df.copy()
    if age_group != "All":
        filtered_df = filtered_df[filtered_df["age"] == age_group]
    if education != "All":
        filtered_df = filtered_df[filtered_df["education"] == education]

    # Show interactive chart
    fig = lifestyle_factors_chart(filtered_df)
    st.plotly_chart(fig, use_container_width=True)
    
elif page == "**H2**: Education and diabetes prevention":
    st.subheader("Hypothesis 2")
    st.write("Content for Hypothesis 2 will go here.")
    
elif page == "**H3**: Healthcare access and diabetes":
    st.subheader("Hypothesis 3")
    st.write("Content for Hypothesis 3 will go here.")
    
elif page == "**H4**: Self-rated health and diabetes":
    st.subheader("Hypothesis 4")
    st.write("Content for Hypothesis 4 will go here.")
    
elif page == "**H5**: Pre-existing health conditions and diabetes":
    st.subheader("Hypothesis 5")
    st.write("Content for Hypothesis 5 will go here.")
    
elif page == "Conclusion":
    st.subheader("Conclusion")
    st.write("Summary of findings and insights will go here.")





