from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

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


# Departments

router_departments = APIRouter(prefix="/departments", tags=["departments"])

@router_departments.get("/", response_model=DepartmentList)
def list_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    depts = crud.get_departments(db, skip, limit, active_only)
    return DepartmentList(departments=depts, total=len(depts))

@router_departments.post("/", response_model=Department, status_code=status.HTTP_201_CREATED)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, dept)

@router_departments.get("/{department_id}", response_model=Department)
def get_department(department_id: int, db: Session = Depends(get_db)):
    dept = crud.get_department(db, department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router_departments.patch("/{department_id}", response_model=Department)
def update_department(department_id: int, dept: DepartmentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_department(db, department_id, dept)
    if not updated:
        raise HTTPException(status_code=404, detail="Department not found")
    return updated

@router_departments.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    if not crud.delete_department(db, department_id):
        raise HTTPException(status_code=404, detail="Department not found")


# Categories

router_categories = APIRouter(prefix="/categories", tags=["categories"])

@router_categories.get("/", response_model=CategoryList)
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    department_id: Optional[int] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    cats = crud.get_categories(db, skip, limit, department_id, active_only)
    return CategoryList(categories=cats, total=len(cats))

@router_categories.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(cat: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, cat)

@router_categories.get("/{category_id}", response_model=CategoryWithDepartment)
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = crud.get_category(db, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@router_categories.patch("/{category_id}", response_model=Category)
def update_category(category_id: int, cat: CategoryUpdate, db: Session = Depends(get_db)):
    updated = crud.update_category(db, category_id, cat)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router_categories.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    if not crud.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail="Category not found")


# Item Types

router_item_types = APIRouter(prefix="/item-types", tags=["item-types"])

@router_item_types.get("/", response_model=ItemTypeList)
def list_item_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category_id: Optional[int] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    types = crud.get_item_types(db, skip, limit, category_id, active_only)
    return ItemTypeList(item_types=types, total=len(types))

@router_item_types.post("/", response_model=ItemType, status_code=status.HTTP_201_CREATED)
def create_item_type(item_type: ItemTypeCreate, db: Session = Depends(get_db)):
    return crud.create_item_type(db, item_type)

@router_item_types.get("/{item_type_id}", response_model=ItemTypeWithCategory)
def get_item_type(item_type_id: int, db: Session = Depends(get_db)):
    it = crud.get_item_type(db, item_type_id)
    if not it:
        raise HTTPException(status_code=404, detail="Item type not found")
    return it

@router_item_types.patch("/{item_type_id}", response_model=ItemType)
def update_item_type(item_type_id: int, item_type: ItemTypeUpdate, db: Session = Depends(get_db)):
    updated = crud.update_item_type(db, item_type_id, item_type)
    if not updated:
        raise HTTPException(status_code=404, detail="Item type not found")
    return updated

@router_item_types.delete("/{item_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_type(item_type_id: int, db: Session = Depends(get_db)):
    if not crud.delete_item_type(db, item_type_id):
        raise HTTPException(status_code=404, detail="Item type not found")


# Sizes

router_sizes = APIRouter(prefix="/sizes", tags=["sizes"])

@router_sizes.get("/", response_model=SizeList)
def list_sizes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    size_system: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    sizes = crud.get_sizes(db, skip, limit, size_system)
    return SizeList(sizes=sizes, total=len(sizes))

@router_sizes.post("/", response_model=Size, status_code=status.HTTP_201_CREATED)
def create_size(size: SizeCreate, db: Session = Depends(get_db)):
    return crud.create_size(db, size)

@router_sizes.get("/{size_id}", response_model=Size)
def get_size(size_id: int, db: Session = Depends(get_db)):
    s = crud.get_size(db, size_id)
    if not s:
        raise HTTPException(status_code=404, detail="Size not found")
    return s

@router_sizes.patch("/{size_id}", response_model=Size)
def update_size(size_id: int, size: SizeUpdate, db: Session = Depends(get_db)):
    updated = crud.update_size(db, size_id, size)
    if not updated:
        raise HTTPException(status_code=404, detail="Size not found")
    return updated

@router_sizes.delete("/{size_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_size(size_id: int, db: Session = Depends(get_db)):
    if not crud.delete_size(db, size_id):
        raise HTTPException(status_code=404, detail="Size not found")


# Colors

router_colors = APIRouter(prefix="/colors", tags=["colors"])

@router_colors.get("/", response_model=ColorList)
def list_colors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    color_family: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    colors = crud.get_colors(db, skip, limit, color_family)
    return ColorList(colors=colors, total=len(colors))

@router_colors.post("/", response_model=Color, status_code=status.HTTP_201_CREATED)
def create_color(color: ColorCreate, db: Session = Depends(get_db)):
    return crud.create_color(db, color)

@router_colors.get("/{color_id}", response_model=Color)
def get_color(color_id: int, db: Session = Depends(get_db)):
    c = crud.get_color(db, color_id)
    if not c:
        raise HTTPException(status_code=404, detail="Color not found")
    return c

@router_colors.patch("/{color_id}", response_model=Color)
def update_color(color_id: int, color: ColorUpdate, db: Session = Depends(get_db)):
    updated = crud.update_color(db, color_id, color)
    if not updated:
        raise HTTPException(status_code=404, detail="Color not found")
    return updated

@router_colors.delete("/{color_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_color(color_id: int, db: Session = Depends(get_db)):
    if not crud.delete_color(db, color_id):
        raise HTTPException(status_code=404, detail="Color not found")


# Tags

router_tags = APIRouter(prefix="/tags", tags=["tags"])

@router_tags.get("/", response_model=TagList)
def list_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    tag_category: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    tags = crud.get_tags(db, skip, limit, tag_category, active_only)
    return TagList(tags=tags, total=len(tags))

@router_tags.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db, tag)

@router_tags.get("/{tag_id}", response_model=Tag)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    t = crud.get_tag(db, tag_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tag not found")
    return t

@router_tags.patch("/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    updated = crud.update_tag(db, tag_id, tag)
    if not updated:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated

@router_tags.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    if not crud.delete_tag(db, tag_id):
        raise HTTPException(status_code=404, detail="Tag not found")


# Conditions

router_conditions = APIRouter(prefix="/conditions", tags=["conditions"])

@router_conditions.get("/", response_model=ConditionList)
def list_conditions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    conds = crud.get_conditions(db, skip, limit)
    return ConditionList(conditions=conds, total=len(conds))

@router_conditions.post("/", response_model=Condition, status_code=status.HTTP_201_CREATED)
def create_condition(cond: ConditionCreate, db: Session = Depends(get_db)):
    return crud.create_condition(db, cond)

@router_conditions.get("/{condition_id}", response_model=Condition)
def get_condition(condition_id: int, db: Session = Depends(get_db)):
    c = crud.get_condition(db, condition_id)
    if not c:
        raise HTTPException(status_code=404, detail="Condition not found")
    return c

@router_conditions.patch("/{condition_id}", response_model=Condition)
def update_condition(condition_id: int, cond: ConditionUpdate, db: Session = Depends(get_db)):
    updated = crud.update_condition(db, condition_id, cond)
    if not updated:
        raise HTTPException(status_code=404, detail="Condition not found")
    return updated

@router_conditions.delete("/{condition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_condition(condition_id: int, db: Session = Depends(get_db)):
    if not crud.delete_condition(db, condition_id):
        raise HTTPException(status_code=404, detail="Condition not found")


# Item Statuses

router_item_statuses = APIRouter(prefix="/item-statuses", tags=["item-statuses"])

@router_item_statuses.get("/", response_model=ItemStatusList)
def list_item_statuses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    available_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    statuses = crud.get_item_statuses(db, skip, limit, available_only)
    return ItemStatusList(statuses=statuses, total=len(statuses))

@router_item_statuses.post("/", response_model=ItemStatus, status_code=status.HTTP_201_CREATED)
def create_item_status(stat: ItemStatusCreate, db: Session = Depends(get_db)):
    return crud.create_item_status(db, stat)

@router_item_statuses.get("/{status_id}", response_model=ItemStatus)
def get_item_status(status_id: int, db: Session = Depends(get_db)):
    s = crud.get_item_status(db, status_id)
    if not s:
        raise HTTPException(status_code=404, detail="Status not found")
    return s

@router_item_statuses.patch("/{status_id}", response_model=ItemStatus)
def update_item_status(status_id: int, stat: ItemStatusUpdate, db: Session = Depends(get_db)):
    updated = crud.update_item_status(db, status_id, stat)
    if not updated:
        raise HTTPException(status_code=404, detail="Status not found")
    return updated

@router_item_statuses.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_status(status_id: int, db: Session = Depends(get_db)):
    if not crud.delete_item_status(db, status_id):
        raise HTTPException(status_code=404, detail="Status not found")


# Locations

router_locations = APIRouter(prefix="/locations", tags=["locations"])

@router_locations.get("/", response_model=LocationList)
def list_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    location_type: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    locs = crud.get_locations(db, skip, limit, location_type, active_only)
    return LocationList(locations=locs, total=len(locs))

@router_locations.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
def create_location(loc: LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db, loc)

@router_locations.get("/{location_id}", response_model=Location)
def get_location(location_id: int, db: Session = Depends(get_db)):
    l = crud.get_location(db, location_id)
    if not l:
        raise HTTPException(status_code=404, detail="Location not found")
    return l

@router_locations.patch("/{location_id}", response_model=Location)
def update_location(location_id: int, loc: LocationUpdate, db: Session = Depends(get_db)):
    updated = crud.update_location(db, location_id, loc)
    if not updated:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated

@router_locations.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    if not crud.delete_location(db, location_id):
        raise HTTPException(status_code=404, detail="Location not found")
