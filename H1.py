##imports
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from ipywidgets import VBox, HBox, Dropdown, ToggleButtons, Output
from IPython.display import display

## read dataset
df_brfss = pd.read_csv("diabetes.csv")

## standardising column names 
df_brfss.columns = df_brfss.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-','_')

## Individual Lifestyle Factors vs. Diabetes
FACTOR_ORDER = [
    ("smoker",            "Smoking"),
    ("physactivity",      "No Physical Activity"),
    ("fruits",            "Low Fruit Intake"),
    ("veggies",           "Low Veggie Intake"),
    ("hvyalcoholconsump", "Heavy Alcohol Consumption"),
]
RISK_VALUE = {"smoker":1, "physactivity":0, "fruits":0, "veggies":0, "hvyalcoholconsump":1}
COLORS = {"With Risk": "#A64A47", "Without Risk": "#E8C6AE"}  

need = {k for k,_ in FACTOR_ORDER} | {"diabetes_binary"}
missing = need - set(df_brfss.columns)
assert not missing, f"Missing columns: {missing}"

df_long = df_brfss.melt(
    id_vars="diabetes_binary",
    value_vars=[k for k,_ in FACTOR_ORDER],
    var_name="factor",
    value_name="value"
)

df_long["risk_val"] = df_long["factor"].map(RISK_VALUE)
df_long["group"]    = np.where(df_long["value"] == df_long["risk_val"], "With Risk", "Without Risk")
label_map = dict(FACTOR_ORDER)
df_long["Factor"] = df_long["factor"].map(label_map)

g = df_long.groupby(["Factor","group"])["diabetes_binary"]
summary = g.agg(sum="sum", n="count", prev="mean").reset_index()

cat_order = [lbl for _, lbl in FACTOR_ORDER]
summary["Factor"] = pd.Categorical(summary["Factor"], categories=cat_order, ordered=True)
summary = summary.sort_values(["Factor","group"])

ymax = max(0.05, float(summary["prev"].max()) * 1.25)
ymax = min(1.0, ymax)  

fig = go.Figure()

for i, y0 in enumerate(np.arange(0, ymax, 0.10)):
    if i % 2 == 0:
        fig.add_hrect(y0=y0, y1=min(y0+0.10, ymax),
                      fillcolor="#F2F4F7", line_width=0, layer="below")

buttons = []
total_traces = 2 * len(cat_order)

for fi, f_label in enumerate(cat_order):
    sub = summary[summary["Factor"] == f_label]
    for group_name in ["With Risk", "Without Risk"]:
        s = sub[sub["group"] == group_name]
        fig.add_bar(
            name=group_name,
            legendgroup=group_name,
            showlegend=(fi == 0),               
            x=s["Factor"],                       
            y=s["prev"],
            text=(s["prev"]*100).round(1).astype(str) + "%",
            textposition="outside",
            marker=dict(color=COLORS[group_name],
                        line=dict(color="rgba(0,0,0,0.12)", width=1)),
            customdata=np.stack([s["n"], s["sum"]], axis=-1),
            hovertemplate=(
                "Factor: %{x}<br>%{fullData.name}: %{y:.1%}"
                "<br>n=%{customdata[0]}  cases=%{customdata[1]}"
                "<extra></extra>"
            ),
            offsetgroup=group_name
        )

initial_vis = [False] * total_traces
initial_vis[0] = True; initial_vis[1] = True  
for i, vis in enumerate(initial_vis):
    fig.data[i].visible = vis

for fi, f_label in enumerate(cat_order):
    vis = [False]*total_traces
    vis[2*fi] = True; vis[2*fi+1] = True
    buttons.append(dict(
        label=f_label,
        method="update",
        args=[{"visible": vis},
              {"xaxis": {"title": "",
                         "categoryorder": "array",
                         "categoryarray": [f_label]}}]
    ))

fig.update_traces(cliponaxis=False, textfont_size=11)
fig.update_layout(
    title=dict(text="Individual Lifestyle Factors<br><sup>Diabetes rate with vs without risk</sup>",
               x=0.02, xanchor="left"),
    barmode="group", bargap=0.28, bargroupgap=0.14,
    xaxis=dict(title="Lifestyle Factors", showgrid=False),
    yaxis=dict(title="Diabetes Rate (%)", tickformat=".0%", dtick=0.10, range=[0, ymax], showgrid=False),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18),
    template="simple_white",
    margin=dict(l=70, r=30, t=80, b=90),
    updatemenus=[dict(
        type="dropdown", x=1.0, xanchor="right", y=1.12, yanchor="top",
        buttons=buttons, direction="down", pad={"r": 6, "t": 6}
    )]
)

fig.show()

## diabetes rate with vs without risk
need = {k for k,_ in FACTOR_ORDER} | {"diabetes_binary"}
missing = need - set(df_brfss.columns)
assert not missing, f"Missing columns: {missing}"

df_long = df_brfss.melt(
    id_vars="diabetes_binary",
    value_vars=[k for k,_ in FACTOR_ORDER],
    var_name="factor",
    value_name="value"
)
risk_map = pd.Series(RISK_VALUE)
df_long["group"] = np.where(df_long["value"] == df_long["factor"].map(risk_map),
                            "With Risk", "Without Risk")
label_map = dict(FACTOR_ORDER)
df_long["Factor"] = df_long["factor"].map(label_map)

summary = (df_long
           .groupby(["Factor","group"])["diabetes_binary"]
           .agg(sum="sum", n="count", prev="mean")
           .reset_index())

cat_order = [lbl for _, lbl in FACTOR_ORDER]
summary["Factor"] = pd.Categorical(summary["Factor"], categories=cat_order, ordered=True)
summary = summary.sort_values(["Factor","group"])

# plot
ymax = max(0.05, float(summary["prev"].max()) * 1.25)
ymax = min(1.0, ymax)  # cap at 100%

fig = go.Figure()

for i, y0 in enumerate(np.arange(0, ymax, 0.10)):
    if i % 2 == 0:
        fig.add_hrect(y0=y0, y1=min(y0+0.10, ymax),
                      fillcolor="#F2F4F7", line_width=0, layer="below")

hover = (
    "Factor: %{x}<br>%{fullData.name}: %{y:.1%}"
    "<br>n=%{customdata[0]}  cases=%{customdata[1]}<extra></extra>"
)

for name, color in [("With Risk","#A64A47"), ("Without Risk","#E8C6AE")]:
    s = summary[summary["group"] == name]
    fig.add_bar(
        name=name, legendgroup=name,
        x=s["Factor"], y=s["prev"],
        text=(s["prev"]*100).round(1).astype(str) + "%",
        textposition="outside",
        marker=dict(color=color, line=dict(color="rgba(0,0,0,0.12)", width=1)),
        customdata=np.stack([s["n"], s["sum"]], axis=-1),
        hovertemplate=hover,
        offsetgroup=name
    )

fig.update_traces(cliponaxis=False, textfont_size=11)
fig.update_layout(
    title=dict(text="Individual Lifestyle Factors<br><sup>Diabetes rate with vs without risk</sup>",
               x=0.02, xanchor="left"),
    barmode="group", bargap=0.28, bargroupgap=0.14,
    xaxis=dict(title="Lifestyle Factors", showgrid=False),
    yaxis=dict(title="Diabetes Rate (%)", tickformat=".0%", dtick=0.10, range=[0, ymax], showgrid=False),
    legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18),
    template="simple_white",
    margin=dict(l=70, r=30, t=80, b=90)
)

fig.show()

## grouped by age group
RISK_VALUE = {"smoker":1, "physactivity":0, "fruits":0, "veggies":0, "hvyalcoholconsump":1}
COLOR_MAP  = {"With Risk":"#A64A47", "Without Risk":"#E8C6AE"}
AGE_ORDER  = ["18–29","30–44","45–59","60–74","75+"]
CAT_ORDER  = [lbl for _, lbl in FACTOR_ORDER]

d = df_brfss.copy()
d.columns = d.columns.str.lower()

db = pd.to_numeric(d.get("diabetes_binary"), errors="coerce")
d = d.assign(diabetes_binary=(db == 1).astype(float)).dropna(subset=["diabetes_binary"])

if "age" in d.columns:
    age = pd.to_numeric(d["age"], errors="coerce")
    if age.dropna().between(1,13).all():
        def _map_code(a):
            if a in (1,2): return "18–29"
            if a in (3,4,5): return "30–44"
            if a in (6,7,8): return "45–59"
            if a in (9,10,11): return "60–74"
            if a in (12,13): return "75+"
            return np.nan
        d["agegroup"] = age.astype("Int64").map(_map_code)
    else:
        d["agegroup"] = pd.cut(age, [18,30,45,60,75,np.inf],
                               labels=AGE_ORDER, right=False, include_lowest=True)

fcols = [k for k,_ in FACTOR_ORDER]
idvars = ["diabetes_binary"] + (["agegroup"] if "agegroup" in d.columns else [])
df_long = d.melt(id_vars=idvars, value_vars=fcols,
                 var_name="factor", value_name="value")
df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce").where(lambda s: s.isin([0,1]))
df_long = df_long.dropna(subset=["value"])

risk_map = pd.Series(RISK_VALUE)
df_long["group"] = np.where(df_long["value"] == df_long["factor"].map(risk_map),
                            "With Risk", "Without Risk")
df_long["Factor"] = pd.Categorical(df_long["factor"].map(dict(FACTOR_ORDER)),
                                   categories=CAT_ORDER, ordered=True)

gkeys = ["Factor","group"] + (["agegroup"] if "agegroup" in df_long.columns else [])
summary = (df_long.groupby(gkeys, observed=True)["diabetes_binary"]
                  .agg(sum="sum", n="count", prev="mean")
                  .reset_index())
summary["text"] = (summary["prev"]*100).round(1).astype(str) + "%"

ymax = min(1.0, max(0.05, float(summary["prev"].max())*1.25))

fig = px.bar(
    summary, x="Factor", y="prev", color="group",
    barmode="group", text="text",
    animation_frame=("agegroup" if "agegroup" in summary.columns else None),
    color_discrete_map=COLOR_MAP,
    category_orders={"Factor": CAT_ORDER, "agegroup": AGE_ORDER},
    title="Diabetes Rate by Lifestyle Behaviour" + ("" if "agegroup" not in summary.columns else " — by Age Group")
)

fig.update_traces(
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>%{legendgroup}: %{y:.1%}<br>n=%{customdata[0]}  cases=%{customdata[1]}<extra></extra>",
    customdata=np.c_[summary["n"], summary["sum"]],
    marker_line_width=1, marker_line_color="rgba(0,0,0,0.12)"
)

for i, y0 in enumerate(np.arange(0, ymax, 0.10)):
    if i % 2 == 0:
        fig.add_hrect(y0=y0, y1=min(y0+0.10, ymax),
                      fillcolor="#F2F4F7", line_width=0, layer="below")

fig.update_layout(
    template="simple_white",
    bargap=0.28, bargroupgap=0.14, showlegend=True,
    xaxis=dict(title="", showgrid=False, categoryorder="array", categoryarray=CAT_ORDER),
    yaxis=dict(title="Diabetes Rate (%)", tickformat=".0%", dtick=0.10, range=[0, ymax], showgrid=False),
    margin=dict(l=70, r=30, t=80, b=80)
)

fig.show()

## Count lifestyle risks per person (smoking, inactivity, low fruit/veg, heavy alcohol), compute diabetes prevalence for 0,1,2,3,4+ factors
df = df_brfss.copy()
cols = {
    "smoke":    ("smoker",            1),
    "inactive": ("physactivity",      0),
    "lowfruit": ("fruits",            0),
    "lowveg":   ("veggies",           0),
    "heavyalc": ("hvyalcoholconsump", 1),
}

rb = pd.DataFrame(index=df.index)
for new, (col, risky) in cols.items():
    if col in df.columns:
        rb[new] = (pd.to_numeric(df[col], errors="coerce") == risky).astype(int)

if rb.shape[1] == 0:
    rb["none"] = 0  

df["risk_behaviors"] = rb.sum(axis=1).fillna(0).astype(int)

order = ["0 factors","1 factor","2 factors","3 factors","4+ factors"]
labels = lambda k: "4+ factors" if k >= 4 else f"{k} factor{'s' if k != 1 else ''}"

prev_rb = (df.assign(diabetes_binary=(pd.to_numeric(df["diabetes_binary"], errors="coerce") == 1).astype(float))
             .groupby("risk_behaviors", as_index=False)["diabetes_binary"].mean()
             .rename(columns={"diabetes_binary":"prevalence"}))

prev_rb["group"] = prev_rb["risk_behaviors"].map(labels)
prev_rb = (prev_rb.groupby("group", as_index=False)["prevalence"].mean())
prev_rb["group"] = pd.Categorical(prev_rb["group"], categories=order, ordered=True)
prev_rb = prev_rb.sort_values("group")

# Plot
ymax = min(1.0, max(0.05, float(prev_rb["prevalence"].max()) * 1.25))
step = 0.10

fig = go.Figure(go.Bar(
    x=prev_rb["group"].astype(str),
    y=prev_rb["prevalence"],
    text=(prev_rb["prevalence"]*100).round(1).astype(str) + "%",
    textposition="outside",
    marker=dict(color="#a64a47", line=dict(width=1, color="rgba(0,0,0,0.15)")),
    hovertemplate="<b>%{x}</b><br>Diabetes rate: %{y:.1%}<extra></extra>",
    cliponaxis=False
))

for i, y0 in enumerate(np.arange(0, ymax, step)):
    if i % 2 == 0:
        fig.add_hrect(y0=y0, y1=min(y0+step, ymax),
                      fillcolor="#F2F4F7", line_width=0, layer="below")

fig.update_layout(
    title=dict(text="Diabetes prevalence increases with multiple lifestyle risk factors", x=0.02),
    template="simple_white",
    bargap=0.35, showlegend=False,
    margin=dict(l=60, r=20, t=60, b=60),
    xaxis=dict(title="Number of factors", categoryorder="array",
               categoryarray=order, showgrid=False),
    yaxis=dict(title="Diabetes Rate (%)", tickformat=".0%", dtick=0.10,
               range=[0, ymax], showgrid=False),
    uniformtext_minsize=10, uniformtext_mode="hide",
    paper_bgcolor="white", plot_bgcolor="white"
)

fig.show()

## relative risk radar
FACTOR_ORDER = [
    ("smoker",            "Smoking"),
    ("physactivity",      "No Physical Activity"),
    ("fruits",            "Low Fruit Intake"),
    ("veggies",           "Low Veggie Intake"),
    ("hvyalcoholconsump", "Heavy Alcohol Consumption"),
]
RISK_VALUE = {"smoker":1, "physactivity":0, "fruits":0, "veggies":0, "hvyalcoholconsump":1}
CAT_ORDER  = [label for _, label in FACTOR_ORDER]

df = df_brfss.copy()
df.columns = df.columns.str.lower()
df["diab01"] = (pd.to_numeric(df["diabetes_binary"], errors="coerce") == 1).astype(float)

fcols = [k for k,_ in FACTOR_ORDER if k in df.columns]
for c in fcols:
    df[c] = pd.to_numeric(df[c], errors="coerce").where(lambda s: s.isin([0,1]))

long = df.melt(id_vars="diab01", value_vars=fcols, var_name="factor", value_name="value").dropna()
long["group"]  = np.where(long["value"] == long["factor"].map(RISK_VALUE), "With Risk", "Without Risk")
long["Factor"] = pd.Categorical(long["factor"].map(dict(FACTOR_ORDER)), categories=CAT_ORDER, ordered=True)

df_bars = (long.groupby(["Factor","group"], observed=True)["diab01"]
                .mean()
                .unstack("group")
                .reindex(CAT_ORDER)
                .reset_index())

wr = df_bars["With Risk"].astype(float).to_numpy()
wo = df_bars["Without Risk"].astype(float).to_numpy()
ratio = np.divide(wr, wo, out=np.full_like(wr, np.nan), where=wo > 0)
df_bars["% Increase"] = (ratio - 1) * 100

factors = df_bars["Factor"].astype(str).to_numpy()
delta   = df_bars["% Increase"].astype(float).to_numpy()

theta = np.r_[factors, factors[:1]] if len(factors) else factors
r     = np.r_[delta,   delta[:1]]   if len(delta)   else delta

vmax = np.nanmax(delta) if np.isfinite(delta).any() else 0.0
vmin = np.nanmin(delta) if np.isfinite(delta).any() else 0.0
rmax = max(10.0, 10.0 * np.ceil((vmax*1.10)/10.0))
rmin = 10.0 * np.floor((min(0.0, vmin*1.10))/10.0)

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    theta=theta, r=r,
    mode="lines",
    line=dict(color="#a64a47", width=3, shape="spline"),
    fill="toself", fillcolor="rgba(166,74,71,0.22)",
    hoverinfo="text",
    text=[f"{lab}: {val:+.1f}%" for lab, val in zip(theta, r)],
    hovertext=[f"<b>{lab}</b><br>Δ risk: {val:+.1f}%" for lab, val in zip(theta, r)],
    showlegend=False
))

fig.add_trace(go.Scatterpolar(
    theta=factors, r=delta,
    mode="markers+text",
    marker=dict(size=8, color="#a64a47", line=dict(width=1, color="rgba(0,0,0,0.2)")),
    text=[f"{v:+.0f}%" if np.isfinite(v) else "" for v in delta],
    textposition="top center",
    hovertemplate="<b>%{theta}</b><br>Δ risk: %{r:+.1f}%<extra></extra>",
    showlegend=False
))

fig.update_layout(
    title=dict(text="Relative Risk Comparison<br><sup>% change in diabetes rate by factor</sup>", x=0.03, xanchor="left"),
    template="simple_white",
    polar=dict(
        bgcolor="white",
        angularaxis=dict(rotation=90, direction="clockwise"),
        radialaxis=dict(range=[rmin, rmax], tick0=0, dtick=10, ticksuffix="%")
    ),
    margin=dict(l=40, r=40, t=80, b=40)
)

fig.show()

## Physical Activity vs Diabetes by Education, AgeGroup and Sex
EDU_MAP = {
    1: "K-only / None",
    2: "Grades 1–8",
    3: "Grades 9–11",
    4: "HS Grad / GED",
    5: "Some College / AA",
    6: "College 4+",
}
EDU_ORDER = [EDU_MAP[k] for k in (1,2,3,4,5,6)]
AGE_ORDER = ["18–29","30–44","45–59","60–74","75+"]

COLOR_NO  = "#a64a47"   # inactive = No
COLOR_YES = "#D6B4B3"   # active   = Yes
GRID      = "#e9eef3"

def normalize(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    df.columns = df.columns.str.lower()

    # diabetes -> 0/1
    db = pd.to_numeric(df.get("diabetes_binary"), errors="coerce")
    df["diabetes"] = (db == 1).astype(float)

    # physactivity -> Yes/No
    pa = pd.to_numeric(df.get("physactivity"), errors="coerce")
    pa = pa.where(pa.isin([0,1]), np.where(pa == 1, 1, 0))  
    df["phys_lbl"] = np.where(pa == 1, "Yes", "No")

    age = pd.to_numeric(df.get("age"), errors="coerce")
    if age.dropna().between(1,13).all():
        def map_agecode(a):
            if a in (1,2): return "18–29"
            if a in (3,4,5): return "30–44"
            if a in (6,7,8): return "45–59"
            if a in (9,10,11): return "60–74"
            if a in (12,13): return "75+"
            return np.nan
        df["agegroup"] = age.astype("Int64").map(map_agecode)
    else:
        df["agegroup"] = pd.cut(age, [18,30,45,60,75,np.inf],
                                labels=AGE_ORDER, right=False, include_lowest=True)

    edu = pd.to_numeric(df.get("education"), errors="coerce").astype("Int64")
    df["education_lbl"] = pd.Categorical(edu.map(EDU_MAP),
                                         categories=EDU_ORDER, ordered=True)

    sex_raw = df.get("sex")
    if sex_raw is not None:
        s = pd.to_numeric(sex_raw, errors="coerce")
        if s.dropna().isin([0,1]).all():
            df["sex_lbl"] = s.map({0:"Female", 1:"Male"})
        elif s.dropna().isin([1,2]).all():
            df["sex_lbl"] = s.map({1:"Male", 2:"Female"})
        else:
            v = sex_raw.astype(str).str.lower().str.strip()
            df["sex_lbl"] = np.where(v.isin(["f","female"]), "Female",
                              np.where(v.isin(["m","male"]), "Male", np.nan))
    else:
        df["sex_lbl"] = np.nan

    return df

def make_table(df: pd.DataFrame, facet_var: str) -> pd.DataFrame:
    sub = df.dropna(subset=["diabetes","phys_lbl", facet_var]).copy()
    g = (sub.groupby([facet_var, "phys_lbl"], observed=True)
           .agg(n=("diabetes","size"), cases=("diabetes","sum"))
           .reset_index())
    g["prev"] = g["cases"] / g["n"]
    g["phys_lbl"] = pd.Categorical(g["phys_lbl"], ["No","Yes"], ordered=True)
    if facet_var == "agegroup":
        g["agegroup"] = pd.Categorical(g["agegroup"], AGE_ORDER, ordered=True)
    if facet_var == "education_lbl":
        g["education_lbl"] = pd.Categorical(g["education_lbl"], EDU_ORDER, ordered=True)
    return g.sort_values([facet_var, "phys_lbl"]).reset_index(drop=True)

def facet_plot(tbl: pd.DataFrame, facet_var: str, title_note: str):
    category_orders = {"phys_lbl":["No","Yes"]}
    if facet_var == "agegroup":       category_orders["agegroup"] = AGE_ORDER
    if facet_var == "education_lbl":  category_orders["education_lbl"] = EDU_ORDER

    fig = px.bar(
        tbl, x="phys_lbl", y="prev",
        facet_col=facet_var, facet_col_wrap=3,
        color="phys_lbl",
        category_orders=category_orders,
        color_discrete_map={"No": COLOR_NO, "Yes": COLOR_YES},
        text=tbl["prev"].map(lambda v: f"{v:.0%}"),
        title=f"Physical Activity vs Diabetes by {title_note}<br><sup>% with diabetes — faceted</sup>"
    )
    fig.update_traces(
        marker_line_width=1, marker_line_color="rgba(0,0,0,0.15)",
        textposition="outside",
        hovertemplate="%{x}<br>%{y:.1%}<extra></extra>"
    )
    fig.for_each_yaxis(lambda a: a.update(title="% Diabetes", tickformat=".0%", dtick=0.10, range=[0,1], gridcolor=GRID))
    fig.for_each_xaxis(lambda a: a.update(title="Physically Active"))
    fig.update_layout(template="simple_white", bargap=0.35, showlegend=False,
                      margin=dict(l=50, r=20, t=70, b=50))
    return fig

def animate_by_age(tbl_age: pd.DataFrame):
    frames = []
    for ag in AGE_ORDER:
        t = tbl_age[tbl_age["agegroup"] == ag]
        if t.empty: 
            continue
        frames.append(go.Frame(
            name=str(ag),
            data=[go.Bar(
                x=t["phys_lbl"], y=t["prev"],
                text=t["prev"].map(lambda v: f"{v:.0%}"),
                marker_line_width=1, marker_line_color="rgba(0,0,0,0.15)",
                marker_color=[COLOR_NO if v=="No" else COLOR_YES for v in t["phys_lbl"]],
                showlegend=False,
                hovertemplate="%{x}<br>%{y:.1%}<extra></extra>"
            )]
        ))

    fig = go.Figure(data=(frames[0].data if frames else []), frames=frames)
    fig.update_layout(
        title="Physical Activity vs Diabetes — Animated by Age Group",
        template="simple_white",
        xaxis=dict(title="Physically Active", categoryorder="array", categoryarray=["No","Yes"]),
        yaxis=dict(title="% Diabetes", tickformat=".0%", dtick=0.10, range=[0,1], gridcolor=GRID),
        updatemenus=[dict(type="buttons", showactive=False, x=1, y=1.12, xanchor="right",
                          buttons=[
                              dict(label="▶ Play",  method="animate", args=[None, {"fromcurrent": True, "frame": {"duration": 900, "redraw": True}, "transition": {"duration": 200}}]),
                              dict(label="⏸ Pause", method="animate", args=[[None], {"mode":"immediate", "frame":{"duration":0,"redraw":False}, "transition":{"duration":0}}])
                          ])],
        sliders=[dict(
            active=0, x=0.05, y=1.05, xanchor="left", len=0.7,
            currentvalue=dict(prefix="Age Group: ", visible=True),
            steps=[dict(method="animate", label=f.name, args=[[f.name], {"mode":"immediate","frame":{"duration":0,"redraw":True}, "transition":{"duration":0}}]) for f in frames]
        )],
        margin=dict(l=50, r=20, t=90, b=50)
    )
    return fig

def show_physactivity(df_brfss: pd.DataFrame):
    df = normalize(df_brfss)

    facet_dd = Dropdown(
        options=[("Education","education_lbl"), ("Age Group","agegroup"), ("Sex","sex_lbl")],
        value="education_lbl", description="Facet:"
    )
    view_toggle = ToggleButtons(
        options=[("Faceted","facet"), ("Animate by Age","animate")],
        value="facet", description="View:"
    )
    out = Output()

    def render(*_):
        out.clear_output(wait=True)
        with out:
            if view_toggle.value == "facet":
                tbl = make_table(df, facet_dd.value)
                pretty = dict(education_lbl="Education", agegroup="Age Group", sex_lbl="Sex")[facet_dd.value]
                fig = facet_plot(tbl, facet_var=facet_dd.value, title_note=pretty)
                fig.show()
            else:
                tbl_age = make_table(df, "agegroup")
                fig = animate_by_age(tbl_age)
                fig.show()

    facet_dd.observe(render, names="value")
    view_toggle.observe(render, names="value")

    render()
    display(VBox([HBox([facet_dd, view_toggle]), out]))

show_physactivity(df_brfss)