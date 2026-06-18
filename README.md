# IPL Performance Analytics

An end-to-end data visualization project analyzing IPL ball-by-ball data from 2008 to 2019.

The project combines data preprocessing, batting analysis, bowling analysis, match-pattern analysis, and a Streamlit dashboard that presents all graphs and insights in one deployable web app.

## Live Dashboard

This project is designed to be deployed with Streamlit Cloud.

Main app file:

```text
streamlit_app.py
```

## Project Highlights

- Cleaned and standardized IPL match and delivery datasets
- Normalized franchise name changes across seasons
- Built batting and bowling performance metrics
- Created phase-wise analysis for powerplay, middle overs, and death overs
- Compared batting-first and chasing patterns
- Studied toss decisions, venue impact, powerplay outcomes, and win margins
- Converted the notebook analysis into a single Streamlit dashboard

## Dashboard Sections

| Section | Focus | Output |
|---|---|---|
| Final Dashboard | Executive summary | Six-panel overview plus top player tables |
| Module 1 - Data Preprocessing | Data readiness | Data quality and franchise normalization visuals |
| Module 2 - Batting Analysis | Batting performance | Scoring trends, player roles, acceleration, and impact charts |
| Module 3 - Bowling Analysis | Bowling performance | Matchups, economy, dismissal types, specialist roles, and impact charts |
| Module 4 - Match & Team Patterns | Match strategy | Toss, chasing, powerplay, venue, momentum, and margin visuals |

## Repository Structure

```text
.
|-- streamlit_app.py
|-- requirements.txt
|-- matches.csv
|-- deliveries.csv
|-- Module1_Preprocessing.ipynb
|-- Module2_Batting.ipynb
|-- Module3_Bowling.ipynb
|-- Module4_Patterns.ipynb
|-- Module5_Dashboard.ipynb
|-- data/
|   |-- clean/
|   |-- derived/
|-- outputs/
|   |-- figures/
|-- research_paper/
```

## Modules

### Module 1 - Data Preprocessing

Cleans the raw IPL datasets, removes invalid records, standardizes team names, adds season and match-phase fields, and creates analysis-ready datasets.

### Module 2 - Batting Analysis

Explores batting trends through season scoring patterns, phase-wise run rates, top run scorers, strike-rate heatmaps, boundary trends, player classification, and performance in wins vs losses.

### Module 3 - Bowling Analysis

Analyzes bowling performance through bowler-batsman matchups, economy by phase, dismissal types, pressure vs boundary risk, top wicket-takers, specialist roles, and wickets in winning matches.

### Module 4 - Match & Team Patterns

Studies match strategy using toss decisions, chasing trends, powerplay score impact, team win percentages, venue effects, match momentum, and win margin distribution.

### Module 5 - Dashboard

Combines the strongest findings into a final dashboard. The Streamlit app expands this into a single web dashboard containing all module graphs and insight tables.

## Data Files

Raw files:

- `matches.csv`
- `deliveries.csv`

Generated clean and derived files:

- `data/clean/matches_clean.csv`
- `data/clean/deliveries_clean.csv`
- `data/clean/legal_deliveries.csv`
- `data/derived/player_stats.csv`
- `data/derived/bowler_stats.csv`

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run streamlit_app.py
```

## Deploy on Streamlit Cloud

1. Push the repository to GitHub.
2. Go to Streamlit Cloud.
3. Create a new app from the GitHub repository.
4. Set the main file path to:

```text
streamlit_app.py
```

5. Deploy the app.

Make sure `outputs/figures/*.png` is included in GitHub because the dashboard displays those graph images.

## Tech Stack

- Python
- Pandas
- Matplotlib
- Streamlit
- Jupyter Notebook

## Key Insights

- IPL scoring increased across seasons from 2008 to 2019.
- Death overs are the most explosive scoring phase.
- Powerplay scoring has a clear relationship with match outcome.
- Elite bowlers combine high wicket-taking ability with low economy.
- Venue conditions influence whether defending or chasing is more favorable.
- Toss decisions are more meaningful when compared with actual win percentage.
