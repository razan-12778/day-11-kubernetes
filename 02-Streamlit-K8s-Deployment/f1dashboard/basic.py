import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from timeit import default_timer as timer


conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo=False)
TABLES = [
    "races",
    "circuits",
    "constructor_results",
    "constructor_standings",
    "constructors",
    "driver_standings",
    "drivers",
    "lap_times",
    "pit_stops",
    "qualifying",
    "results",
    "seasons",
    "status",
]


@st.cache_data
def load_data(table_name):
    """
    Loads the races data from the F1 database.
    Implement the right caching decorator.
    Returns:
        pd.DataFrame: The race dataset
    """
    data = pd.read_sql_query(f"select * from {table_name}", conn)

    return data


def create_main_page():
    """
    Creates the following Streamlit headers:
    - A title
    - A subheader
    - A title in the sidebar
    - A markdown section in the sidebar
    - A widget in the sidebar to select a table from the `TABLES` list,
    and then return the selected table (instead of the hard-coded "races" value)
    """
    st.title("Formula 1 Dashboard")
    st.info(
        """
    Delete me once completed
    """
    )
    selected_table = "races"

    st.subheader("Welcome to the Formula 1 Dashboard")
    st.sidebar.title("Info")
    st.sidebar.markdown("This page shows the Formula 1 data from 1950 to 2020")
    selected_table = st.sidebar.selectbox("Select a table", TABLES, key="table")

    return selected_table


def summary_statistics(data):
    """
    Creates a subheader and writes the summary statistics for the data
    """
    st.subheader("Summary statistics")
    st.info("Use the describe method to get the summary statistics")

    st.write(data.describe())


@st.cache_data
def top_drivers():
    """
    Get the top 5 drivers with the most points.
    You can get the name from the drivers table and
    combine it with the points from the driver_standings table.
    Returns:
        pd.DataFrame: The top 5 drivers with the columns:
                      - driver_name
                      - total_points
    """
    st.info("Write a query to get the top 5 drivers and visualize the results.")

    top_drivers = pd.read_sql_query(
        """
    select
        concat(forename,' ',surname) as driver_name,
        sum(points) as total_points
    FROM
        drivers
    inner join
        driver_standings on drivers.driver_id = driver_standings.driver_id
    group by
        concat(forename,' ',surname)
    order by
        sum(points) desc
    limit
        5
    """,
        conn,
    )
    return top_drivers


@st.cache_data
def lewis_over_the_years():
    """
    Get the points from Lewis Hamilton between 2007 and 2018.
    Use the following table to get the data:
        - drivers
        - driver_standings
        - races

    Returns:
        pd.DataFrame: The points from Lewis Hamilton over the years, with the columns:
                        - year
                        - total_points
    """
    st.info(
        "Write a query to get the points of Lewis Hamilton over the years and visualize the results."
    )

    lewis_points = pd.read_sql_query(
        """
    with lewis_id as (
        select driver_id from drivers where surname = 'Hamilton' and forename = 'Lewis'
    ),

    driver_points as (
        select points, race_id, driver_id from driver_standings
    ),

    race_results as (
        select race_id, year from races
    )

    select
        year, max(points) as total_points
    from
        lewis_id
    inner join
        driver_points
    on
        lewis_id.driver_id = driver_points.driver_id
    inner join
        race_results on race_results.race_id = driver_points.race_id
    where year > 2006
    group by
        year
    """,
        conn,
    )
    return lewis_points


def session_state(data):
    """
    Initialize the session state
    using data as the key and value as the
    initialization value.

    Put data in the session state after having
    initialized it.

    Args:
        data (pd.DataFrame): The formula 1 dataset
    """

    # Initialization of session state, assign a random value
    # to the session state

    if "data" not in st.session_state:
        st.session_state["data"] = "value"

    # Update the session state using the dataframe

    st.session_state["data"] = data


if __name__ == "__main__":
    selected_table = create_main_page()

    # used to time the loading of the data
    start = timer()
    data = load_data(selected_table)
    end = timer()
    st.sidebar.info(f"{round(end-start,4)} seconds to load the data")

    st.dataframe(data)

    summary_statistics(data)
    session_state(data)

    st.subheader("Top 5 Drivers")
    top_driver_data = top_drivers()
    st.write(top_driver_data)
    st.warning("Use the Altair library to create a bar chart with the top drivers")
    # create a bar chart with the top drivers

    bar_chart = (
        alt.Chart(top_driver_data)
        .mark_bar()
        .encode(
            y=alt.Y("total_points"),
            x=alt.X("driver_name", sort="-y"),
            color="driver_name",
            tooltip="total_points",
        )
    )

    st.altair_chart(bar_chart, use_container_width=True)

    st.subheader("Lewis Hamilton over the years")
    lewis_years = lewis_over_the_years()

    # Convert the year column to datetime
    lewis_years["year"] = pd.to_datetime(lewis_years["year"], format="%Y")

    st.warning("Create a line chart with the lewis_years, use the Altair library")

    line_chart = alt.Chart(lewis_years).mark_line().encode(y="total_points", x="year")

    st.altair_chart(line_chart, use_container_width=True)
