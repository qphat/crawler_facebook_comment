from airflow.providers.mysql.hooks.mysql import MySqlHook

class MySQLLoader:
    def __init__(self, conn_id):
        """
        Initialize the loader with a connection ID.
        Args:
            conn_id (str): Airflow connection ID for the database.
        """
        self.conn_id = conn_id

    def create_table_if_not_exists(self, table_name, schema):
        """
        Create a table in MySQL if it does not already exist.
        Args:
            table_name (str): Name of the table to create.
            schema (str): SQL schema definition for the table.
        """
        mysql_hook = MySqlHook(mysql_conn_id=self.conn_id)
        connection = mysql_hook.get_sqlalchemy_engine()

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {schema}
        );
        """

        with connection.begin() as conn:
            conn.execute(create_table_query)

        print(f"Table '{table_name}' checked/created successfully.")

    def load_to_mysql(self, data, table_name):
        """
        Load cleaned data into a MySQL table.
        Args:
            data (list): List of dictionaries containing cleaned data.
            table_name (str): Target table name in the database.
        """
        mysql_hook = MySqlHook(mysql_conn_id=self.conn_id)
        connection = mysql_hook.get_sqlalchemy_engine()

        # Insert data into the database
        with connection.begin() as conn:
            conn.execute(
                f"""
                INSERT INTO {table_name} (comment)
                VALUES (:comment)
                """,
                data
            )
        print(f"Successfully loaded data into table: {table_name}")
