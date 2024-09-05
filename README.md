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

## Methodology
- 🌐 **Web Scraping**:
  -  Libraries used: `pandas`,`bs4`,`requests`
  -  Data was extracted from *basketball.realgm.com* using Python's web scraping libraries. This allowed us to gather detailed statistics for PBA players participating in the 2023-2024 Philippine Cup.

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def table_scraper(url, class_name):
    page = requests.get(url=url).text
    soup = BeautifulSoup(page, 'html.parser')
    header_cols = soup.find(class_=class_name).find('thead').find_all('th')
    header_cols_cleaned = [header_col.text.strip() for header_col in header_cols]
    row_data = soup.find(class_=class_name).find('tbody').find_all('tr')
    df = pd.DataFrame(columns=header_cols_cleaned)

    for index, row in enumerate(row_data):
        content = [data.text for data in row.find_all('td')]
        length = len(df)
        df.loc[length] = content

    for row in df.columns:
        try:
            # Attempt to convert the column to float type
            df[row] = df[row].astype('float')
            print(f"Successfully converted {row} to float.")
        except ValueError:
            # Skip conversion if an error occurs
            print(f"Could not convert {row} to float, skipping.")
            pass

    return df
```

The above Python code snippet, sourced from `notebooks/Basketball_realgm_PBA_webscraper.ipynb` within this repository, extracts a DataFrame from basketball.realgm.com. It fetches the page content, parses it to locate table headers and rows, and attempts to convert the data into a float format where possible.

<br />

- 🌐 **Filtering**:
  -  Libraries used: `pandas`, `streamlit`
  - The pandas library was utilized to load the web-scraped dataframes and apply filters based on user input. The filtering interface was constructed using Streamlit widgets, with session state logic connecting widget selections to pandas operations
  - This code snippet from the Stat Scatter page illustrates how to implement the page logic using Streamlit's `session state` and `pandas`

```python
import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv(r'datasets\compiled_stats.csv')

col1, col2 = st.columns(2)


with col1:
    st.selectbox('Y-axis', 
                   options=relevant_filters,
                   on_change=store_value,
                   key='_y_axis')
    
with col2:
    st.selectbox('X-axis', 
                   options=relevant_filters,
                   on_change=store_value,
                   key='_x_axis')

filtered_df = df[   (df['GP'] >= st.session_state._games_played)
                ]

chart = alt.Chart(filtered_df).mark_circle().encode(
    alt.X(st.session_state._x_axis).scale(zero=False),
    alt.Y(st.session_state._y_axis).scale(zero=False, padding=1),
    color='Team',
    size=st.session_state._y_axis,
    description='Player'
)


st.altair_chart(chart)
```
