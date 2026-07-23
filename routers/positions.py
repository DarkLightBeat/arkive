from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Position
from schemas.position import PositionCreate, PositionUpdate, PositionResponse

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.post("/", response_model=PositionResponse)
def create_position(position: PositionCreate, db: Session = Depends(get_db)):
    new_position = Position(**position.model_dump())
    db.add(new_position)
    db.commit()
    db.refresh(new_position)
    return new_position


@router.get("/", response_model=list[PositionResponse])
def list_positions(open_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Position)
    if open_only:
        query = query.filter(Position.is_open == 1)
    return query.all()


@router.get("/{position_id}", response_model=PositionResponse)
def get_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


@router.put("/{position_id}", response_model=PositionResponse)
def update_position(position_id: int, updates: PositionUpdate, db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(position, field, value)

    db.commit()
    db.refresh(position)
    return position


@router.delete("/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    db.delete(position)
    db.commit()
    return {"message": f"Position {position_id} deleted successfully"}