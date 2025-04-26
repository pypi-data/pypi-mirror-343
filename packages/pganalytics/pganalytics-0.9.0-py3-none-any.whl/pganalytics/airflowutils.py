from google.cloud import bigquery
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

import pandas as pd
from airflow.operators.email import EmailOperator
import yaml

class BigQueryUtils:
    """
    A utility class for interacting with Google BigQuery. This class provides methods to 
    facilitate data operations such as querying data and managing BigQuery tables.

    Attributes:
        gcp_connection_id (str): The connection ID for GCP within Apache Airflow.
        client (google.cloud.bigquery.Client): The BigQuery client instance.
    """
    
    def __init__(self, gcp_connection_id="google_cloud_default"):
        """
        Initializes the BigQueryUtils instance with a specified GCP connection ID.

        Args:
            gcp_connection_id (str): A reference to the Google Cloud Platform connection configuration.
                                     Defaults to "google_cloud_default".
        """
        self.gcp_connection_id = gcp_connection_id
        self.client = self._initialize_client()

    def _initialize_client(self):
        """
        Initializes the BigQuery client using the Airflow BigQueryHook.

        Returns:
            google.cloud.bigquery.Client: A client instance to perform BigQuery operations.
        """
        hook = BigQueryHook(gcp_conn_id=self.gcp_connection_id)
        return hook.get_client()

    def fetch_data(self, query: str):
        """
        Executes a SQL query against the BigQuery database and returns the result as a Pandas DataFrame.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            pandas.DataFrame: The query result as a DataFrame.
        """
        query_job = self.client.query(query)
        return query_job.to_dataframe()
    
    def create_or_replace_table(self, query: str):
        """
        Executes a SQL query to create or replace a BigQuery table.

        Args:
            query (str): The SQL query for creating or replacing the table.
        """
        query_job = self.client.query(query)  # Initiate a query job
        query_job.result()  # Wait for the job to complete
        print(f"Table created or replaced successfully.")

    def create_table_and_insert_data(self, dataset_id: str, table_id: str, dataframe):
        table_ref = f"{dataset_id}.{table_id}"

        # Define the schema from the DataFrame
        schema = [
            bigquery.SchemaField(name, dtype.name)
            for name, dtype in dataframe.dtypes.items()
        ]

        # Try to get the table, and if it doesn't exist, create it
        try:
            self.client.get_table(table_ref)
        except Exception:
            table = bigquery.Table(table_ref, schema=schema)
            table = self.client.create_table(table)

        # Insert DataFrame data into BigQuery
        self.insert_data(dataset_id, table_id, dataframe)

    def insert_data(self, dataset_id: str, table_id: str, dataframe):
        """Inserts a pandas DataFrame into a specified BigQuery table."""
        table_ref = f"{dataset_id}.{table_id}"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
        load_job = self.client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
        load_job.result()  # Wait for the loading to complete
        print(f"Data inserted into {table_ref} successfully.")

    def truncate_and_insert_data(self, dataset_id: str, table_id: str, dataframe):
        """
        Truncates the table and then inserts new data.
        """
        table_ref = f"{dataset_id}.{table_id}"

        # Truncate the table by overwriting it
        # Set write_disposition to WRITE_TRUNCATE for truncating the table
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        load_job = self.client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
        load_job.result()
        print(f"Table {table_ref} has been truncated and new data inserted successfully.")

    def delete_data(self, query: str):
        """Deletes data from a specified BigQuery table on the query."""
        
        query_job = self.client.query(query)
        query_job.result()  # Wait for the job to complete
        print(f"Data deleted.")

    def delete_table(self, dataset_id: str, table_id: str):
        table_ref = f"{dataset_id}.{table_id}"
        try:
            self.client.delete_table(table_ref)
            print(f"Table {table_ref} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete table {table_ref}: {e}")

class EmailUtils:
    """
    A utility class for handling email operations in Apache Airflow, especially those involving
    data retrieval from Google BigQuery and sending data reports over email.

    Attributes:
        bq_utils (BigQueryUtils): An instance of BigQueryUtils for interacting with BigQuery.
    """
    
    def __init__(self, gcp_connection_id="google_cloud_default"):
        """
        Initializes the EmailUtils instance and its associated BigQueryUtils instance.

        Args:
            gcp_connection_id (str): A reference to the Google Cloud Platform connection configuration.
                                     Defaults to "google_cloud_default".
        """
        self.bq_utils = BigQueryUtils(gcp_connection_id)

    def fetch_data_and_create_excel(self, query: str, excel_file_path: str) -> None:
        """
        Fetches data from BigQuery using BigQueryUtils and writes the data to an Excel file.

        Args:
            query (str): The SQL query to be executed to retrieve data.
            excel_file_path (str): The path where the Excel file will be saved.
        """
        # Use bq_utils to fetch data
        dataframe = self.bq_utils.fetch_data(query)
        
        # Write DataFrame to Excel file
        dataframe.to_excel(excel_file_path, index=False)
    
    def create_email_task(self, task_id: str, receiver_email: str, subject: str, body: str, excel_file_path: str) -> EmailOperator:
        """
        Creates an Airflow email task to send an email with an attachment.

        Args:
            task_id (str): The unique identifier for the Airflow task.
            receiver_email (str): The recipient's email address.
            subject (str): The subject of the email.
            body (str): The HTML content of the email.
            excel_file_path (str): The path to the Excel file to be sent as an attachment.

        Returns:
            EmailOperator: An instance of the Airflow EmailOperator configured for sending emails.
        """
        return EmailOperator(
            task_id=task_id,
            to=receiver_email,
            subject=subject,
            html_content=body,
            files=[excel_file_path],  # Attach the file
    )

class Misc:
    """
    A miscellaneous utility class for handling file operations, such as reading SQL files
    and loading configuration from YAML files.
    """

    def read_sql_file(self, file_path: str):
        """
        Reads the contents of a SQL file and returns it as a string.

        Args:
            file_path (str): The path to the SQL file.

        Returns:
            str: The contents of the SQL file.
        """
        with open(file_path, 'r') as file:
            return file.read()
    
    def load_config(self, file_path: str):
        """
        Loads configuration settings from a YAML file.

        Args:
            file_path (str): The path to the YAML configuration file.

        Returns:
            dict: The configuration data loaded from the file.
        """
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config