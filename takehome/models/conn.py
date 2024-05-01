import psycopg2
import os

conn_str = os.getenv("CONN_STR")
conn = psycopg2.connect(conn_str)
