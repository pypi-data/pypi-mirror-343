import os

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):

    AWS_DEFAULT_REGION: str
    AWS_DEFAULT_REGION = "ap-southeast-2"
    DATABRICKS_CLUSTER_HOST: str
    DATABRICKS_CLUSTER_HOST = os.getenv("DATABRICKS_PROD_CLUSTER_HOST")
    DATABRICKS_PAT_TOKEN: str
    DATABRICKS_PAT_TOKEN = os.getenv("DATABRICKS_PAT_TOKEN")
    DATABRICKS_SQL_CLUSTER_PATH: str
    DATABRICKS_SQL_CLUSTER_PATH = os.getenv("DATABRICKS_SQL_CLUSTER_PATH")
    PIPELINE_TYPE: str
    PIPELINE_TYPE = os.getenv("PIPELINE_TYPE")
    VECTOR_SEARCH_PREFIX: str
    VECTOR_SEARCH_PREFIX = "growlithe"
    VS_ENDPOINT_TYPE: str
    VS_ENDPOINT_TYPE = "STANDARD"
    UNITY_CATALOG: str
    UNITY_CATALOG = os.getenv("UNITY_CATALOG")


load_dotenv()
settings = Settings()
