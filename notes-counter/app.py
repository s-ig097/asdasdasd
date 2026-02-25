import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/add/<text>")
def add_note(text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (text) VALUES (%s)", (text,))
    conn.commit()
    cur.close()
    conn.close()
    return f"Added: {text}"


@app.route("/count")
def count_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM notes")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return str(count)


@app.route("/list")
def list_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM notes")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return "<br>".join([r[0] for r in rows])


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)