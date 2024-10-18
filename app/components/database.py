import logging
import os

import databricks.sql.client
from databricks import sql

logger = logging.getLogger(__name__)


class DatabricksSQLConnector:
    def __init__(self, token):
        # Scope represents the programmatic ID for Azure Databricks.
        # https://learn.microsoft.com/en-us/azure/databricks/dev-tools/service-prin-aad-token#--get-an-azure-active-directory-access-token
        self.server_hostname = os.environ.get("SERVER_HOSTNAME")
        self.http_path = os.environ.get("HTTP_PATH")
        self.token = token

    def databricks_sql_connect(self) -> databricks.sql.client.Connection:
        """
        Connects with the datalake using the environment variables.

        :return: connection: databricks sql client connection
        """

        connection = sql.connect(
            server_hostname=self.server_hostname,
            http_path="/sql/1.0/warehouses/" + self.http_path,
            access_token=self.token,
        )

        return connection
