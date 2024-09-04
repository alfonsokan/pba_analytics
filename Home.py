import streamlit as st

# Home Page
st.title("🏀 PBA Analytics App")

st.header("Overview")
st.markdown("""
The data powering this app was web scraped from [basketball.realgm.com](https://basketball.realgm.com/), focusing on Philippine Basketball Association (PBA) teams that participated in the **2023-2024 Philippine Cup**. The available stat types include **Averages, Totals, Per 36 Minutes, Advanced,** and **Miscellaneous.**

Unlike the official PBA website, which primarily offers fans access to general stats like **Averages** and **Totals**, this app provides a more comprehensive and in-depth analysis. With additional stat types such as **Per 36 Minutes** and **Advanced** metrics, the app delivers a richer, more detailed view of player performances.
""")

# How the App Was Made Section
st.header("How This App Was Made")
st.markdown("""
This app was developed using a combination of web scraping, data processing, and visualization techniques:

- **🌐 Web Scraping:** Data was extracted from [basketball.realgm.com](https://basketball.realgm.com/) using Python's web scraping libraries. This allowed us to gather detailed statistics for PBA players participating in the 2023-2024 Philippine Cup.
  
- **🐼 Pandas:** The scraped data was cleaned, processed, and analyzed using the Pandas library. Pandas enabled us to manipulate the data efficiently, creating different statistical views such as Averages, Totals, Per 36 Minutes, and Advanced stats.
  
- **📊 Streamlit Data Elements:** Streamlit was used to create an interactive and user-friendly interface. Key features like the **Find-a-Player**, **Head-to-Head Comparison**, and **Stat Scatter** tools were built using Streamlit's data elements, making the app both dynamic and easy to navigate.
""")


st.header("What Sets This App Apart?")
st.markdown("""
In addition to standard player stats (available in the **Team Overview** & **League Leaders** sections), the app offers the following unique features tailored for PBA fans:
""")

st.markdown("""
- **🔍 Find-a-Player:** Search for players who meet a specific statistical criteria, i.e. look for players averaging between 10-15 PPG and 5-10 RPG.
            
- **⚔️ Head-to-Head Comparison:** Easily compare the stats of two players side by side.
            

- **📊 Stat Scatter:** A powerful tool that allows users to visualize two stats on a scatter plot, offering deeper insights. For instance, you can identify the most efficient PBA scorers by plotting **Points Per Game (PPG)** against **Field Goal Percentage (FG%)**.
""")
# Recommendations Section
st.header("Future Recommendations")
st.markdown("""
- **📅 Include Stats from Other Seasons:** Expand the app to include statistics from previous PBA seasons, allowing users to explore and compare player performance over time.
            
- **🛠️ Customizable Visualizations:** Allow users to create and save custom visualizations, making it easier to track specific stats or trends over the course of a season.
            
- **📊 Team Analytics:** Expand the analysis to team-level statistics, offering insights into team performance, strengths, and weaknesses throughout the season.
""")
