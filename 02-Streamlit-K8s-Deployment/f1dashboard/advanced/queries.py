import pandas as pd
import streamlit as st
from f1dashboard.advanced.database import F1Database


class F1Queries:
    def __init__(self) -> None:
        self.conn = F1Database().db_connection

    # # Perform query.
    # # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=600)
    def _run_query(_self, query):
        """
        Base utility method queries a database using pandas and returning a dataframe

        Parameters
        ----------
        query: Str
            SQL query as a f-string

        Returns
        -------
        races: pandas.DataFrame
            Dataframe containing the result of the query

        """

        return pd.read_sql_query(query, _self.conn)

    def retrieve_table(self, table_name):
        table_results = self._run_query(
            f"""
        select
            *
        FROM
            {table_name}
        """
        )
        return table_results

    def top_drivers(self):
        """
        Get the top 5 drivers with the most points.
        You can get the name from the drivers table and
        combine it with the points from the driver_standings table.
        Returns:
            pd.DataFrame: The top 5 drivers with the columns:
                        - driver_name
                        - total_points
        """

        top_drivers = self._run_query(
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
        """
        )

        return top_drivers

    def lewis_over_the_years(self):
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

        lewis_points = self._run_query(
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
        """
        )

        return lewis_points


if __name__ == "__main__":
    queries = F1Queries()
