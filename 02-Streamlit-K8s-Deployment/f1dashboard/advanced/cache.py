import streamlit as st
from advanced.queries import F1Queries


class F1Cache:
    def __init__(self) -> None:
        """Initialize the cache class"""
        self.f1_queries = F1Queries()

    def store_in_cache(self, key, value):
        """Store data in the cache

        Args:
            key (str): The key to store the data under
            value (str): The value to store
        """
        st.session_state[key] = value

    def get_data_from_cache(self, key):
        """Get data from the cache if it exists

        Args:
            key (str): The key to get the data from

        Returns:
            pd.DataFrame: The data from the cache
        """
        if key not in st.session_state:
            self.store_in_cache(key, None)
        return st.session_state[key]

    def get_data(self, table_to_query):
        """Get data from the cache or the database

        Args:
            table_to_query (str): The query to run

        Returns:
            pd.DataFrame: The results of the query
        """
        if table_to_query in st.session_state:
            st.info("Retrieved the data from cache")
            return self.get_data_from_cache(table_to_query)
        else:
            st.info("Retrieved the data from the database")
            # table_to_query is a string value that is mapped to
            # a function in the F1Queries class. See the mapping
            # under the __init__ method in the F1Queries class.
            results = getattr(self.f1_queries, table_to_query)()

            # Store the results in the cache
            self.store_in_cache(table_to_query, results)
            return results
