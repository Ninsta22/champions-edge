# League of Legends Champion Recommender

![Created by Team Pangolin](https://github.com/Ninsta22/champions-edge/assets/142264378/52981049-3b54-49d2-8625-31232628e504)

This README outlines our methodology for developing a predictive model designed to forecast which team is likely to win in League of Legends, a leading multiplayer online battle arena (MOBA) game with over 180 million active players.

🎯 **Primary Goal**  
The tool aims to provide players with a strategic advantage by recommending optimal team compositions, thus enhancing win probabilities before the match begins.

👥 **Game Overview**  
League of Legends pits two teams of five players against each other, where each player selects from over 160 unique champions. The game's complexity and the vast array of possible team compositions create a substantial challenge that our ML tool seeks to address.

## What is the Goal for This Project?
The main objective behind this project is to provide players with a competitive edge through a tool that offers the ability to strategically plan team compositions with the highest chance of winning. By leveraging AI, we aim to enhance gameplay strategy and overall success for a team in League of Legends matches.

## Dataset Overview

- Our dataset is aggregated and released by Tim Sevenhuysen of OraclesElixir.com.
- It spans from 2017 to 2024, containing records of 65,807 unique professional matches across major leagues like LCS, LEC, LCK, LPL, PCS, and CBLoL.
- The dataset includes comprehensive match-level statistics such as team kills, team deaths, total damage to champions, and total gold.
- Detailed champion selection data is available for all 166 champions as of the start of 2024.
- We are utilizing this dataset due to its extensive coverage, structured and accessible format, and the regular updates it receives.
- These features make it ideal for developing a predictive model that can accurately forecast win probabilities and recommend optimal team compositions.

## Preprocessing
During preprocessing, we concentrated on three principal components:
1. **Historical In-Game Contributions of the Champions**: Analyzing the past performance and impact of champions within games.
2. **Career Performance of Individual Players**: Incorporating statistics that reflect the long-term performance of players.
3. **Overall Historical Performance of Teams**: Evaluating team success and strategy over time.

Our findings indicate that while historical data on champions offers some predictive utility, the most significant predictors of game outcomes are the career statistics of players and teams. These elements substantially enhance the predictive accuracy of our models.

## Model Description
We employed a variety of modeling techniques to develop this prediction tool:
- Logistic Regression (a baseline model)
- Tree-Based Ensemble Methods (Random Forest, Ensemble-based models)
- Neural Networks

Each method was chosen for its unique ability to leverage insights from tabular data.

## We have a website!

Our website, [ChampionEdge](https://championedge.streamlit.app/), enhances gameplay with two innovative features:

🏆 **Win Prediction:**
- Input the champions in your team (5) and your opponent's team (5).
- The site uses a Random Forest model to predict the likely winner and the win probability percentage.

🛡️ **Champion Recommendation**
- Enter the four champions of your team and the five champions of the opposing team.
- The system suggests a list of five optimal champions to round out your team composition, maximizing your chances of victory.

## Team Pangolin

- Kian Bagherlee
- Poojitha Balamurugan
- Jaxon Yue
- Yabei Zeng

We're from Duke - MIDS Program, Class of 2025.





