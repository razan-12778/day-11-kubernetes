import streamlit as st
from f1dashboard.advanced.queries import F1Queries


class F1State:
    def __init__(self) -> None:
        """Initialize the cache class"""
        self.f1_queries = F1Queries()

    def store_in_state(self, key, value):
        """Store data in the cache

        Args:
            key (str): The key to store the data under
            value (str): The value to store
        """
        st.session_state[key] = value

    def get_data_from_state(self, key):
        """Get data from the cache if it exists

        Args:
            key (str): The key to get the data from

        Returns:
            pd.DataFrame: The data from the cache
        """
        if key not in st.session_state:
            self.store_in_state(key, None)
        return st.session_state[key]

    def get_query_result(self, f1query_method_to_call):
        """Get query result from state or the database. Store in state if new

        Args:
            f1query_method_to_call (str): The query to run

        Returns:
            pd.DataFrame: The results of the query
        """
        if f1query_method_to_call in st.session_state:
            st.info("Retrieve the data from state...")
            return self.get_data_from_state(f1query_method_to_call)
        else:
            st.info("Retrieve the data from the database...")
            # f1query_method_to_call is a string value that is mapped to
            # a function in the F1Queries class. See the mapping
            # under the __init__ method in the F1Queries class.
            results = getattr(self.f1_queries, f1query_method_to_call)()

            # Store the results in the cache
            self.store_in_state(f1query_method_to_call, results)
            return results
