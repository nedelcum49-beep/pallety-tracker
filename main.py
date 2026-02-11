
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from . import models
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trailer Pallet Tracker")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/trailers/{code}")
def create_trailer(code: str, db: Session = Depends(get_db)):
    t = models.Trailer(code=code)
    db.add(t)
    db.commit()
    return {"created": code}

@app.post("/trailers/{code}/scan/{barcode}")
def scan_pallet(code: str, barcode: str, operator: str, db: Session = Depends(get_db)):
    trailer = db.query(models.Trailer).filter_by(code=code, status="OPEN").first()
    if not trailer:
        raise HTTPException(404, "Trailer not open")

    existing = db.query(models.Pallet).filter_by(barcode=barcode, is_active=True).first()
    if existing:
        raise HTTPException(400, "Pallet already active")

    pallet = models.Pallet(barcode=barcode, trailer=trailer)
    db.add(pallet)

    count = db.query(models.Pallet).filter_by(trailer_id=trailer.id, is_active=True).count()
    if count >= settings.MAX_PALLETS:
        trailer.status = "CLOSED"

    db.add(models.Audit(action=f"SCAN {barcode}", operator=operator))
    db.commit()

    return {"pallet": barcode, "count": count}

@app.get("/trailers/{code}/zpl")
def export_zpl(code: str):
    return f"^XA^FO50,50^ADN,36,20^FDTRAILER {code}^FS^XZ"
