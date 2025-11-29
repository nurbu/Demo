from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from database import get_db
from schemas import (
    Item, ItemCreate, ItemUpdate, ItemWithRelations, ItemWithHistory,
    ItemList, ItemFilters, ItemPhoto, ItemPhotoCreate, ItemPhotoUpdate,
    ItemHistory, ItemHistoryCreate,
    BulkUpdateStatus, BulkUpdateLocation, BulkUpdatePrice, BulkDelete
)
import crud

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=ItemList)
def read_items(
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
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    Get all items with optional filtering, searching, and pagination.
    
    - **department_id**: Filter by department
    - **category_id**: Filter by category
    - **item_type_id**: Filter by item type
    - **brand**: Search by brand name (case-insensitive partial match)
    - **size_id**: Filter by size
    - **color_primary_id**: Filter by primary color
    - **condition_id**: Filter by condition
    - **status_id**: Filter by status
    - **location_id**: Filter by location
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **on_sale**: Filter items on sale
    - **season**: Filter by season
    - **tag_ids**: Filter by tags (items with any of these tags)
    - **search**: Search in description, brand, and customer notes
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (max 100)
    - **sort_by**: Field to sort by (e.g., date_added, price, brand)
    - **sort_order**: Sort order (asc or desc)
    """
    filters = ItemFilters(
        department_id=department_id,
        category_id=category_id,
        item_type_id=item_type_id,
        brand=brand,
        size_id=size_id,
        color_primary_id=color_primary_id,
        condition_id=condition_id,
        status_id=status_id,
        location_id=location_id,
        min_price=min_price,
        max_price=max_price,
        on_sale=on_sale,
        season=season,
        tag_ids=tag_ids,
        search=search,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    items, total = crud.get_items(db, filters)
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return ItemList(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("/", response_model=ItemWithRelations, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item.
    
    The item will be created with all specified attributes and tags.
    A history record will be automatically created.
    """
    return crud.create_item(db, item)


@router.get("/{item_id}", response_model=ItemWithHistory)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific item by ID.
    
    Returns the item with all related data including department, category,
    item type, colors, size, condition, status, location, tags, photos, and history.
    """
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.patch("/{item_id}", response_model=ItemWithRelations)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """
    Update an item.
    
    Only the fields provided will be updated. A history record will be
    automatically created tracking the changes.
    """
    db_item = crud.update_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item.
    
    This will also delete all associated photos and history records (cascade).
    """
    success = crud.delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None


# ============================================================================
# Item Photos Endpoints
# ============================================================================

@router.get("/{item_id}/photos", response_model=List[ItemPhoto])
def read_item_photos(item_id: int, db: Session = Depends(get_db)):
    """Get all photos for a specific item, ordered by sort_order."""
    # Verify item exists
    item = crud.get_item(db, item_id, with_relations=False)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return crud.get_item_photos(db, item_id)


@router.post("/{item_id}/photos", response_model=ItemPhoto, status_code=status.HTTP_201_CREATED)
def create_item_photo(item_id: int, photo: ItemPhotoCreate, db: Session = Depends(get_db)):
    """
    Add a photo to an item.
    
    Set is_primary=true to make this the main photo for the item.
    """
    # Verify item exists
    item = crud.get_item(db, item_id, with_relations=False)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Override item_id from path
    photo.item_id = item_id
    return crud.create_item_photo(db, photo)


@router.patch("/photos/{photo_id}", response_model=ItemPhoto)
def update_item_photo(photo_id: int, photo: ItemPhotoUpdate, db: Session = Depends(get_db)):
    """Update a photo (change sort order, set as primary, etc.)."""
    db_photo = crud.update_item_photo(db, photo_id, photo)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo


@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_photo(photo_id: int, db: Session = Depends(get_db)):
    """Delete a photo."""
    success = crud.delete_item_photo(db, photo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")
    return None


# ============================================================================
# Item History Endpoints
# ============================================================================

@router.get("/{item_id}/history", response_model=List[ItemHistory])
def read_item_history(
    item_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get history for a specific item.
    
    Returns all changes made to the item, ordered by date (newest first).
    """
    # Verify item exists
    item = crud.get_item(db, item_id, with_relations=False)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return crud.get_item_history(db, item_id, skip, limit)


# ============================================================================
# Bulk Operations Endpoints
# ============================================================================

@router.post("/bulk/update-status")
def bulk_update_status(bulk_update: BulkUpdateStatus, db: Session = Depends(get_db)):
    """
    Update status for multiple items at once.
    
    Useful for marking multiple items as sold, on hold, etc.
    """
    count = crud.bulk_update_status(db, bulk_update.item_ids, bulk_update.status_id, bulk_update.notes)
    return {"message": f"Updated status for {count} items", "updated_count": count}


@router.post("/bulk/update-location")
def bulk_update_location(bulk_update: BulkUpdateLocation, db: Session = Depends(get_db)):
    """
    Update location for multiple items at once.
    
    Useful for moving items from storage to sales floor, etc.
    """
    count = crud.bulk_update_location(db, bulk_update.item_ids, bulk_update.location_id, bulk_update.notes)
    return {"message": f"Updated location for {count} items", "updated_count": count}


@router.post("/bulk/update-price")
def bulk_update_price(bulk_update: BulkUpdatePrice, db: Session = Depends(get_db)):
    """
    Update prices for multiple items at once.
    
    Can update regular price, sale status, and sale price.
    """
    count = crud.bulk_update_price(
        db, 
        bulk_update.item_ids, 
        bulk_update.price, 
        bulk_update.on_sale, 
        bulk_update.sale_price
    )
    return {"message": f"Updated prices for {count} items", "updated_count": count}


@router.post("/bulk/delete")
def bulk_delete(bulk_delete: BulkDelete, db: Session = Depends(get_db)):
    """
    Delete multiple items at once.
    
    ⚠️ Warning: This permanently deletes items and all associated data.
    """
    deleted_count = 0
    for item_id in bulk_delete.item_ids:
        if crud.delete_item(db, item_id):
            deleted_count += 1
    
    return {"message": f"Deleted {deleted_count} items", "deleted_count": deleted_count}
