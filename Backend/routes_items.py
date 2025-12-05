from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import math
import shutil
import os
import uuid

from database import get_db
from schemas import (
    Item, ItemCreate, ItemUpdate, ItemWithRelations, ItemWithHistory,
    ItemList, ItemFilters, ItemPhoto, ItemPhotoCreate, ItemPhotoUpdate,
    ItemHistory, BulkUpdateStatus, BulkUpdateLocation, BulkUpdatePrice, BulkDelete
)
import crud

router = APIRouter(prefix="/items", tags=["items"])

IMAGEDIR = "images/"

@router.post("/{item_id}/photos/upload", response_model=ItemPhoto, status_code=status.HTTP_201_CREATED)
async def upload_item_photo(
    item_id: int, 
    file: UploadFile = File(...),
    is_primary: bool = Form(False),
    sort_order: int = Form(1),
    db: Session = Depends(get_db)
):
    if not crud.get_item(db, item_id, with_relations=False):
        raise HTTPException(status_code=404, detail="Item not found")

    # Ensure image directory exists
    if not os.path.exists(IMAGEDIR):
        os.makedirs(IMAGEDIR)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{item_id}_{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(IMAGEDIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Create DB record
    # API serves images at /images/{filename}
    web_path = f"/images/{unique_filename}"
    
    photo_create = ItemPhotoCreate(
        item_id=item_id,
        file_path=web_path,
        is_primary=is_primary,
        sort_order=sort_order
    )
    
    return crud.create_item_photo(db, photo_create)



@router.get("/", response_model=ItemList)
def list_items(
    department_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    item_type_id: Optional[int] = Query(None),
    brand: Optional[str] = Query(None),
    size_id: Optional[int] = Query(None),
    color_primary_id: Optional[int] = Query(None),
    condition_id: Optional[int] = Query(None),
    status_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    on_sale: Optional[bool] = Query(None),
    season: Optional[str] = Query(None),
    tag_ids: Optional[List[int]] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("date_added"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    filters = ItemFilters(
        department_id=department_id, category_id=category_id,
        item_type_id=item_type_id, brand=brand, size_id=size_id,
        color_primary_id=color_primary_id, condition_id=condition_id,
        status_id=status_id, location_id=location_id,
        min_price=min_price, max_price=max_price, on_sale=on_sale,
        season=season, tag_ids=tag_ids, search=search,
        page=page, page_size=page_size, sort_by=sort_by, sort_order=sort_order
    )
    
    items, total = crud.get_items(db, filters)
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return ItemList(
        items=items, total=total, page=page,
        page_size=page_size, total_pages=total_pages
    )


@router.post("/", response_model=ItemWithRelations, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)


@router.get("/{item_id}", response_model=ItemWithHistory)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.patch("/{item_id}", response_model=ItemWithRelations)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    if not crud.delete_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item not found")


# Photos

@router.get("/{item_id}/photos", response_model=List[ItemPhoto])
def list_item_photos(item_id: int, db: Session = Depends(get_db)):
    if not crud.get_item(db, item_id, with_relations=False):
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.get_item_photos(db, item_id)


@router.post("/{item_id}/photos", response_model=ItemPhoto, status_code=status.HTTP_201_CREATED)
def add_item_photo(item_id: int, photo: ItemPhotoCreate, db: Session = Depends(get_db)):
    if not crud.get_item(db, item_id, with_relations=False):
        raise HTTPException(status_code=404, detail="Item not found")
    photo.item_id = item_id
    return crud.create_item_photo(db, photo)


@router.patch("/photos/{photo_id}", response_model=ItemPhoto)
def update_photo(photo_id: int, photo: ItemPhotoUpdate, db: Session = Depends(get_db)):
    db_photo = crud.update_item_photo(db, photo_id, photo)
    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo


@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    if not crud.delete_item_photo(db, photo_id):
        raise HTTPException(status_code=404, detail="Photo not found")


# History

@router.get("/{item_id}/history", response_model=List[ItemHistory])
def list_item_history(
    item_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    if not crud.get_item(db, item_id, with_relations=False):
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.get_item_history(db, item_id, skip, limit)


# Bulk Operations

@router.post("/bulk/update-status")
def bulk_status_update(data: BulkUpdateStatus, db: Session = Depends(get_db)):
    count = crud.bulk_update_status(db, data.item_ids, data.status_id, data.notes)
    return {"message": f"Updated {count} items", "updated_count": count}


@router.post("/bulk/update-location")
def bulk_location_update(data: BulkUpdateLocation, db: Session = Depends(get_db)):
    count = crud.bulk_update_location(db, data.item_ids, data.location_id, data.notes)
    return {"message": f"Updated {count} items", "updated_count": count}


@router.post("/bulk/update-price")
def bulk_price_update(data: BulkUpdatePrice, db: Session = Depends(get_db)):
    count = crud.bulk_update_price(db, data.item_ids, data.price, data.on_sale, data.sale_price)
    return {"message": f"Updated {count} items", "updated_count": count}


@router.post("/bulk/delete")
def bulk_delete_items(data: BulkDelete, db: Session = Depends(get_db)):
    deleted = sum(1 for item_id in data.item_ids if crud.delete_item(db, item_id))
    return {"message": f"Deleted {deleted} items", "deleted_count": deleted}
