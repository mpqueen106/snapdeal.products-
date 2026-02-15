import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import plotly.io as pio
import webbrowser
import os

pio.renderers.default = "browser"

# -----------------------------
# Data Generation
# -----------------------------
np.random.seed(42)

df = pd.DataFrame({
    "date": pd.date_range(start="2025-01-01", periods=90, freq="D"),
    "discount": np.random.uniform(5, 30, 90),
    "product_category": np.random.choice(
        ["Electronics", "Clothing", "Food"], 90
    ),
    "region": np.random.choice(["North", "South", "East"], 90),
})

# -----------------------------
# Graph 1
# -----------------------------
daily_avg = df.groupby("date", as_index=False)["discount"].mean()
fig1 = px.line(daily_avg, x="date", y="discount",
               title="1. Daily Average Discount")

# -----------------------------
# Graph 2
# -----------------------------
fig2 = px.area(daily_avg, x="date", y="discount",
               title="2. Area Chart")

# -----------------------------
# Graph 3
# -----------------------------
cat_trend = df.groupby(
    ["date", "product_category"],
    as_index=False
)["discount"].mean()

fig3 = px.line(cat_trend, x="date", y="discount",
               color="product_category",
               title="3. Category-wise Trend")

# -----------------------------
# Graph 4
# -----------------------------
df["month"] = df["date"].dt.to_period("M")
monthly = df.groupby("month")["discount"].agg(
    avg="mean", std="std"
).reset_index()
monthly["month"] = monthly["month"].astype(str)

fig4 = go.Figure()
fig4.add_bar(x=monthly["month"], y=monthly["std"], name="Std Dev")
fig4.add_scatter(x=monthly["month"], y=monthly["avg"],
                 mode="lines+markers", name="Average", yaxis="y2")
fig4.update_layout(
    title="4. Monthly Statistics",
    yaxis2=dict(overlaying="y", side="right")
)

# -----------------------------
# Graph 5
# -----------------------------
x = np.arange(len(daily_avg))
slope, intercept, r, p, err = stats.linregress(x, daily_avg["discount"])
trend = slope * x + intercept

fig5 = go.Figure()
fig5.add_scatter(x=daily_avg["date"], y=daily_avg["discount"],
                 mode="lines", name="Daily Avg")
fig5.add_scatter(x=daily_avg["date"], y=trend,
                 mode="lines", name=f"Trend (R²={r**2:.3f})",
                 line=dict(dash="dash"))
fig5.update_layout(title="5. Linear Trend")

# -----------------------------
# CORRECT HTML COMBINE
# -----------------------------
html = f"""
<html>
<head>
<title>All Discount Graphs</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>

<h2>Graph 1</h2>
{fig1.to_html(full_html=False)}

<h2>Graph 2</h2>
{fig2.to_html(full_html=False)}

<h2>Graph 3</h2>
{fig3.to_html(full_html=False)}

<h2>Graph 4</h2>
{fig4.to_html(full_html=False)}

<h2>Graph 5</h2>
{fig5.to_html(full_html=False)}

</body>
</html>
"""

file_name = "all_discount_graphs.html"
with open(file_name, "w", encoding="utf-8") as f:
    f.write(html)

webbrowser.open("file://" + os.path.realpath(file_name))

print("✅ ALL 5 GRAPHS DISPLAYED SUCCESSFULLY")