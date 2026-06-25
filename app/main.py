import os

from fastapi import FastAPI, HTTPException
from psycopg2 import OperationalError
from psycopg2.pool import SimpleConnectionPool

app = FastAPI()


def get_pool():
    return SimpleConnectionPool(
        1,
        10,
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


@app.get("/records")
def records():
    try:
        pool = get_pool()
        conn = pool.getconn()
        cur = conn.cursor()
        cur.execute("select id, name from employees order by id")
        data = cur.fetchall()
        cur.close()
        pool.putconn(conn)
        pool.closeall()
        return {"records": [{"id": r[0], "name": r[1]} for r in data]}
    except OperationalError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc


@app.get("/")
def root():
    return {"status": "ok"}

