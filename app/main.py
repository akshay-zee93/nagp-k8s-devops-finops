from fastapi import FastAPI
from psycopg2.pool import SimpleConnectionPool
import os
app=FastAPI()
pool=SimpleConnectionPool(1,10,host=os.getenv("DB_HOST"),database=os.getenv("DB_NAME"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"))
@app.get('/records')
def records():
 conn=pool.getconn(); cur=conn.cursor(); cur.execute('select id,name from employees order by id'); data=cur.fetchall(); cur.close(); pool.putconn(conn); return {'records':[{'id':r[0],'name':r[1]} for r in data]}
@app.get('/')
def root(): return {'status':'ok'}
