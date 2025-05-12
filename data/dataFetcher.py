import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import sqlite3
import pymysql
import psycopg2
import re
class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.db_type = os.getenv("DB_TYPE", "sqlite").lower()
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.engine = self._create_engine()

    def _create_engine(self):
        if self.db_type == "sqlite":
            db_url = f"sqlite:///{self.db_name}"
        else:
            db_url = f"{self.db_type}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return create_engine(db_url)

    def fetch_data(self, sql_query):
        return pd.read_sql(sql_query, self.engine)

    def fetch_schema(self):
        if self.db_type == 'sqlite':
            return self._fetch_sqlite_schema()
        elif self.db_type == 'mysql':
            return self._fetch_mysql_schema()
        elif self.db_type == 'postgresql':
            return self._fetch_postgres_schema()
        else:
            raise ValueError(f"Unsupported DB_TYPE: {self.db_type}")

    def _fetch_sqlite_schema(self):
        db_path = os.getenv('SQLITE_PATH', self.db_name)
        schema_dict = {}
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [row[0] for row in cur.fetchall()]
            for table in tables:
                cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
                schema = cur.fetchone()
                if schema and schema[0]:
                    schema_dict[table] = schema[0]
            cur.close()
            conn.close()
        except Exception as e:
            raise RuntimeError(f"Error accessing SQLite database: {e}")
        return schema_dict

    def _fetch_mysql_schema(self):
        schema_dict = {}
        try:
            conn = pymysql.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            cur = conn.cursor()
            cur.execute("SHOW TABLES;")
            tables = [row[0] for row in cur.fetchall()]
            for table in tables:
                cur.execute(f"SHOW CREATE TABLE `{table}`;")
                schema = cur.fetchone()
                if schema and len(schema) > 1:
                    schema_dict[table] = schema[1]
            cur.close()
            conn.close()
        except Exception as e:
            raise RuntimeError(f"Error accessing MySQL database: {e}")
        return schema_dict

    def _fetch_postgres_schema(self):
        schema_dict = {}
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                dbname=self.db_name
            )
            cur = conn.cursor()
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE';
            """)
            tables = [row[0] for row in cur.fetchall()]
            for table in tables:
                cur.execute(f"""
                    SELECT 'CREATE TABLE ' || relname || E'\n(\n' ||
                    array_to_string(
                        array_agg(
                            '    ' || column_name || ' ' ||  type || ' '|| not_null
                        )
                        , E',\n'
                    ) || E'\n);\n'
                    FROM (
                        SELECT
                            c.relname,
                            a.attname AS column_name,
                            pg_catalog.format_type(a.atttypid, a.atttypmod) AS type,
                            CASE WHEN a.attnotnull THEN 'NOT NULL' ELSE 'NULL' END as not_null
                        FROM pg_class c,
                            pg_attribute a,
                            pg_type t
                        WHERE c.relname = %s
                            AND a.attnum > 0
                            AND a.attrelid = c.oid
                            AND a.atttypid = t.oid
                        ORDER BY a.attnum
                    ) as tabledef
                    GROUP BY relname;
                """, (table,))
                schema = cur.fetchone()
                if schema and schema[0]:
                    schema_dict[table] = schema[0]
            cur.close()
            conn.close()
        except Exception as e:
            raise RuntimeError(f"Error accessing PostgreSQL database: {e}")
        return schema_dict
    
    def get_condensed_schema(SELF):

        db_type = os.getenv('DB_TYPE', 'sqlite').lower()
        output_lines = []

        if db_type == 'sqlite':
            db_path = os.getenv('SQLITE_PATH', './data/dataset.db') # Default path
            if not os.path.exists(db_path):
                return f"Error: SQLite database file not found at {db_path}"
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Get table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = [row[0] for row in cursor.fetchall()]
                output_lines.append("Tables:")
                for table in tables:
                    output_lines.append(f"- `{table}`")
                output_lines.append("\nRelationships:")

                # Get relationships for each table
                for table_name in tables:
                    cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
                    foreign_keys = cursor.fetchall()
                    for fk in foreign_keys:
                        # fk columns: id, seq, table (referenced), from (current), to (referenced_col)
                        referenced_table = fk[2]
                        from_column = fk[3]
                        to_column = fk[4] if fk[4] else "PRIMARY KEY" # to_column can be None
                        output_lines.append(
                            f"- Table `{table_name}` column `{from_column}` REFERENCES `{referenced_table}`(`{to_column}`)"
                        )
                conn.close()
            except sqlite3.Error as e:
                return f"SQLite Error: {e}"

        elif db_type == 'mysql':
            mysql_host = os.getenv('db_HOST', 'localhost')
            mysql_user = os.getenv('db_USER', 'root')
            mysql_password = os.getenv('db_PASSWORD', '')
            mysql_db = os.getenv('db_name')

            if not mysql_db:
                return "Error: MYSQL_DB environment variable not set for MySQL connection."

            try:
                conn = pymysql.connect(
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    database=mysql_db,
                    cursorclass=pymysql.cursors.DictCursor # Easier to work with results
                )
                cursor = conn.cursor()

                # Get table names
                cursor.execute("SHOW TABLES;")
                tables = [row['Tables_in_' + mysql_db] for row in cursor.fetchall()]
                output_lines.append("Tables:")
                for table in tables:
                    output_lines.append(f"- `{table}`")
                output_lines.append("\nRelationships:")

                # Get relationships from INFORMATION_SCHEMA
                # This is generally more reliable than parsing SHOW CREATE TABLE
                query = """
                    SELECT
                        TABLE_NAME,                  -- The table with the foreign key
                        COLUMN_NAME,                 -- The column in TABLE_NAME that is the FK
                        REFERENCED_TABLE_NAME,       -- The table the FK references
                        REFERENCED_COLUMN_NAME       -- The column in REFERENCED_TABLE_NAME
                    FROM
                        INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                    WHERE
                        REFERENCED_TABLE_SCHEMA = %s -- Ensure it's the current database
                        AND REFERENCED_TABLE_NAME IS NOT NULL; -- Filter for actual FKs
                """
                cursor.execute(query, (mysql_db,))
                foreign_keys = cursor.fetchall()
                for fk in foreign_keys:
                    output_lines.append(
                        f"- Table `{fk['TABLE_NAME']}` column `{fk['COLUMN_NAME']}` REFERENCES `{fk['REFERENCED_TABLE_NAME']}`(`{fk['REFERENCED_COLUMN_NAME']}`)"
                    )
                conn.close()
            except pymysql.MySQLError as e:
                return f"MySQL Error: {e}"
            except ImportError:
                return "Error: pymysql library is not installed. Please install it using 'pip install pymysql'."


        else:
            return f"Error: Unsupported DB_TYPE '{db_type}'. Please use 'sqlite' or 'mysql'."

        if not output_lines or len(output_lines) <=3 : # Check if only headers were added
            return "No tables or relationships found in the database."
            
        return "\n".join(output_lines)
