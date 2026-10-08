"""
In data visualizations the following visualizations are shown:
- A bar chart with the top 5 drivers with the most points
- A line chart with the points of Lewis Hamilton over the years
"""

import altair as alt
import streamlit as st
from f1dashboard.advanced.state import F1State
from f1dashboard.advanced.queries import F1Queries
import pandas as pd


class DataVisualizations:
    def __init__(self) -> None:
        self.f1_state = F1State()
        self.f1_queries = F1Queries()

    def top_drivers(self):
        """Create a bar chart with the top 5 drivers"""

        st.subheader("Top 5 Drivers")
        # Use your package logic to load data, then plot it accordingly.

        top_driver_data = self.f1_state.get_query_result("top_drivers")
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

    def lewis_hamilton_over_the_years(self):
        """Create a line chart with the points of Lewis Hamilton over the years"""
        st.subheader("Lewis Hamilton over the years")

        # Use your package logic to load data, then plot it accordingly.

        lewis_data = self.f1_state.get_query_result("lewis_over_the_years")
        lewis_data["year"] = pd.to_datetime(lewis_data["year"], format="%Y")
        line_chart = (
            alt.Chart(lewis_data).mark_line().encode(y="total_points", x="year")
        )

        st.altair_chart(line_chart, use_container_width=True)


if __name__ == "__main__":
    st.title("Data visualizations")

    data_visualizations = DataVisualizations()
    data_visualizations.top_drivers()
    data_visualizations.lewis_hamilton_over_the_years()
