# IPL Performance Analytics

This repository contains an IPL 2008--2019 ball-by-ball analytics project integrating data preprocessing, visualization, and hypothesis testing.

## Repository Structure

- `Module1_Preprocessing.ipynb`  
  Data cleaning, franchise normalization, feature engineering, and export of analysis-ready datasets.

- `Module2_Batting.ipynb`  
  Batting-focused visual and statistical analysis.

- `Module3_Bowling.ipynb`  
  Bowling-focused visual and statistical analysis.

- `main.tex`  
  Main IEEE conference-format research paper source.

- `ipl_performance_paper.tex`  
  Working paper source file.

## Data Files

- `matches.csv`
- `deliveries.csv`
- `matches_clean.csv`
- `deliveries_clean.csv`
- `legal_deliveries.csv`
- `player_stats.csv`
- `bowler_stats.csv`

## Figures Included in the Paper

- `fig01_data_quality.png`
- `fig02_team_normalization.png`
- `fig03_season_scoring_trend.png`
- `fig04_phase_run_rate.png`
- `fig07_batting_phase_heatmap.png`
- `fig08_matchup_heatmap.png`
- `fig10_phase_economy_boxplot.png`
- `fig12_bowler_match_impact.png`

## Reproducibility

Run the notebooks in sequence:

1. `Module1_Preprocessing.ipynb`
2. `Module2_Batting.ipynb`
3. `Module3_Bowling.ipynb`

The repository `.gitignore` excludes generated LaTeX auxiliary files and notebook checkpoint artifacts.
