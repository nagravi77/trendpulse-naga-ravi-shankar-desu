import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os


# 1 — Setup


df = pd.read_csv("data/trends_analysed.csv")
os.makedirs("outputs", exist_ok=True)

# Shared colour palette
PALETTE   = ["#FF6B6B", "#FFB347", "#4ECDC4", "#45B7D1", "#96CEB4"]
BG        = "#0F1117"
CARD      = "#1A1D27"
TEXT      = "#E8EAF0"
SUBTEXT   = "#8B90A7"
GRID      = "#252836"

def apply_dark_style(ax, title, xlabel, ylabel):
    ax.set_facecolor(CARD)
    ax.set_title(title, color=TEXT, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, color=SUBTEXT, fontsize=10)
    ax.set_ylabel(ylabel, color=SUBTEXT, fontsize=10)
    ax.tick_params(colors=SUBTEXT, labelsize=9)
    ax.spines[:].set_color(GRID)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)


# 2 — Chart 1: Top 10 Stories by Score


top10 = df.nlargest(10, "score").copy()
top10["short_title"] = top10["title"].apply(
    lambda t: t[:50] + "…" if len(t) > 50 else t
)

fig1, ax1 = plt.subplots(figsize=(10, 6))
fig1.patch.set_facecolor(BG)

colors1 = [PALETTE[i % len(PALETTE)] for i in range(len(top10))]
bars = ax1.barh(top10["short_title"], top10["score"], color=colors1,
                height=0.65, zorder=3)

# Value labels on bars
for bar in bars:
    w = bar.get_width()
    ax1.text(w + 10, bar.get_y() + bar.get_height() / 2,
             f"{w:,}", va="center", ha="left", color=SUBTEXT, fontsize=8)

ax1.invert_yaxis()
apply_dark_style(ax1, "Top 10 Stories by Score", "Score", "Story")
ax1.tick_params(axis="y", labelsize=8)

plt.tight_layout(pad=1.5)
plt.savefig("outputs/chart1_top_stories.png", dpi=150, bbox_inches="tight",
            facecolor=BG)
plt.close()
print("Saved outputs/chart1_top_stories.png")


# 3 — Chart 2: Stories per Category


cat_counts = df["category"].value_counts()

fig2, ax2 = plt.subplots(figsize=(8, 5))
fig2.patch.set_facecolor(BG)

bars2 = ax2.bar(cat_counts.index, cat_counts.values,
                color=PALETTE[:len(cat_counts)], width=0.55, zorder=3)

for bar in bars2:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.4,
             str(int(h)), ha="center", va="bottom", color=SUBTEXT, fontsize=9)

apply_dark_style(ax2, "Stories per Category", "Category", "Number of Stories")
ax2.set_ylim(0, cat_counts.max() + 4)

plt.tight_layout(pad=1.5)
plt.savefig("outputs/chart2_categories.png", dpi=150, bbox_inches="tight",
            facecolor=BG)
plt.close()
print("Saved outputs/chart2_categories.png")


# 4 — Chart 3: Score vs Comments


popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(8, 5))
fig3.patch.set_facecolor(BG)

ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="#45B7D1", alpha=0.75, s=55, zorder=3, label="Not Popular")
ax3.scatter(popular["score"],     popular["num_comments"],
            color="#FF6B6B", alpha=0.85, s=75, zorder=4, label="Popular",
            edgecolors="#FF9999", linewidths=0.6)

apply_dark_style(ax3, "Score vs Comments", "Score", "Number of Comments")
ax3.xaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)

legend = ax3.legend(facecolor=CARD, edgecolor=GRID, labelcolor=TEXT,
                    fontsize=9, framealpha=0.9)

plt.tight_layout(pad=1.5)
plt.savefig("outputs/chart3_scatter.png", dpi=150, bbox_inches="tight",
            facecolor=BG)
plt.close()
print("Saved outputs/chart3_scatter.png")


# Dashboard


fig, axes = plt.subplots(1, 3, figsize=(22, 7))
fig.patch.set_facecolor(BG)
fig.suptitle("TrendPulse Dashboard", color=TEXT, fontsize=18,
             fontweight="bold", y=1.01)

# --- Dashboard Chart 1 ---
ax = axes[0]
ax.set_facecolor(CARD)
bars = ax.barh(top10["short_title"], top10["score"], color=colors1,
               height=0.65, zorder=3)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 8, bar.get_y() + bar.get_height() / 2,
            f"{w:,}", va="center", ha="left", color=SUBTEXT, fontsize=7)
ax.invert_yaxis()
apply_dark_style(ax, "Top 10 Stories by Score", "Score", "")
ax.tick_params(axis="y", labelsize=7)

# --- Dashboard Chart 2 ---
ax = axes[1]
ax.set_facecolor(CARD)
bars2d = ax.bar(cat_counts.index, cat_counts.values,
                color=PALETTE[:len(cat_counts)], width=0.55, zorder=3)
for bar in bars2d:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3,
            str(int(h)), ha="center", va="bottom", color=SUBTEXT, fontsize=8)
apply_dark_style(ax, "Stories per Category", "Category", "Count")
ax.set_ylim(0, cat_counts.max() + 4)

# --- Dashboard Chart 3 ---
ax = axes[2]
ax.set_facecolor(CARD)
ax.scatter(not_popular["score"], not_popular["num_comments"],
           color="#45B7D1", alpha=0.75, s=45, zorder=3, label="Not Popular")
ax.scatter(popular["score"],     popular["num_comments"],
           color="#FF6B6B", alpha=0.85, s=65, zorder=4, label="Popular",
           edgecolors="#FF9999", linewidths=0.6)
apply_dark_style(ax, "Score vs Comments", "Score", "Comments")
ax.xaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
ax.legend(facecolor=CARD, edgecolor=GRID, labelcolor=TEXT, fontsize=8)

plt.tight_layout(pad=2.0)
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight",
            facecolor=BG)
plt.close()
print("Saved outputs/dashboard.png")