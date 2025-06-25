from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True)
    query = Column(Text)
    answer = Column(Text)
    sources = Column(Text)

engine = create_engine("sqlite:///query_logs.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def log_query(query: str, answer: str, sources: list):
    db = SessionLocal()
    log_entry = QueryLog(
        query=query,
        answer=answer,
        sources=", ".join(sources)
    )
    db.add(log_entry)
    db.commit()
    db.close()