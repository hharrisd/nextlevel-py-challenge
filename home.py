import asyncio

import pandas as pd
import streamlit as st
from pandas import DataFrame
import matplotlib.pyplot as plt

from utilities import check_files_exists, create_files, CSV_FILES

st.title("The Lord of the Rings Insight")
st.write("Some information from characters of the LOTR")


def create_csv_files() -> None:
    asyncio.run(create_files())


@st.cache_data
def load_data() -> tuple[DataFrame, DataFrame, DataFrame]:
    characters_df = pd.read_csv('data/characters.csv')
    quotes_df = pd.read_csv('data/quotes.csv')
    movies_df = pd.read_csv('data/movies.csv')

    return characters_df, quotes_df, movies_df


if check_files_exists(CSV_FILES) is False:
    csv_files_state = st.warning("The CSV files are missing!")
    create_csv_files()
    csv_files_state.success("The CSV files are loaded!!")

data_load_state = st.text('Loading data...')
characters_data, quotes_data, movies_data = load_data()
data_load_state.text("Data loaded!")

if st.toggle("Display raw data"):
    if st.checkbox('Show Characters raw data'):
        st.subheader("Character's raw data")
        st.write(characters_data)

    if st.checkbox('Show Quotes raw data'):
        st.subheader("Quote's raw data")
        st.write(quotes_data)

    if st.checkbox('Show Movies raw data'):
        st.subheader("Movie's raw data")
        st.write(movies_data)

st.divider()
st.subheader("Totals")
st.write(f"Total of characters: {len(characters_data.index)}")

filtered_race = characters_data[characters_data['race'] != "No Race"]
filtered_realm = characters_data[characters_data['realm'] != "No Realm"]

total_race = filtered_race['race'].value_counts()
total_realm = filtered_realm['realm'].value_counts()

# Two columns for charts and datasets
col1, col2 = st.columns([0.7, 0.3])

# FIrst row
col1.subheader("Races")
col1.write(f"Total of races: {len(total_race.index)}")
col1.line_chart(total_race)

col2.subheader("Races Data")
col2.write(total_race)

# Second row
col1.subheader("Realms")
col1.write(f"Total of realms: {len(total_realm.index)}")
col1.line_chart(total_realm)

col2.subheader("Realm Data")
col2.write(total_realm)

st.divider()

st.subheader("Main races in LOTR")
race_counts = total_race.nlargest(20)
st.bar_chart(race_counts)

st.divider()

st.subheader("Main realms in LOTR")

# Group by 'race' and count occurrences
realm_counts = total_realm.nlargest(10)
#
# # Create a pie chart using matplotlib
fig, ax = plt.subplots()
ax.pie(realm_counts, labels=realm_counts.index, autopct='%1.1f%%', startangle=20)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.legend(title='Realms', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
#
# # Display the pie chart using Streamlit
st.pyplot(fig)

st.divider()
# Get and write random quotes
st.subheader("Quotes")

if st.button("Get random quotes"):
    random_quotes = quotes_data.sample(n=5)

    # Merge selected quotes with associated characters based on character_id
    merged_data = pd.merge(random_quotes, characters_data, left_on='character', right_on='id')

    merged_data = pd.merge(merged_data, movies_data, left_on="movie", right_on="id",
                           suffixes=('_character', '_movie'))

    for _, row in merged_data.iterrows():
        st.write(f"> *{row['dialog']}*")
        st.write(f"by **{row['name_character']}**, {row['race']} from {row['realm']}, on *{row['name_movie']}.*")
