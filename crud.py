from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime

from models import (
    Department, Category, ItemType, Size, Color, Tag, Condition, 
    ItemStatus, Location, Item, ItemPhoto, ItemHistory, item_tags
)
from schemas import (
    DepartmentCreate, DepartmentUpdate,
    CategoryCreate, CategoryUpdate,
    ItemTypeCreate, ItemTypeUpdate,
    SizeCreate, SizeUpdate,
    ColorCreate, ColorUpdate,
    TagCreate, TagUpdate,
    ConditionCreate, ConditionUpdate,
    ItemStatusCreate, ItemStatusUpdate,
    LocationCreate, LocationUpdate,
    ItemCreate, ItemUpdate,
    ItemPhotoCreate, ItemPhotoUpdate,
    ItemHistoryCreate,
    ItemFilters
)


# ============================================================================
# Department CRUD
# ============================================================================

def get_departments(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True):
    query = db.query(Department)
    if active_only:
        query = query.filter(Department.active == True)
    return query.order_by(Department.sort_order).offset(skip).limit(limit).all()


def get_department(db: Session, department_id: int):
    return db.query(Department).filter(Department.department_id == department_id).first()


def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def update_department(db: Session, department_id: int, department: DepartmentUpdate):
    db_department = get_department(db, department_id)
    if db_department:
        update_data = department.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_department, key, value)
        db.commit()
        db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: int):
    db_department = get_department(db, department_id)
    if db_department:
        db.delete(db_department)
        db.commit()
        return True
    return False


# ============================================================================
# Category CRUD
# ============================================================================

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
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = get_category(db, category_id)
    if db_category:
        update_data = category.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# ============================================================================
# ItemType CRUD
# ============================================================================

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
    db_item_type = ItemType(**item_type.model_dump())
    db.add(db_item_type)
    db.commit()
    db.refresh(db_item_type)
    return db_item_type


def update_item_type(db: Session, item_type_id: int, item_type: ItemTypeUpdate):
    db_item_type = get_item_type(db, item_type_id)
    if db_item_type:
        update_data = item_type.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item_type, key, value)
        db.commit()
        db.refresh(db_item_type)
    return db_item_type


def delete_item_type(db: Session, item_type_id: int):
    db_item_type = get_item_type(db, item_type_id)
    if db_item_type:
        db.delete(db_item_type)
        db.commit()
        return True
    return False


# ============================================================================
# Size CRUD
# ============================================================================

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
    if db_size:
        update_data = size.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_size, key, value)
        db.commit()
        db.refresh(db_size)
    return db_size


def delete_size(db: Session, size_id: int):
    db_size = get_size(db, size_id)
    if db_size:
        db.delete(db_size)
        db.commit()
        return True
    return False


# ============================================================================
# Color CRUD
# ============================================================================

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
    if db_color:
        update_data = color.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_color, key, value)
        db.commit()
        db.refresh(db_color)
    return db_color


def delete_color(db: Session, color_id: int):
    db_color = get_color(db, color_id)
    if db_color:
        db.delete(db_color)
        db.commit()
        return True
    return False


# ============================================================================
# Tag CRUD
# ============================================================================

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
    if db_tag:
        update_data = tag.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tag, key, value)
        db.commit()
        db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int):
    db_tag = get_tag(db, tag_id)
    if db_tag:
        db.delete(db_tag)
        db.commit()
        return True
    return False


# ============================================================================
# Condition CRUD
# ============================================================================

def get_conditions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Condition).order_by(Condition.sort_order).offset(skip).limit(limit).all()


def get_condition(db: Session, condition_id: int):
    return db.query(Condition).filter(Condition.condition_id == condition_id).first()


def create_condition(db: Session, condition: ConditionCreate):
    db_condition = Condition(**condition.model_dump())
    db.add(db_condition)
    db.commit()
    db.refresh(db_condition)
    return db_condition


def update_condition(db: Session, condition_id: int, condition: ConditionUpdate):
    db_condition = get_condition(db, condition_id)
    if db_condition:
        update_data = condition.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_condition, key, value)
        db.commit()
        db.refresh(db_condition)
    return db_condition


def delete_condition(db: Session, condition_id: int):
    db_condition = get_condition(db, condition_id)
    if db_condition:
        db.delete(db_condition)
        db.commit()
        return True
    return False


# ============================================================================
# ItemStatus CRUD
# ============================================================================

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
    if db_status:
        update_data = status.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_status, key, value)
        db.commit()
        db.refresh(db_status)
    return db_status


def delete_item_status(db: Session, status_id: int):
    db_status = get_item_status(db, status_id)
    if db_status:
        db.delete(db_status)
        db.commit()
        return True
    return False


# ============================================================================
# Location CRUD
# ============================================================================

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
    db_location = Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(db: Session, location_id: int, location: LocationUpdate):
    db_location = get_location(db, location_id)
    if db_location:
        update_data = location.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_location, key, value)
        db.commit()
        db.refresh(db_location)
    return db_location


def delete_location(db: Session, location_id: int):
    db_location = get_location(db, location_id)
    if db_location:
        db.delete(db_location)
        db.commit()
        return True
    return False


# ============================================================================
# Item CRUD (Advanced with filtering)
# ============================================================================

def get_items(db: Session, filters: ItemFilters):
    """Get items with advanced filtering and pagination"""
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
    
    # Apply filters
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
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Item.description.ilike(search_term),
                Item.brand.ilike(search_term),
                Item.customer_notes.ilike(search_term)
            )
        )
    if filters.tag_ids:
        # Filter by tags (items that have ANY of the specified tags)
        query = query.join(Item.tags).filter(Tag.tag_id.in_(filters.tag_ids))
    
    # Count total before pagination
    total = query.count()
    
    # Apply sorting
    sort_column = getattr(Item, filters.sort_by, Item.date_added)
    if filters.sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Apply pagination
    skip = (filters.page - 1) * filters.page_size
    items = query.offset(skip).limit(filters.page_size).all()
    
    return items, total


def get_item(db: Session, item_id: int, with_relations: bool = True):
    """Get a single item by ID"""
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
    """Create a new item with tags"""
    item_data = item.model_dump(exclude={'tag_ids'})
    db_item = Item(**item_data)
    
    # Add tags if provided
    if item.tag_ids:
        tags = db.query(Tag).filter(Tag.tag_id.in_(item.tag_ids)).all()
        db_item.tags = tags
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Create history record
    create_item_history(db, ItemHistoryCreate(
        item_id=db_item.item_id,
        action="Created",
        new_value=f"Item created: {db_item.description[:50]}",
        notes="Initial creation"
    ))
    
    return db_item


def update_item(db: Session, item_id: int, item: ItemUpdate):
    """Update an item"""
    db_item = get_item(db, item_id, with_relations=False)
    if not db_item:
        return None
    
    update_data = item.model_dump(exclude_unset=True, exclude={'tag_ids'})
    
    # Track changes for history
    changes = []
    for key, value in update_data.items():
        old_value = getattr(db_item, key)
        if old_value != value:
            changes.append(f"{key}: {old_value} → {value}")
            setattr(db_item, key, value)
    
    # Update tags if provided
    if item.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.tag_id.in_(item.tag_ids)).all()
        db_item.tags = tags
        changes.append(f"Tags updated")
    
    db.commit()
    db.refresh(db_item)
    
    # Create history record
    if changes:
        create_item_history(db, ItemHistoryCreate(
            item_id=db_item.item_id,
            action="Updated",
            old_value="; ".join(changes[:5]),  # Limit to first 5 changes
            new_value="Item updated",
            notes=f"{len(changes)} fields updated"
        ))
    
    return db_item


def delete_item(db: Session, item_id: int):
    """Delete an item"""
    db_item = get_item(db, item_id, with_relations=False)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


# ============================================================================
# ItemPhoto CRUD
# ============================================================================

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
    if db_photo:
        update_data = photo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_photo, key, value)
        db.commit()
        db.refresh(db_photo)
    return db_photo


def delete_item_photo(db: Session, photo_id: int):
    db_photo = db.query(ItemPhoto).filter(ItemPhoto.photo_id == photo_id).first()
    if db_photo:
        db.delete(db_photo)
        db.commit()
        return True
    return False


# ============================================================================
# ItemHistory CRUD
# ============================================================================

def get_item_history(db: Session, item_id: int, skip: int = 0, limit: int = 100):
    return db.query(ItemHistory).filter(ItemHistory.item_id == item_id).order_by(ItemHistory.action_date.desc()).offset(skip).limit(limit).all()


def create_item_history(db: Session, history: ItemHistoryCreate):
    db_history = ItemHistory(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history


# ============================================================================
# Bulk Operations
# ============================================================================

def bulk_update_status(db: Session, item_ids: List[int], status_id: int, notes: Optional[str] = None):
    """Update status for multiple items"""
    items = db.query(Item).filter(Item.item_id.in_(item_ids)).all()
    for item in items:
        old_status_id = item.status_id
        item.status_id = status_id
        
        # Create history
        create_item_history(db, ItemHistoryCreate(
            item_id=item.item_id,
            action="Status_Changed",
            old_value=str(old_status_id),
            new_value=str(status_id),
            notes=notes
        ))
    
    db.commit()
    return len(items)


def bulk_update_location(db: Session, item_ids: List[int], location_id: int, notes: Optional[str] = None):
    """Update location for multiple items"""
    items = db.query(Item).filter(Item.item_id.in_(item_ids)).all()
    for item in items:
        old_location_id = item.current_location_id
        item.current_location_id = location_id
        
        # Create history
        create_item_history(db, ItemHistoryCreate(
            item_id=item.item_id,
            action="Location_Changed",
            old_value=str(old_location_id) if old_location_id else "None",
            new_value=str(location_id),
            notes=notes
        ))
    
    db.commit()
    return len(items)


def bulk_update_price(db: Session, item_ids: List[int], price: Optional[float] = None, 
                     on_sale: Optional[bool] = None, sale_price: Optional[float] = None):
    """Update prices for multiple items"""
    items = db.query(Item).filter(Item.item_id.in_(item_ids)).all()
    for item in items:
        changes = []
        if price is not None:
            old_price = item.price
            item.price = price
            changes.append(f"price: {old_price} → {price}")
        if on_sale is not None:
            item.on_sale = on_sale
            changes.append(f"on_sale: {on_sale}")
        if sale_price is not None:
            item.sale_price = sale_price
            changes.append(f"sale_price: {sale_price}")
        
        # Create history
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
