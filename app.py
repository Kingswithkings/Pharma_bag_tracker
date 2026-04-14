from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from database import Base, engine, get_db
from models import BagRecord
from schemas import BagCreate, BagUpdateStatus

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pharmacy Bag Tracker")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    bags = db.query(BagRecord).order_by(BagRecord.updated_at.desc()).all()
    active_bags = db.query(BagRecord).filter(BagRecord.status != "returned").count()
    returned_bags = db.query(BagRecord).filter(BagRecord.status == "returned").count()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "bags": bags,
            "active_bags": active_bags,
            "returned_bags": returned_bags,
        },
    )


@app.post("/bags")
def create_bag_record(
    bag_id: str = Form(...),
    ward: str = Form(...),
    status: str = Form("in_transit"),
    courier: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    record = BagRecord(
        bag_id=bag_id.strip(),
        ward=ward.strip(),
        status=status.strip(),
        courier=courier.strip() if courier else None,
        notes=notes.strip() if notes else None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return RedirectResponse(url="/", status_code=303)


@app.post("/bags/{record_id}/status")
def update_bag_status(
    record_id: int,
    status: str = Form(...),
    ward: Optional[str] = Form(None),
    courier: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    record = db.query(BagRecord).filter(BagRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.status = status.strip()
    if ward:
        record.ward = ward.strip()
    if courier:
        record.courier = courier.strip()
    if notes:
        record.notes = notes.strip()

    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.get("/api/bags")
def list_bags(db: Session = Depends(get_db)):
    return db.query(BagRecord).order_by(BagRecord.updated_at.desc()).all()


@app.get("/api/bags/active")
def active_bags(db: Session = Depends(get_db)):
    return db.query(BagRecord).filter(BagRecord.status != "returned").order_by(BagRecord.updated_at.desc()).all()