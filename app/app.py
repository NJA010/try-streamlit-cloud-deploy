import logging

import databricks.sql.client
import pandas as pd
import streamlit as st
from components.database import DatabricksSQLConnector
from components.token import TokenRetriever
from tables import generate_table

APP_NAME = "Streamlit Table Production Example"
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def cursor_to_df(cursor: databricks.sql.client.Cursor) -> pd.DataFrame:
    """
    Creates a dataframe out of a cursor result.

    :param cursor: a databricks sql cursor
    :return: a pandas DataFrame
    """

    result = pd.DataFrame(
        cursor.fetchall(), columns=[desc[0] for desc in cursor.description]
    )

    return result


def get_samples(connection: databricks.sql.client.Connection):
    """
    Get samples from nyctaxi trips.

    :param connection: a databricks sql client connection
    :return: a pandas DataFrame
    """

    with connection.cursor() as cursor:
        cursor.execute("SELECT * " "FROM samples.nyctaxi.trips " "LIMIT 100")
        result = cursor_to_df(cursor)

    return result


def display_streamlit_table():
    """
    Display streamlit table.
    """

    st.title(APP_NAME)
    st.table(generate_table(5, 5))
    st.markdown("---")


def display_databricks_sql_connection_example():
    """
    Display databricks sql connection example.
    """

    st.title("Databricks SQL Connection Example")

    # Get either personal access token or managed identity token
    token = TokenRetriever().get_token()
    logger.info("token retrieved")
    # Create Databricks sql connector
    connector = DatabricksSQLConnector(token)
    try:
        connection = connector.databricks_sql_connect()
        samples = get_samples(connection)
        st.dataframe(samples)
        logger.info("Fetched Databricks Datalake results")
    except Exception as e:
        logger.error(f"Error in Databricks SQL connection example: {str(e)}")


def display_footer(app_name):
    """
    Display footer

    :param app_name: the name of the streamlit application
    """

    st.text(f"Footer: {app_name}")


def main():
    display_streamlit_table()
    display_databricks_sql_connection_example()
    display_footer(APP_NAME)


if __name__ == "__main__":
    main()
