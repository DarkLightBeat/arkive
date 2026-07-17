from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "ARKIVE backend is running"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT extversion FROM pg_extension WHERE extname='vector'"))
    row = result.fetchone()
    return {"pgvector_version": row[0] if row else "not found"}