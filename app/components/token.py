import logging
import os

from azure.identity import ManagedIdentityCredential

logger = logging.getLogger(__name__)


class TokenRetriever:
    def __init__(self):
        self.dbx_scope = os.environ.get("DBX_SCOPE")
        self.personal_access_token = os.getenv("DATABRICKS_PAT")
        self.mi_client_id = os.getenv("AZURE_CLIENT_ID")

    def retrieve_mi_token(self):
        """
        Retrieves managed identity token.
        :return: token: string
        """

        try:
            mi_creds = ManagedIdentityCredential(client_id=self.mi_client_id)
            token = mi_creds.get_token(self.dbx_scope).token
            logger.info("AAD token retrieved and set for managed identity.")
            return token
        except Exception as e:
            logger.error(f"Error retrieving AAD token: {str(e)}")
            raise

    def get_token(self):
        """
        Gets either personal access token or managed identity token.
        :return: token: string
        """

        if self.personal_access_token is not None:
            return self.personal_access_token
        elif self.mi_client_id is not None:
            return self.retrieve_mi_token()
        else:
            logger.info("Failed to provide authentication credentials.")
