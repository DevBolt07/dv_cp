from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).parent
FIGURES_DIR = ROOT / "outputs" / "figures"


TEAM_NAME_MAP = {
    "Delhi Daredevils": "Delhi Capitals",
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
}

MODULE_DASHBOARDS = {
    "Module 1 - Data Preprocessing": {
        "subtitle": "Data quality checks, franchise normalization, and clean dataset preparation.",
        "focus": "Data readiness",
        "charts": [
            ("Data Quality: Raw vs Cleaned", "chart0a_data_quality.png"),
            ("Team Name Normalization", "chart0b_team_normalization.png"),
        ],
        "insights": [
            "Raw IPL records were validated for completeness, duplicate rows, valid run ranges, and valid over/ball ranges.",
            "Franchise rebrands were standardized so long-term team analysis is consistent.",
            "Clean, legal-delivery, batting-stat, and bowling-stat datasets were created for later modules.",
        ],
    },
    "Module 2 - Batting Analysis": {
        "subtitle": "Scoring trends, batting phases, player roles, and impact in wins vs losses.",
        "focus": "Batting performance",
        "charts": [
            ("Season-wise Average Score", "chart1_both_innings_trend.png"),
            ("Phase-wise Run Rate", "chart2_phase_runrate.png"),
            ("Batsman Phase Heatmap", "chart4_phase_heatmap.png"),
            ("Boundaries per Season", "chart5_boundaries_season.png"),
            ("Player Classification", "chart6_player_classification.png"),
            ("Strike Rate Acceleration", "chart7_sr_acceleration.png"),
            ("Performance in Wins vs Losses", "chart8_wins_vs_losses.png"),
        ],
        "insights": [
            "IPL scoring has risen over time, but batting-first and chasing trends remain close enough to compare strategically.",
            "Death overs produce the highest scoring acceleration.",
            "Player role classification separates anchors, support players, aggressive scorers, and match winners.",
        ],
    },
    "Module 3 - Bowling Analysis": {
        "subtitle": "Bowler matchups, phase economy, dismissals, specialist roles, and match impact.",
        "focus": "Bowling performance",
        "charts": [
            ("Bowler vs Batsman Heatmap", "chart8_bowler_batsman_heatmap.png"),
            ("Economy Rate by Phase", "chart9_economy_boxplot.png"),
            ("Dismissal Types", "chart10_dismissals.png"),
            ("Dot Ball vs Boundary Rate", "chart11_dot_boundary_phase.png"),
            ("Top Bowlers by Wickets", "chart12_top_bowlers.png"),
            ("Bowler Role Classification", "chart13_bowler_scatter.png"),
            ("Death Overs Specialists", "chart14_death_specialists.png"),
            ("Powerplay Specialists", "chart15_powerplay_specialists.png"),
            ("Wickets in Winning Matches", "chart16_wickets_winning.png"),
        ],
        "insights": [
            "Elite bowlers combine wicket-taking with economy control.",
            "Bowling value changes by phase: powerplay control and death-over control reward different skill profiles.",
            "Impact bowlers are highlighted by wickets that occur in winning matches, not just total wickets.",
        ],
    },
    "Module 4 - Match & Team Patterns": {
        "subtitle": "Toss decisions, chasing trends, venue effects, match momentum, and win margins.",
        "focus": "Match strategy",
        "charts": [
            ("Toss Decision Analysis", "chart14_toss_decision.png"),
            ("Chasing vs Defending by Season", "chart15_chasing_trend.png"),
            ("Powerplay Score vs Outcome", "chart16_powerplay_outcome.png"),
            ("Team Win Percentage", "chart17_team_win_pct.png"),
            ("Season-wise Match Score Trend", "chart18_season_scores.png"),
            ("Venue Impact", "chart19_venue_impact.png"),
            ("Match Momentum", "chart20_momentum.png"),
            ("Win Margin Distribution", "chart21_win_margins.png"),
        ],
        "insights": [
            "Toss decisions are useful only when linked to actual win percentage.",
            "Powerplay scoring while batting first has a visible relationship with match outcome.",
            "Venue patterns show that some grounds favor defending while others favor chasing.",
        ],
    },
}


def phase_from_over(over: int) -> str:
    if over <= 6:
        return "Powerplay"
    if over <= 15:
        return "Middle"
    return "Death"


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    deliveries = pd.read_csv(ROOT / "deliveries.csv")
    matches = pd.read_csv(ROOT / "matches.csv")

    team_columns = ["batting_team", "bowling_team"]
    for column in team_columns:
        deliveries[column] = deliveries[column].replace(TEAM_NAME_MAP)

    match_team_columns = ["team1", "team2", "toss_winner", "winner"]
    for column in match_team_columns:
        matches[column] = matches[column].replace(TEAM_NAME_MAP)

    deliveries["phase"] = deliveries["over"].apply(phase_from_over)
    legal = deliveries[(deliveries["wide_runs"] == 0) & (deliveries["noball_runs"] == 0)].copy()

    return deliveries, legal.merge(matches[["id", "season"]], left_on="match_id", right_on="id", how="left"), matches


@st.cache_data
def build_stats(deliveries: pd.DataFrame, legal: pd.DataFrame, matches: pd.DataFrame) -> dict:
    deliveries = deliveries.merge(matches[["id", "season"]], left_on="match_id", right_on="id", how="left")

    season_scores = deliveries.groupby(["match_id", "season", "inning"])["total_runs"].sum().reset_index()
    avg_inn1 = season_scores[season_scores["inning"] == 1].groupby("season")["total_runs"].mean().round(1)
    avg_inn2 = season_scores[season_scores["inning"] == 2].groupby("season")["total_runs"].mean().round(1)

    phase_order = ["Powerplay", "Middle", "Death"]
    phase_total_runs = deliveries.groupby("phase")["total_runs"].sum()
    phase_legal_balls = legal.groupby("phase")["ball"].count()
    phase_rr = {
        phase: round(phase_total_runs[phase] / phase_legal_balls[phase] * 6, 2)
        for phase in phase_order
    }

    legal_batting = deliveries[(deliveries["wide_runs"] == 0) & (deliveries["noball_runs"] == 0)]
    dismissals = deliveries.dropna(subset=["player_dismissed"])
    player_stats = deliveries.groupby("batsman").agg(total_runs=("batsman_runs", "sum")).reset_index()
    balls_faced = legal_batting.groupby("batsman")["ball"].count().rename("total_balls")
    innings = deliveries.groupby("batsman")["match_id"].nunique().rename("innings")
    dismissal_counts = dismissals.groupby("player_dismissed")["match_id"].count().rename("dismissals")
    player_stats = player_stats.merge(balls_faced, on="batsman", how="left")
    player_stats = player_stats.merge(innings, on="batsman", how="left")
    player_stats = player_stats.merge(dismissal_counts, left_on="batsman", right_index=True, how="left")
    player_stats["dismissals"] = player_stats["dismissals"].fillna(0)
    player_stats["strike_rate"] = (player_stats["total_runs"] / player_stats["total_balls"] * 100).round(1)
    player_stats["average"] = (player_stats["total_runs"] / player_stats["dismissals"].replace(0, pd.NA)).round(1)
    top10 = player_stats.nlargest(10, "total_runs").sort_values("total_runs")

    legal_bowling = deliveries[(deliveries["wide_runs"] == 0) & (deliveries["noball_runs"] == 0)]
    wicket_kinds = deliveries[
        deliveries["dismissal_kind"].notna()
        & ~deliveries["dismissal_kind"].isin(["run out", "retired hurt", "obstructing the field"])
    ]
    bowler_stats = deliveries.groupby("bowler").agg(runs_conceded=("total_runs", "sum")).reset_index()
    bowler_stats = bowler_stats.merge(
        legal_bowling.groupby("bowler")["ball"].count().rename("balls"),
        on="bowler",
        how="left",
    )
    bowler_stats = bowler_stats.merge(
        legal_bowling.groupby("bowler")["match_id"].nunique().rename("matches"),
        on="bowler",
        how="left",
    )
    bowler_stats = bowler_stats.merge(
        wicket_kinds.groupby("bowler")["player_dismissed"].count().rename("wickets"),
        on="bowler",
        how="left",
    )
    bowler_stats["wickets"] = bowler_stats["wickets"].fillna(0)
    bowler_stats["economy"] = (bowler_stats["runs_conceded"] / bowler_stats["balls"] * 6).round(2)

    top60 = bowler_stats.nlargest(60, "wickets").copy()
    eco_median = top60["economy"].median()
    wkt_median = top60["wickets"].median()
    top60["role"] = top60.apply(
        lambda row: "Elite"
        if row["economy"] <= eco_median and row["wickets"] >= wkt_median
        else "Aggressive"
        if row["economy"] > eco_median and row["wickets"] >= wkt_median
        else "Defensive"
        if row["economy"] <= eco_median
        else "Average",
        axis=1,
    )

    bat_first_lookup = deliveries[deliveries["inning"] == 1].groupby("match_id")["batting_team"].first().reset_index()
    bat_first_lookup.columns = ["id", "bat_first_team"]
    matches_ext = matches.merge(bat_first_lookup, on="id", how="left")
    matches_ext["bat_first_won"] = (matches_ext["bat_first_team"] == matches_ext["winner"]).astype(int)

    pp = deliveries[(deliveries["inning"] == 1) & (deliveries["phase"] == "Powerplay")]
    pp_scores = pp.groupby("match_id")["total_runs"].sum().reset_index()
    pp_scores.columns = ["id", "pp_runs"]
    pp_merged = pp_scores.merge(matches_ext[["id", "bat_first_won"]], on="id")
    pp_merged["pp_bin"] = pd.cut(
        pp_merged["pp_runs"],
        bins=[0, 30, 40, 50, 60, 120],
        labels=["<30", "30-40", "40-50", "50-60", ">60"],
    )
    win_rate = pp_merged.groupby("pp_bin", observed=True)["bat_first_won"].mean().mul(100).round(1)

    venue_stats = matches_ext.groupby("venue").agg(
        n_matches=("id", "count"),
        bat_wins=("bat_first_won", "sum"),
    ).reset_index()
    venue_stats["bat_first_pct"] = (venue_stats["bat_wins"] / venue_stats["n_matches"] * 100).round(1)
    venue_stats = venue_stats[venue_stats["n_matches"] >= 15].sort_values("bat_first_pct")
    venue_stats["venue_short"] = venue_stats["venue"].replace(
        {
            "Rajiv Gandhi International Stadium, Uppal": "RGIS Hyderabad",
            "Punjab Cricket Association Stadium, Mohali": "PCA Mohali",
            "MA Chidambaram Stadium, Chepauk": "Chepauk Chennai",
            "Maharashtra Cricket Association Stadium": "MCA Pune",
            "Dr DY Patil Sports Academy": "DY Patil Mumbai",
            "Subrata Roy Sahara Stadium": "Sahara Pune",
        }
    )

    return {
        "avg_inn1": avg_inn1,
        "avg_inn2": avg_inn2,
        "phase_order": phase_order,
        "phase_rr": phase_rr,
        "top10": top10,
        "top60": top60,
        "eco_median": eco_median,
        "wkt_median": wkt_median,
        "win_rate": win_rate,
        "venue_stats": venue_stats,
        "player_stats": player_stats,
        "bowler_stats": bowler_stats,
    }


def build_dashboard(stats: dict) -> plt.Figure:
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle("IPL Data Analysis Dashboard | 2008-2019", fontsize=17, fontweight="bold", y=1.01)

    avg_inn1 = stats["avg_inn1"]
    avg_inn2 = stats["avg_inn2"]
    phase_order = stats["phase_order"]
    phase_rr = stats["phase_rr"]
    top10 = stats["top10"]
    top60 = stats["top60"]
    win_rate = stats["win_rate"]
    venue_stats = stats["venue_stats"]

    ax1 = axes[0, 0]
    ax1.plot(avg_inn1.index, avg_inn1.values, color="steelblue", linewidth=2, marker="o", label="Batting first")
    ax1.plot(avg_inn2.index, avg_inn2.values, color="red", linewidth=2, marker="s", linestyle="--", label="Chasing")
    ax1.fill_between(avg_inn1.index, avg_inn1.values, avg_inn2.values, alpha=0.08, color="steelblue")
    ax1.set_title("IPL Scores Rising - Defending Gap Stays Constant", fontsize=11, pad=8)
    ax1.set_xlabel("Season")
    ax1.set_ylabel("Avg Runs")
    ax1.tick_params(axis="x", rotation=45, labelsize=8)
    ax1.legend(fontsize=8)
    ax1.grid(True, linestyle="--", alpha=0.3)

    ax2 = axes[0, 1]
    p_vals = [phase_rr[phase] for phase in phase_order]
    bars = ax2.bar(phase_order, p_vals, color=["steelblue", "orange", "red"], width=0.5, edgecolor="white")
    for bar, value in zip(bars, p_vals):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, str(value), ha="center", fontsize=10, fontweight="bold")
    ax2.set_title("Death Overs Most Explosive", fontsize=11, pad=8)
    ax2.set_ylabel("Runs per Over")
    ax2.set_ylim(0, 12)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)

    ax3 = axes[0, 2]
    norm = plt.Normalize(top10["strike_rate"].min(), top10["strike_rate"].max())
    colors = plt.cm.Blues(norm(top10["strike_rate"].values))
    bars3 = ax3.barh(top10["batsman"], top10["total_runs"], color=colors)
    for bar, (_, row) in zip(bars3, top10.iterrows()):
        ax3.text(bar.get_width() + 30, bar.get_y() + bar.get_height() / 2, f"SR: {row['strike_rate']}", va="center", fontsize=7.5)
    ax3.set_title("Top Batsmen - Darker Means Higher Strike Rate", fontsize=11, pad=8)
    ax3.set_xlabel("Total Runs")
    ax3.set_xlim(0, top10["total_runs"].max() + 600)
    ax3.tick_params(labelsize=8)
    ax3.grid(axis="x", linestyle="--", alpha=0.3)

    ax4 = axes[1, 0]
    role_colors = {"Elite": "green", "Aggressive": "red", "Defensive": "steelblue", "Average": "gray"}
    for role, group in top60.groupby("role"):
        ax4.scatter(group["economy"], group["wickets"], c=role_colors[role], label=role, alpha=0.7, s=50)
    for name in ["SL Malinga", "SP Narine", "R Ashwin", "Harbhajan Singh"]:
        row = top60[top60["bowler"] == name]
        if len(row):
            ax4.annotate(name, (row.iloc[0]["economy"], row.iloc[0]["wickets"]), textcoords="offset points", xytext=(4, 2), fontsize=7)
    ax4.axvline(stats["eco_median"], color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax4.axhline(stats["wkt_median"], color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax4.set_title("Elite Bowlers: High Wickets + Low Economy", fontsize=11, pad=8)
    ax4.set_xlabel("Economy Rate")
    ax4.set_ylabel("Total Wickets")
    ax4.legend(fontsize=7, title="Role", title_fontsize=7)
    ax4.grid(True, linestyle="--", alpha=0.3)

    ax5 = axes[1, 1]
    pp_colors = ["#E24B4A", "#F09595", "#FAC775", "#5DCAA5", "#0F6E56"]
    bars5 = ax5.bar(win_rate.index.astype(str), win_rate.values, color=pp_colors, width=0.5, edgecolor="white")
    for bar, value in zip(bars5, win_rate.values):
        ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{value}%", ha="center", fontsize=9, fontweight="bold")
    ax5.axhline(50, color="gray", linestyle="--", linewidth=1, label="50% baseline")
    ax5.set_title("Powerplay Score vs Match Win %", fontsize=11, pad=8)
    ax5.set_xlabel("Powerplay Runs")
    ax5.set_ylabel("Batting First Win %")
    ax5.set_ylim(0, 80)
    ax5.legend(fontsize=8)
    ax5.grid(axis="y", linestyle="--", alpha=0.3)

    ax6 = axes[1, 2]
    v_colors = ["#5DCAA5" if value >= 50 else "#F09595" for value in venue_stats["bat_first_pct"]]
    bars6 = ax6.barh(venue_stats["venue_short"], venue_stats["bat_first_pct"], color=v_colors, edgecolor="white")
    for bar, (_, row) in zip(bars6, venue_stats.iterrows()):
        ax6.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f"{row['bat_first_pct']}%", va="center", fontsize=8)
    ax6.axvline(50, color="gray", linestyle="--", linewidth=1)
    ax6.set_title("Venue Impact on Batting First", fontsize=11, pad=8)
    ax6.set_xlabel("Batting First Win %")
    ax6.set_xlim(0, 80)
    ax6.tick_params(labelsize=8)
    ax6.grid(axis="x", linestyle="--", alpha=0.3)

    fig.tight_layout()
    return fig


def render_metric_strip(deliveries_df: pd.DataFrame, matches_df: pd.DataFrame, stats_data: dict) -> None:
    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Matches", f"{matches_df['id'].nunique():,}")
    metric_2.metric("Deliveries", f"{deliveries_df.shape[0]:,}")
    metric_3.metric("Seasons", f"{matches_df['season'].nunique():,}")
    metric_4.metric("Players", f"{stats_data['player_stats']['batsman'].nunique():,}")


def render_image_grid(charts: list[tuple[str, str]]) -> None:
    for index in range(0, len(charts), 2):
        columns = st.columns(2)
        for column, (title, filename) in zip(columns, charts[index : index + 2]):
            image_path = FIGURES_DIR / filename
            with column:
                st.subheader(title)
                if image_path.exists():
                    st.image(str(image_path), use_container_width=True)
                else:
                    st.warning(f"Missing figure: {filename}")


def render_insight_table(module_name: str, insights: list[str]) -> None:
    st.dataframe(
        pd.DataFrame(
            {
                "No.": range(1, len(insights) + 1),
                "Module": [module_name] * len(insights),
                "Insight": insights,
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_module_section(module_name: str) -> None:
    dashboard = MODULE_DASHBOARDS[module_name]
    st.header(module_name)
    st.caption(dashboard["subtitle"])

    stat_1, stat_2 = st.columns(2)
    stat_1.metric("Charts", len(dashboard["charts"]))
    stat_2.metric("Focus", dashboard["focus"])

    st.subheader("Insight Table")
    render_insight_table(module_name, dashboard["insights"])

    st.subheader("Graphs")
    render_image_grid(dashboard["charts"])


def render_final_dashboard(deliveries_df: pd.DataFrame, matches_df: pd.DataFrame, stats_data: dict) -> None:
    st.title("Final Dashboard - IPL Performance Analytics")
    st.caption("Executive summary of the strongest findings from all four analysis modules.")

    render_metric_strip(deliveries_df, matches_df, stats_data)
    st.pyplot(build_dashboard(stats_data), use_container_width=True)

    st.subheader("Key Insights")
    st.markdown(
        """
- IPL scoring increased across seasons, while the gap between batting first and chasing stayed fairly consistent.
- Death overs are the highest-scoring phase, with the strongest run-rate acceleration.
- Virat Kohli leads the batting chart for the 2008-2019 dataset.
- Elite bowlers combine high wickets with low economy, led by names such as Malinga, Narine, and Ashwin.
- Teams crossing 60 runs in the powerplay while batting first show a stronger win probability.
- Venue matters: some grounds favor defending, while others favor chasing.
"""
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Top 10 Batsmen")
        st.dataframe(
            stats_data["top10"].sort_values("total_runs", ascending=False)[
                ["batsman", "total_runs", "total_balls", "strike_rate", "average"]
            ],
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.subheader("Top Bowlers by Wickets")
        st.dataframe(
            stats_data["bowler_stats"].nlargest(10, "wickets")[
                ["bowler", "wickets", "economy", "matches", "balls"]
            ],
            use_container_width=True,
            hide_index=True,
        )


def render_project_summary() -> None:
    rows = []
    for module_name, dashboard in MODULE_DASHBOARDS.items():
        rows.append(
            {
                "Module": module_name,
                "Focus": dashboard["focus"],
                "Graphs": len(dashboard["charts"]),
                "Output": dashboard["subtitle"],
            }
        )

    st.subheader("Project Module Summary")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def render_complete_dashboard(deliveries_df: pd.DataFrame, matches_df: pd.DataFrame, stats_data: dict) -> None:
    st.title("IPL Performance Analytics Dashboard")
    st.caption("A complete data visualization project covering preprocessing, batting, bowling, match patterns, and final insights.")

    render_metric_strip(deliveries_df, matches_df, stats_data)

    st.header("Executive Dashboard")
    st.pyplot(build_dashboard(stats_data), use_container_width=True)

    render_project_summary()

    st.header("Final Insight Tables")
    left, right = st.columns(2)
    with left:
        st.subheader("Top 10 Batsmen")
        st.dataframe(
            stats_data["top10"].sort_values("total_runs", ascending=False)[
                ["batsman", "total_runs", "total_balls", "strike_rate", "average"]
            ],
            use_container_width=True,
            hide_index=True,
        )
    with right:
        st.subheader("Top Bowlers by Wickets")
        st.dataframe(
            stats_data["bowler_stats"].nlargest(10, "wickets")[
                ["bowler", "wickets", "economy", "matches", "balls"]
            ],
            use_container_width=True,
            hide_index=True,
        )

    for module_name in MODULE_DASHBOARDS:
        st.divider()
        render_module_section(module_name)


st.set_page_config(page_title="IPL Performance Analytics", layout="wide")

deliveries_df, legal_df, matches_df = load_data()
stats_data = build_stats(deliveries_df, legal_df, matches_df)

render_complete_dashboard(deliveries_df, matches_df, stats_data)
