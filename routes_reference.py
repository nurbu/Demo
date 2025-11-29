from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from schemas import (
    Department, DepartmentCreate, DepartmentUpdate, DepartmentList,
    Category, CategoryCreate, CategoryUpdate, CategoryList, CategoryWithDepartment,
    ItemType, ItemTypeCreate, ItemTypeUpdate, ItemTypeList, ItemTypeWithCategory,
    Size, SizeCreate, SizeUpdate, SizeList,
    Color, ColorCreate, ColorUpdate, ColorList,
    Tag, TagCreate, TagUpdate, TagList,
    Condition, ConditionCreate, ConditionUpdate, ConditionList,
    ItemStatus, ItemStatusCreate, ItemStatusUpdate, ItemStatusList,
    Location, LocationCreate, LocationUpdate, LocationList
)
import crud


# ============================================================================
# Departments Router
# ============================================================================

router_departments = APIRouter(
    prefix="/departments",
    tags=["departments"]
)


@router_departments.get("/", response_model=DepartmentList)
def read_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all departments."""
    departments = crud.get_departments(db, skip, limit, active_only)
    return DepartmentList(departments=departments, total=len(departments))


@router_departments.post("/", response_model=Department, status_code=status.HTTP_201_CREATED)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new department."""
    return crud.create_department(db, department)


@router_departments.get("/{department_id}", response_model=Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    """Get a specific department by ID."""
    db_department = crud.get_department(db, department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


@router_departments.patch("/{department_id}", response_model=Department)
def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    """Update a department."""
    db_department = crud.update_department(db, department_id, department)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


@router_departments.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    """Delete a department."""
    success = crud.delete_department(db, department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return None


# ============================================================================
# Categories Router
# ============================================================================

router_categories = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router_categories.get("/", response_model=CategoryList)
def read_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    department_id: Optional[int] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all categories, optionally filtered by department."""
    categories = crud.get_categories(db, skip, limit, department_id, active_only)
    return CategoryList(categories=categories, total=len(categories))


@router_categories.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    return crud.create_category(db, category)


@router_categories.get("/{category_id}", response_model=CategoryWithDepartment)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID."""
    db_category = crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router_categories.patch("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """Update a category."""
    db_category = crud.update_category(db, category_id, category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router_categories.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category."""
    success = crud.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return None


# ============================================================================
# Item Types Router
# ============================================================================

router_item_types = APIRouter(
    prefix="/item-types",
    tags=["item-types"]
)


@router_item_types.get("/", response_model=ItemTypeList)
def read_item_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category_id: Optional[int] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all item types, optionally filtered by category."""
    item_types = crud.get_item_types(db, skip, limit, category_id, active_only)
    return ItemTypeList(item_types=item_types, total=len(item_types))


@router_item_types.post("/", response_model=ItemType, status_code=status.HTTP_201_CREATED)
def create_item_type(item_type: ItemTypeCreate, db: Session = Depends(get_db)):
    """Create a new item type."""
    return crud.create_item_type(db, item_type)


@router_item_types.get("/{item_type_id}", response_model=ItemTypeWithCategory)
def read_item_type(item_type_id: int, db: Session = Depends(get_db)):
    """Get a specific item type by ID."""
    db_item_type = crud.get_item_type(db, item_type_id)
    if db_item_type is None:
        raise HTTPException(status_code=404, detail="Item type not found")
    return db_item_type


@router_item_types.patch("/{item_type_id}", response_model=ItemType)
def update_item_type(item_type_id: int, item_type: ItemTypeUpdate, db: Session = Depends(get_db)):
    """Update an item type."""
    db_item_type = crud.update_item_type(db, item_type_id, item_type)
    if db_item_type is None:
        raise HTTPException(status_code=404, detail="Item type not found")
    return db_item_type


@router_item_types.delete("/{item_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_type(item_type_id: int, db: Session = Depends(get_db)):
    """Delete an item type."""
    success = crud.delete_item_type(db, item_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item type not found")
    return None


# ============================================================================
# Sizes Router
# ============================================================================

router_sizes = APIRouter(
    prefix="/sizes",
    tags=["sizes"]
)


@router_sizes.get("/", response_model=SizeList)
def read_sizes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    size_system: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all sizes, optionally filtered by size system (Letter, US Numeric, Waist, Shoes, Universal)."""
    sizes = crud.get_sizes(db, skip, limit, size_system)
    return SizeList(sizes=sizes, total=len(sizes))


@router_sizes.post("/", response_model=Size, status_code=status.HTTP_201_CREATED)
def create_size(size: SizeCreate, db: Session = Depends(get_db)):
    """Create a new size."""
    return crud.create_size(db, size)


@router_sizes.get("/{size_id}", response_model=Size)
def read_size(size_id: int, db: Session = Depends(get_db)):
    """Get a specific size by ID."""
    db_size = crud.get_size(db, size_id)
    if db_size is None:
        raise HTTPException(status_code=404, detail="Size not found")
    return db_size


@router_sizes.patch("/{size_id}", response_model=Size)
def update_size(size_id: int, size: SizeUpdate, db: Session = Depends(get_db)):
    """Update a size."""
    db_size = crud.update_size(db, size_id, size)
    if db_size is None:
        raise HTTPException(status_code=404, detail="Size not found")
    return db_size


@router_sizes.delete("/{size_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_size(size_id: int, db: Session = Depends(get_db)):
    """Delete a size."""
    success = crud.delete_size(db, size_id)
    if not success:
        raise HTTPException(status_code=404, detail="Size not found")
    return None


# ============================================================================
# Colors Router
# ============================================================================

router_colors = APIRouter(
    prefix="/colors",
    tags=["colors"]
)


@router_colors.get("/", response_model=ColorList)
def read_colors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    color_family: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all colors, optionally filtered by color family."""
    colors = crud.get_colors(db, skip, limit, color_family)
    return ColorList(colors=colors, total=len(colors))


@router_colors.post("/", response_model=Color, status_code=status.HTTP_201_CREATED)
def create_color(color: ColorCreate, db: Session = Depends(get_db)):
    """Create a new color."""
    return crud.create_color(db, color)


@router_colors.get("/{color_id}", response_model=Color)
def read_color(color_id: int, db: Session = Depends(get_db)):
    """Get a specific color by ID."""
    db_color = crud.get_color(db, color_id)
    if db_color is None:
        raise HTTPException(status_code=404, detail="Color not found")
    return db_color


@router_colors.patch("/{color_id}", response_model=Color)
def update_color(color_id: int, color: ColorUpdate, db: Session = Depends(get_db)):
    """Update a color."""
    db_color = crud.update_color(db, color_id, color)
    if db_color is None:
        raise HTTPException(status_code=404, detail="Color not found")
    return db_color


@router_colors.delete("/{color_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_color(color_id: int, db: Session = Depends(get_db)):
    """Delete a color."""
    success = crud.delete_color(db, color_id)
    if not success:
        raise HTTPException(status_code=404, detail="Color not found")
    return None


# ============================================================================
# Tags Router
# ============================================================================

router_tags = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


@router_tags.get("/", response_model=TagList)
def read_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    tag_category: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all tags, optionally filtered by tag category (Era, Style, Feature, Occasion, Pattern)."""
    tags = crud.get_tags(db, skip, limit, tag_category, active_only)
    return TagList(tags=tags, total=len(tags))


@router_tags.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """Create a new tag."""
    return crud.create_tag(db, tag)


@router_tags.get("/{tag_id}", response_model=Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    """Get a specific tag by ID."""
    db_tag = crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router_tags.patch("/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    """Update a tag."""
    db_tag = crud.update_tag(db, tag_id, tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router_tags.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Delete a tag."""
    success = crud.delete_tag(db, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return None


# ============================================================================
# Conditions Router
# ============================================================================

router_conditions = APIRouter(
    prefix="/conditions",
    tags=["conditions"]
)


@router_conditions.get("/", response_model=ConditionList)
def read_conditions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get all conditions."""
    conditions = crud.get_conditions(db, skip, limit)
    return ConditionList(conditions=conditions, total=len(conditions))


@router_conditions.post("/", response_model=Condition, status_code=status.HTTP_201_CREATED)
def create_condition(condition: ConditionCreate, db: Session = Depends(get_db)):
    """Create a new condition."""
    return crud.create_condition(db, condition)


@router_conditions.get("/{condition_id}", response_model=Condition)
def read_condition(condition_id: int, db: Session = Depends(get_db)):
    """Get a specific condition by ID."""
    db_condition = crud.get_condition(db, condition_id)
    if db_condition is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    return db_condition


@router_conditions.patch("/{condition_id}", response_model=Condition)
def update_condition(condition_id: int, condition: ConditionUpdate, db: Session = Depends(get_db)):
    """Update a condition."""
    db_condition = crud.update_condition(db, condition_id, condition)
    if db_condition is None:
        raise HTTPException(status_code=404, detail="Condition not found")
    return db_condition


@router_conditions.delete("/{condition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_condition(condition_id: int, db: Session = Depends(get_db)):
    """Delete a condition."""
    success = crud.delete_condition(db, condition_id)
    if not success:
        raise HTTPException(status_code=404, detail="Condition not found")
    return None


# ============================================================================
# Item Statuses Router
# ============================================================================

router_item_statuses = APIRouter(
    prefix="/item-statuses",
    tags=["item-statuses"]
)


@router_item_statuses.get("/", response_model=ItemStatusList)
def read_item_statuses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    available_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Get all item statuses."""
    statuses = crud.get_item_statuses(db, skip, limit, available_only)
    return ItemStatusList(statuses=statuses, total=len(statuses))


@router_item_statuses.post("/", response_model=ItemStatus, status_code=status.HTTP_201_CREATED)
def create_item_status(status: ItemStatusCreate, db: Session = Depends(get_db)):
    """Create a new item status."""
    return crud.create_item_status(db, status)


@router_item_statuses.get("/{status_id}", response_model=ItemStatus)
def read_item_status(status_id: int, db: Session = Depends(get_db)):
    """Get a specific item status by ID."""
    db_status = crud.get_item_status(db, status_id)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status


@router_item_statuses.patch("/{status_id}", response_model=ItemStatus)
def update_item_status(status_id: int, status: ItemStatusUpdate, db: Session = Depends(get_db)):
    """Update an item status."""
    db_status = crud.update_item_status(db, status_id, status)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status


@router_item_statuses.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_status(status_id: int, db: Session = Depends(get_db)):
    """Delete an item status."""
    success = crud.delete_item_status(db, status_id)
    if not success:
        raise HTTPException(status_code=404, detail="Status not found")
    return None


# ============================================================================
# Locations Router
# ============================================================================

router_locations = APIRouter(
    prefix="/locations",
    tags=["locations"]
)


@router_locations.get("/", response_model=LocationList)
def read_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    location_type: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all locations, optionally filtered by location type (Sales Floor, Storage, Processing, Archive)."""
    locations = crud.get_locations(db, skip, limit, location_type, active_only)
    return LocationList(locations=locations, total=len(locations))


@router_locations.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    """Create a new location."""
    return crud.create_location(db, location)


@router_locations.get("/{location_id}", response_model=Location)
def read_location(location_id: int, db: Session = Depends(get_db)):
    """Get a specific location by ID."""
    db_location = crud.get_location(db, location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@router_locations.patch("/{location_id}", response_model=Location)
def update_location(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    """Update a location."""
    db_location = crud.update_location(db, location_id, location)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@router_locations.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a location."""
    success = crud.delete_location(db, location_id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")
    return None
