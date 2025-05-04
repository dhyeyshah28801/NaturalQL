import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
# Load environment variables from .env file
load_dotenv()

# Fetch variables
db_type = os.getenv("DB_TYPE")           # e.g., 'postgresql', 'mysql', 'sqlite'
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
if db_type == "sqlite":
    db_url = f"sqlite:///{db_name}"
else:
    db_url = f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create SQLAlchemy engine
engine = create_engine(db_url)


def fetchData(sql_query):
    df = pd.read_sql(sql_query, engine)
    return df