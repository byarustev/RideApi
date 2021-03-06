import psycopg2
import psycopg2.extras as extra
from flask import current_app

TABLE_QUERIES = (
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL )
            """,
            """
            CREATE TABLE IF NOT EXISTS rides (
                ride_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL,
                origin VARCHAR(255) NOT NULL, destination VARCHAR(255) NOT NULL,
                departure_time timestamp, slots integer, description text,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON UPDATE CASCADE
                ON DELETE CASCADE )
            """,
            """
            CREATE TABLE IF NOT EXISTS ride_requests (
                request_id SERIAL PRIMARY KEY, ride_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (ride_id) REFERENCES rides (ride_id) ON UPDATE CASCADE
                ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON UPDATE CASCADE
                ON DELETE CASCADE,
                status VARCHAR(10) NOT NULL )
            """,
            """
            CREATE TABLE IF NOT EXISTS friend_requests (
                request_id SERIAL PRIMARY KEY, from_user INTEGER NOT NULL,
                to_user INTEGER NOT NULL, FOREIGN KEY (from_user) REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (to_user) REFERENCES users (user_id) ON UPDATE CASCADE
                ON DELETE CASCADE,
                status VARCHAR(10) NOT NULL )
            """,
            """
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL,
                message text, FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
            )
            """)


class DataBaseConnection:
    def __init__(self, database=None):
            try:
                if database:
                    self.connection = psycopg2.connect(database=database, user="mczhkqyutgspud",
                                                       password="bc4506c9ca483df2d1756d8fecebdc9" +
                                                                "095df6593414ac3e85b7962f019252600",
                                                       host="ec2-23-23-248-192.compute-1.amazonaws.com",
                                                       port="5432")
                else:
                    if current_app.config["TESTING"]:
                        self.connection = psycopg2.connect(database=current_app.config["TEST_DATABASE"], user="postgres",
                                                           password="",
                                                           host="localhost",
                                                           port="5432")
                    else:

                        self.connection = psycopg2.connect(database=current_app.config["DATABASE"], user="mczhkqyutgspud",
                                                           password="bc4506c9ca483df2d1756d8fecebdc9" +
                                                                    "095df6593414ac3e85b7962f019252600",
                                                           host="ec2-23-23-248-192.compute-1.amazonaws.com",
                                                           port="5432")

                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
                self.dict_cursor = self.connection.cursor(cursor_factory=extra.DictCursor)

                self.create_tables()
            except Exception as exp:
                print(exp)

    def create_tables(self):

        for query in TABLE_QUERIES:
            self.cursor.execute(query)

    def drop_test_tables(self):

        query = "DROP TABLE IF EXISTS {0} CASCADE"
        tables = ["users", "rides", "ride_requests", "friend_requests", "notifications"]

        for table in tables:
            self.cursor.execute(query.format(table))


if __name__ == "__main__":
    db_connection = DataBaseConnection("dbl39rci502hrl")
    db_connection.create_tables()
