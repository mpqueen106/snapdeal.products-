import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ---------------------------
# Sample subcategory data
# ---------------------------
data = {
    "subcategory": [
        "subcat_1","subcat_4","subcat_6","subcat_15","subcat_8",
        "subcat_14","subcat_9","subcat_19","subcat_18","subcat_5",
        "subcat_12","subcat_10","subcat_11","subcat_13","subcat_20",
        "subcat_7","subcat_17","subcat_16","subcat_3","subcat_2"
    ],
    "avg_price": [
        32, 31.8, 31.5, 30.8, 30.2, 29.9, 29.7, 29.0, 28.4, 28.6,
        27.2, 26.9, 26.7, 26.5, 26.6, 26.4, 26.3, 25.6, 25.2, 24.8
    ],
    "avg_rating": [
        4.0, 3.98, 3.96, 3.94, 3.99, 3.95, 3.97, 4.1, 4.05, 4.02,
        4.05, 3.99, 3.96, 3.94, 3.92, 3.88, 3.90, 3.92, 3.98, 4.05
    ],
    "count": np.random.randint(44, 65, 20)
}

df = pd.DataFrame(data)

# ---------------------------
# 1️⃣ Bubble plot
# ---------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(
    data=df,
    x="avg_price",
    y="avg_rating",
    size="count",
    sizes=(100, 600),
    hue="count",
    palette="viridis",
    legend=True
)
plt.xscale("log")
plt.title("Avg Price vs Rating by Subcategory")
plt.xlabel("Avg Price (log)")
plt.ylabel("Avg Rating")
plt.tight_layout()
plt.show()

# ---------------------------
# 2️⃣ Bar + Line chart
# ---------------------------
fig, ax1 = plt.subplots(figsize=(10,6))

ax1.bar(df["subcategory"], df["avg_price"], alpha=0.7)
ax1.set_ylabel("Avg Price")
ax1.set_xticklabels(df["subcategory"], rotation=45, ha="right")

ax2 = ax1.twinx()
ax2.plot(df["subcategory"], df["avg_rating"], marker="o")
ax2.set_ylabel("Avg Rating")

plt.title("Avg Price & Rating by Subcategory")
plt.tight_layout()
plt.show()