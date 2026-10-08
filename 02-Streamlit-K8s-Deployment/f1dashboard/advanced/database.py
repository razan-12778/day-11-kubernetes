import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


class F1Database:
    def __init__(
        self,
    ) -> None:
        self.db_connection = self.init_connection(URL.create(**st.secrets["postgres"]))

    @st.cache_resource
    def init_connection(_self, credentials):
        """Create the database connection using the right credentials

        Args:
            credentials (_type_): _description_

        Returns:
            _type_: _description_
        """
        conn = create_engine(credentials, echo=False)
        return conn
