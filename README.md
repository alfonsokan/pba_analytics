# PBA Analytics App
This Streamlit app provides comprehensive analytics for the Philippine Basketball Association (PBA), covering a wide range of statistics. The data was meticulously web-scraped from basketball.realgm.com and processed using the Pandas library to enable dynamic filtering and analysis.

## Installation
- Use the package manager pip to install the necessary libraries to run the application.
```bash
pip install -r requirements.txt
```
- Ensure the app is located in your working directory, then start it by running the following command:
```python
streamlit run Home.py
```
## Features Summary
- 📄 **Team Overview:** Discover the top players on each team who led in various statistical categories.
- 🔍 **Find-a-Player:** Search for players based on specific statistical criteria, such as those averaging between 10-15 PPG and 5-10 RPG.
- ⚔️ **Head-to-Head Comparison:** Compare the stats of two players side by side with ease.
- 📊 **Stat Scatter:** Visualize two stats on a scatter plot for deeper insights. For example, identify the most efficient PBA scorers by plotting Points Per Game (PPG) against Field Goal Percentage (FG%).
- 📈 **League Leaders:** Explore which players led the league in key statistical categories.

## Future Developments
- 📅 **Include Stats from Other Seasons**: Expand the app to include statistics from previous PBA seasons, allowing users to explore and compare player performance over time.
- 🛠️ **Customizable Visualizations**: Allow users to create and save custom visualizations, making it easier to track specific stats or trends over the course of a season.
- 📊 **Team Analytics**: Expand the analysis to team-level statistics, offering insights into team performance, strengths, and weaknesses throughout the season.

## How the App was Made
- 🌐 Web Scraping: Data was extracted from basketball.realgm.com using Python's web scraping libraries. This allowed us to gather detailed statistics for PBA players participating in the 2023-2024 Philippine Cup.
- 🐼 Pandas: The scraped data was cleaned, processed, and analyzed using the Pandas library. Pandas enabled us to manipulate the data efficiently, creating different statistical views such as Averages, Totals, Per 36 Minutes, and Advanced stats.
- 📊 Streamlit Data Elements: Streamlit was used to create an interactive and user-friendly interface. Key features like the Find-a-Player, Head-to-Head Comparison, and Stat Scatter tools were built using Streamlit's data elements, making the app both dynamic and easy to navigate.
