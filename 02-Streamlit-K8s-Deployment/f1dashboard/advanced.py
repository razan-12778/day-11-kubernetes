import streamlit as st


class F1Dashboard:
    def __init__(self) -> None:
        pass

    def introduction_page(self):
        """Layout the views of the dashboard"""
        st.title("F1 Dashboard")
        st.write(
            """
        This is the Formula 1 dashboard. The dashboard is built with Streamlit.
        The dashboard is built with **descriptive statistics** and **data visualizations**.
        You can navigate to the different pages using the sidebar.

        ---

        The page with the descriptive statistics allows a user of this dashboard to
        get the summary statistics of the tables in the database.

        ---

        In data visualizations the following visualizations are shown:
        - A bar chart with the top 5 drivers with the most points
        - A line chart with the points of Lewis Hamilton over the years
        """
        )


if __name__ == "__main__":
    dashboard = F1Dashboard()
    dashboard.introduction_page()
