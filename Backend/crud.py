from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional

from models import (
    Department, Category, ItemType, Size, Color, Tag, Condition,
    ItemStatus, Location, Item, ItemPhoto, ItemHistory
)
from schemas import (
    DepartmentCreate, DepartmentUpdate, CategoryCreate, CategoryUpdate,
    ItemTypeCreate, ItemTypeUpdate, SizeCreate, SizeUpdate,
    ColorCreate, ColorUpdate, TagCreate, TagUpdate,
    ConditionCreate, ConditionUpdate, ItemStatusCreate, ItemStatusUpdate,
    LocationCreate, LocationUpdate, ItemCreate, ItemUpdate,
    ItemPhotoCreate, ItemPhotoUpdate, ItemHistoryCreate, ItemFilters
)


def get_departments(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True):
    query = db.query(Department)
    if active_only:
        query = query.filter(Department.active == True)
    return query.order_by(Department.sort_order).offset(skip).limit(limit).all()

def get_department(db: Session, department_id: int):
    return db.query(Department).filter(Department.department_id == department_id).first()

def create_department(db: Session, department: DepartmentCreate):
    db_dept = Department(**department.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

def update_department(db: Session, department_id: int, department: DepartmentUpdate):
    db_dept = get_department(db, department_id)
    if not db_dept:
        return None
    for key, value in department.model_dump(exclude_unset=True).items():
        setattr(db_dept, key, value)
    db.commit()
    db.refresh(db_dept)
    return db_dept

def delete_department(db: Session, department_id: int):
    db_dept = get_department(db, department_id)
    if not db_dept:
        return False
    db.delete(db_dept)
    db.commit()
    return True


def get_categories(db: Session, skip: int = 0, limit: int = 100, department_id: Optional[int] = None, active_only: bool = True):
    query = db.query(Category)
    if active_only:
        query = query.filter(Category.active == True)
    if department_id:
        query = query.filter(Category.department_id == department_id)
    return query.order_by(Category.sort_order).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id).first()

def create_category(db: Session, category: CategoryCreate):
    db_cat = Category(**category.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_cat = get_category(db, category_id)
    if not db_cat:
        return None
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_cat, key, value)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def delete_category(db: Session, category_id: int):
    db_cat = get_category(db, category_id)
    if not db_cat:
        return False
    db.delete(db_cat)
    db.commit()
    return True


def get_item_types(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, active_only: bool = True):
    query = db.query(ItemType)
    if active_only:
        query = query.filter(ItemType.active == True)
    if category_id:
        query = query.filter(ItemType.category_id == category_id)
    return query.order_by(ItemType.sort_order).offset(skip).limit(limit).all()

def get_item_type(db: Session, item_type_id: int):
    return db.query(ItemType).filter(ItemType.item_type_id == item_type_id).first()

def create_item_type(db: Session, item_type: ItemTypeCreate):
    db_type = ItemType(**item_type.model_dump())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

def update_item_type(db: Session, item_type_id: int, item_type: ItemTypeUpdate):
    db_type = get_item_type(db, item_type_id)
    if not db_type:
        return None
    for key, value in item_type.model_dump(exclude_unset=True).items():
        setattr(db_type, key, value)
    db.commit()
    db.refresh(db_type)
    return db_type

def delete_item_type(db: Session, item_type_id: int):
    db_type = get_item_type(db, item_type_id)
    if not db_type:
        return False
    db.delete(db_type)
    db.commit()
    return True


def get_sizes(db: Session, skip: int = 0, limit: int = 100, size_system: Optional[str] = None):
    query = db.query(Size)
    if size_system:
        query = query.filter(Size.size_system == size_system)
    return query.order_by(Size.sort_order).offset(skip).limit(limit).all()

def get_size(db: Session, size_id: int):
    return db.query(Size).filter(Size.size_id == size_id).first()

def create_size(db: Session, size: SizeCreate):
    db_size = Size(**size.model_dump())
    db.add(db_size)
    db.commit()
    db.refresh(db_size)
    return db_size

def update_size(db: Session, size_id: int, size: SizeUpdate):
    db_size = get_size(db, size_id)
    if not db_size:
        return None
    for key, value in size.model_dump(exclude_unset=True).items():
        setattr(db_size, key, value)
    db.commit()
    db.refresh(db_size)
    return db_size

def delete_size(db: Session, size_id: int):
    db_size = get_size(db, size_id)
    if not db_size:
        return False
    db.delete(db_size)
    db.commit()
    return True


def get_colors(db: Session, skip: int = 0, limit: int = 100, color_family: Optional[str] = None):
    query = db.query(Color)
    if color_family:
        query = query.filter(Color.color_family == color_family)
    return query.order_by(Color.sort_order).offset(skip).limit(limit).all()

def get_color(db: Session, color_id: int):
    return db.query(Color).filter(Color.color_id == color_id).first()

def create_color(db: Session, color: ColorCreate):
    db_color = Color(**color.model_dump())
    db.add(db_color)
    db.commit()
    db.refresh(db_color)
    return db_color

def update_color(db: Session, color_id: int, color: ColorUpdate):
    db_color = get_color(db, color_id)
    if not db_color:
        return None
    for key, value in color.model_dump(exclude_unset=True).items():
        setattr(db_color, key, value)
    db.commit()
    db.refresh(db_color)
    return db_color

def delete_color(db: Session, color_id: int):
    db_color = get_color(db, color_id)
    if not db_color:
        return False
    db.delete(db_color)
    db.commit()
    return True


def get_tags(db: Session, skip: int = 0, limit: int = 100, tag_category: Optional[str] = None, active_only: bool = True):
    query = db.query(Tag)
    if active_only:
        query = query.filter(Tag.active == True)
    if tag_category:
        query = query.filter(Tag.tag_category == tag_category)
    return query.order_by(Tag.tag_name).offset(skip).limit(limit).all()

def get_tag(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.tag_id == tag_id).first()

def create_tag(db: Session, tag: TagCreate):
    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def update_tag(db: Session, tag_id: int, tag: TagUpdate):
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None
    for key, value in tag.model_dump(exclude_unset=True).items():
        setattr(db_tag, key, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int):
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return False
    db.delete(db_tag)
    db.commit()
    return True


def get_conditions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Condition).order_by(Condition.sort_order).offset(skip).limit(limit).all()

def get_condition(db: Session, condition_id: int):
    return db.query(Condition).filter(Condition.condition_id == condition_id).first()

def create_condition(db: Session, condition: ConditionCreate):
    db_cond = Condition(**condition.model_dump())
    db.add(db_cond)
    db.commit()
    db.refresh(db_cond)
    return db_cond

def update_condition(db: Session, condition_id: int, condition: ConditionUpdate):
    db_cond = get_condition(db, condition_id)
    if not db_cond:
        return None
    for key, value in condition.model_dump(exclude_unset=True).items():
        setattr(db_cond, key, value)
    db.commit()
    db.refresh(db_cond)
    return db_cond

def delete_condition(db: Session, condition_id: int):
    db_cond = get_condition(db, condition_id)
    if not db_cond:
        return False
    db.delete(db_cond)
    db.commit()
    return True


def get_item_statuses(db: Session, skip: int = 0, limit: int = 100, available_only: bool = False):
    query = db.query(ItemStatus)
    if available_only:
        query = query.filter(ItemStatus.is_available_for_sale == True)
    return query.order_by(ItemStatus.sort_order).offset(skip).limit(limit).all()

def get_item_status(db: Session, status_id: int):
    return db.query(ItemStatus).filter(ItemStatus.status_id == status_id).first()

def create_item_status(db: Session, status: ItemStatusCreate):
    db_status = ItemStatus(**status.model_dump())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

def update_item_status(db: Session, status_id: int, status: ItemStatusUpdate):
    db_status = get_item_status(db, status_id)
    if not db_status:
        return None
    for key, value in status.model_dump(exclude_unset=True).items():
        setattr(db_status, key, value)
    db.commit()
    db.refresh(db_status)
    return db_status

def delete_item_status(db: Session, status_id: int):
    db_status = get_item_status(db, status_id)
    if not db_status:
        return False
    db.delete(db_status)
    db.commit()
    return True


def get_locations(db: Session, skip: int = 0, limit: int = 100, location_type: Optional[str] = None, active_only: bool = True):
    query = db.query(Location)
    if active_only:
        query = query.filter(Location.active == True)
    if location_type:
        query = query.filter(Location.location_type == location_type)
    return query.order_by(Location.location_name).offset(skip).limit(limit).all()

def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.location_id == location_id).first()

def create_location(db: Session, location: LocationCreate):
    db_loc = Location(**location.model_dump())
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

def update_location(db: Session, location_id: int, location: LocationUpdate):
    db_loc = get_location(db, location_id)
    if not db_loc:
        return None
    for key, value in location.model_dump(exclude_unset=True).items():
        setattr(db_loc, key, value)
    db.commit()
    db.refresh(db_loc)
    return db_loc

def delete_location(db: Session, location_id: int):
    db_loc = get_location(db, location_id)
    if not db_loc:
        return False
    db.delete(db_loc)
    db.commit()
    return True


def get_items(db: Session, filters: ItemFilters):
    query = db.query(Item).options(
        joinedload(Item.department),
        joinedload(Item.category),
        joinedload(Item.item_type),
        joinedload(Item.size),
        joinedload(Item.color_primary),
        joinedload(Item.color_secondary),
        joinedload(Item.condition),
        joinedload(Item.status),
        joinedload(Item.current_location),
        joinedload(Item.tags),
        joinedload(Item.photos)
    )
    
    if filters.department_id:
        query = query.filter(Item.department_id == filters.department_id)
    if filters.category_id:
        query = query.filter(Item.category_id == filters.category_id)
    if filters.item_type_id:
        query = query.filter(Item.item_type_id == filters.item_type_id)
    if filters.brand:
        query = query.filter(Item.brand.ilike(f"%{filters.brand}%"))
    if filters.size_id:
        query = query.filter(Item.size_id == filters.size_id)
    if filters.color_primary_id:
        query = query.filter(Item.color_primary_id == filters.color_primary_id)
    if filters.condition_id:
        query = query.filter(Item.condition_id == filters.condition_id)
    if filters.status_id:
        query = query.filter(Item.status_id == filters.status_id)
    if filters.location_id:
        query = query.filter(Item.current_location_id == filters.location_id)
    if filters.min_price is not None:
        query = query.filter(Item.price >= filters.min_price)
    if filters.max_price is not None:
        query = query.filter(Item.price <= filters.max_price)
    if filters.on_sale is not None:
        query = query.filter(Item.on_sale == filters.on_sale)
    if filters.season:
        query = query.filter(Item.season == filters.season)
    if filters.search:
        term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Item.description.ilike(term),
                Item.brand.ilike(term),
                Item.customer_notes.ilike(term)
            )
        )
    if filters.tag_ids:
        query = query.join(Item.tags).filter(Tag.tag_id.in_(filters.tag_ids))
    
    total = query.count()
    
    sort_col = getattr(Item, filters.sort_by, Item.date_added)
    if filters.sort_order == "desc":
        query = query.order_by(sort_col.desc())
    else:
        query = query.order_by(sort_col.asc())
    
    skip = (filters.page - 1) * filters.page_size
    items = query.offset(skip).limit(filters.page_size).all()
    
    return items, total


def get_item(db: Session, item_id: int, with_relations: bool = True):
    query = db.query(Item)
    if with_relations:
        query = query.options(
            joinedload(Item.department),
            joinedload(Item.category),
            joinedload(Item.item_type),
            joinedload(Item.size),
            joinedload(Item.color_primary),
            joinedload(Item.color_secondary),
            joinedload(Item.condition),
            joinedload(Item.status),
            joinedload(Item.current_location),
            joinedload(Item.tags),
            joinedload(Item.photos),
            joinedload(Item.history)
        )
    return query.filter(Item.item_id == item_id).first()


def create_item(db: Session, item: ItemCreate):
    item_data = item.model_dump(exclude={'tag_ids'})
    db_item = Item(**item_data)
    
    if item.tag_ids:
        tags = db.query(Tag).filter(Tag.tag_id.in_(item.tag_ids)).all()
        db_item.tags = tags
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    create_item_history(db, ItemHistoryCreate(
        item_id=db_item.item_id,
        action="Created",
        new_value=f"Item created: {db_item.description[:50]}",
        notes="Initial creation"
    ))
    
    return db_item


def update_item(db: Session, item_id: int, item: ItemUpdate):
    db_item = get_item(db, item_id, with_relations=False)
    if not db_item:
        return None
    
    update_data = item.model_dump(exclude_unset=True, exclude={'tag_ids'})
    changes = []
    
    for key, value in update_data.items():
        old_val = getattr(db_item, key)
        if old_val != value:
            changes.append(f"{key}: {old_val} -> {value}")
            setattr(db_item, key, value)
    
    if item.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.tag_id.in_(item.tag_ids)).all()
        db_item.tags = tags
        changes.append("Tags updated")
    
    db.commit()
    db.refresh(db_item)
    
    if changes:
        create_item_history(db, ItemHistoryCreate(
            item_id=db_item.item_id,
            action="Updated",
            old_value="; ".join(changes[:5]),
            new_value="Item updated",
            notes=f"{len(changes)} fields changed"
        ))
    
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id, with_relations=False)
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True


def get_item_photos(db: Session, item_id: int):
    return db.query(ItemPhoto).filter(ItemPhoto.item_id == item_id).order_by(ItemPhoto.sort_order).all()

def create_item_photo(db: Session, photo: ItemPhotoCreate):
    db_photo = ItemPhoto(**photo.model_dump())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def update_item_photo(db: Session, photo_id: int, photo: ItemPhotoUpdate):
    db_photo = db.query(ItemPhoto).filter(ItemPhoto.photo_id == photo_id).first()
    if not db_photo:
        return None
    for key, value in photo.model_dump(exclude_unset=True).items():
        setattr(db_photo, key, value)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def delete_item_photo(db: Session, photo_id: int):
    db_photo = db.query(ItemPhoto).filter(ItemPhoto.photo_id == photo_id).first()
    if not db_photo:
        return False
    db.delete(db_photo)
    db.commit()
    return True


def get_item_history(db: Session, item_id: int, skip: int = 0, limit: int = 100):
    return db.query(ItemHistory).filter(ItemHistory.item_id == item_id).order_by(ItemHistory.action_date.desc()).offset(skip).limit(limit).all()

def create_item_history(db: Session, history: ItemHistoryCreate):
    db_hist = ItemHistory(**history.model_dump())
    db.add(db_hist)
    db.commit()
    db.refresh(db_hist)
    return db_hist


def bulk_update_status(db: Session, item_ids: List[int], status_id: int, notes: Optional[str] = None):
    items = db.query(Item).filter(Item.item_id.in_(item_ids)).all()
    for item in items:
        old_status = item.status_id
        item.status_id = status_id
        create_item_history(db, ItemHistoryCreate(
            item_id=item.item_id,
            action="Status_Changed",
            old_value=str(old_status),
            new_value=str(status_id),
            notes=notes
        ))
    db.commit()
    return len(items)


def bulk_update_location(db: Session, item_ids: List[int], location_id: int, notes: Optional[str] = None):
    items = db.query(Item).filter(Item.item_id.in_(item_ids)).all()
    for item in items:
        old_loc = item.current_location_id
        item.current_location_id = location_id
        create_item_history(db, ItemHistoryCreate(
            item_id=item.item_id,
            action="Location_Changed",
            old_value=str(old_loc) if old_loc else "None",
            new_value=str(location_id),
            notes=notes
        ))
    db.commit()
    return len(items)


def bulk_update_price(db: Session, item_ids: List[int], price: Optional[float] = None,
                      on_sale: Optional[bool] = None, sale_price: Optional[float] = None):
    items = db.query(Item).filter(Item.item_id.in_(item_ids)).all()
    for item in items:
        changes = []
        if price is not None:
            changes.append(f"price: {item.price} -> {price}")
            item.price = price
        if on_sale is not None:
            item.on_sale = on_sale
            changes.append(f"on_sale: {on_sale}")
        if sale_price is not None:
            item.sale_price = sale_price
            changes.append(f"sale_price: {sale_price}")
        
        if changes:
            create_item_history(db, ItemHistoryCreate(
                item_id=item.item_id,
                action="Price_Changed",
                old_value="; ".join(changes),
                new_value="Bulk price update",
                notes="Bulk operation"
            ))
    db.commit()
    return len(items)
