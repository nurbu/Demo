from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Department Schemas
# ============================================================================

class DepartmentBase(BaseModel):
    department_name: str
    sort_order: int
    active: bool = True


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    sort_order: Optional[int] = None
    active: Optional[bool] = None


class Department(DepartmentBase):
    department_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Category Schemas
# ============================================================================

class CategoryBase(BaseModel):
    category_name: str
    department_id: int
    sort_order: int
    active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    department_id: Optional[int] = None
    sort_order: Optional[int] = None
    active: Optional[bool] = None


class Category(CategoryBase):
    category_id: int
    
    model_config = ConfigDict(from_attributes=True)


class CategoryWithDepartment(Category):
    department: Department


# ============================================================================
# ItemType Schemas
# ============================================================================

class ItemTypeBase(BaseModel):
    item_type_name: str
    category_id: int
    sort_order: int
    active: bool = True


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemTypeUpdate(BaseModel):
    item_type_name: Optional[str] = None
    category_id: Optional[int] = None
    sort_order: Optional[int] = None
    active: Optional[bool] = None


class ItemType(ItemTypeBase):
    item_type_id: int
    
    model_config = ConfigDict(from_attributes=True)


class ItemTypeWithCategory(ItemType):
    category: Category


# ============================================================================
# Size Schemas
# ============================================================================

class SizeBase(BaseModel):
    size_value: str
    size_system: str  # Letter, US Numeric, Waist, Shoes, Universal
    sort_order: int
    notes: Optional[str] = None


class SizeCreate(SizeBase):
    pass


class SizeUpdate(BaseModel):
    size_value: Optional[str] = None
    size_system: Optional[str] = None
    sort_order: Optional[int] = None
    notes: Optional[str] = None


class Size(SizeBase):
    size_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Color Schemas
# ============================================================================

class ColorBase(BaseModel):
    color_name: str
    color_family: str  # Neutrals, Blues, Reds, etc.
    hex_code: Optional[str] = None
    sort_order: int


class ColorCreate(ColorBase):
    pass


class ColorUpdate(BaseModel):
    color_name: Optional[str] = None
    color_family: Optional[str] = None
    hex_code: Optional[str] = None
    sort_order: Optional[int] = None


class Color(ColorBase):
    color_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Tag Schemas
# ============================================================================

class TagBase(BaseModel):
    tag_name: str
    tag_category: str  # Era, Style, Feature, Occasion, Pattern
    description: Optional[str] = None
    active: bool = True


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    tag_name: Optional[str] = None
    tag_category: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None


class Tag(TagBase):
    tag_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Condition Schemas
# ============================================================================

class ConditionBase(BaseModel):
    condition_name: str
    description: Optional[str] = None
    sort_order: int


class ConditionCreate(ConditionBase):
    pass


class ConditionUpdate(BaseModel):
    condition_name: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None


class Condition(ConditionBase):
    condition_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# ItemStatus Schemas
# ============================================================================

class ItemStatusBase(BaseModel):
    status_name: str
    description: Optional[str] = None
    is_available_for_sale: bool
    sort_order: int


class ItemStatusCreate(ItemStatusBase):
    pass


class ItemStatusUpdate(BaseModel):
    status_name: Optional[str] = None
    description: Optional[str] = None
    is_available_for_sale: Optional[bool] = None
    sort_order: Optional[int] = None


class ItemStatus(ItemStatusBase):
    status_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Location Schemas
# ============================================================================

class LocationBase(BaseModel):
    location_name: str
    location_type: str  # Sales Floor, Storage, Processing, Archive
    description: Optional[str] = None
    active: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    location_name: Optional[str] = None
    location_type: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None


class Location(LocationBase):
    location_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# ItemPhoto Schemas
# ============================================================================

class ItemPhotoBase(BaseModel):
    file_path: str
    is_primary: bool = False
    sort_order: int = 1


class ItemPhotoCreate(ItemPhotoBase):
    item_id: int


class ItemPhotoUpdate(BaseModel):
    file_path: Optional[str] = None
    is_primary: Optional[bool] = None
    sort_order: Optional[int] = None


class ItemPhoto(ItemPhotoBase):
    photo_id: int
    item_id: int
    uploaded_date: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# ItemHistory Schemas
# ============================================================================

class ItemHistoryBase(BaseModel):
    action: str  # Created, Updated, Status_Changed, Price_Changed, Sold, Removed, Location_Changed
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    notes: Optional[str] = None


class ItemHistoryCreate(ItemHistoryBase):
    item_id: int


class ItemHistory(ItemHistoryBase):
    history_id: int
    item_id: int
    action_date: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Item Schemas
# ============================================================================

class ItemBase(BaseModel):
    department_id: int
    category_id: int
    item_type_id: int
    brand: Optional[str] = None
    size_id: int
    color_primary_id: int
    color_secondary_id: Optional[int] = None
    material: Optional[str] = None
    condition_id: int
    status_id: int
    current_location_id: Optional[int] = None
    price: float = Field(ge=0)
    original_price: Optional[float] = Field(default=None, ge=0)
    on_sale: bool = False
    sale_price: Optional[float] = Field(default=None, ge=0)
    description: str
    internal_notes: Optional[str] = None
    customer_notes: Optional[str] = None
    season: Optional[str] = None  # All Season, Spring/Summer, Fall/Winter


class ItemCreate(ItemBase):
    tag_ids: Optional[List[int]] = []


class ItemUpdate(BaseModel):
    department_id: Optional[int] = None
    category_id: Optional[int] = None
    item_type_id: Optional[int] = None
    brand: Optional[str] = None
    size_id: Optional[int] = None
    color_primary_id: Optional[int] = None
    color_secondary_id: Optional[int] = None
    material: Optional[str] = None
    condition_id: Optional[int] = None
    status_id: Optional[int] = None
    current_location_id: Optional[int] = None
    price: Optional[float] = Field(default=None, ge=0)
    original_price: Optional[float] = Field(default=None, ge=0)
    on_sale: Optional[bool] = None
    sale_price: Optional[float] = Field(default=None, ge=0)
    description: Optional[str] = None
    internal_notes: Optional[str] = None
    customer_notes: Optional[str] = None
    season: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    date_sold: Optional[datetime] = None


class Item(ItemBase):
    item_id: int
    date_added: datetime
    date_sold: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class ItemWithRelations(Item):
    """Complete item with all related data"""
    department: Department
    category: Category
    item_type: ItemType
    size: Size
    color_primary: Color
    color_secondary: Optional[Color] = None
    condition: Condition
    status: ItemStatus
    current_location: Optional[Location] = None
    tags: List[Tag] = []
    photos: List[ItemPhoto] = []


class ItemWithHistory(ItemWithRelations):
    """Item with complete history"""
    history: List[ItemHistory] = []


# ============================================================================
# Response Schemas for Lists
# ============================================================================

class DepartmentList(BaseModel):
    departments: List[Department]
    total: int


class CategoryList(BaseModel):
    categories: List[Category]
    total: int


class ItemTypeList(BaseModel):
    item_types: List[ItemType]
    total: int


class SizeList(BaseModel):
    sizes: List[Size]
    total: int


class ColorList(BaseModel):
    colors: List[Color]
    total: int


class TagList(BaseModel):
    tags: List[Tag]
    total: int


class ConditionList(BaseModel):
    conditions: List[Condition]
    total: int


class ItemStatusList(BaseModel):
    statuses: List[ItemStatus]
    total: int


class LocationList(BaseModel):
    locations: List[Location]
    total: int


class ItemList(BaseModel):
    items: List[ItemWithRelations]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# Filter/Query Schemas
# ============================================================================

class ItemFilters(BaseModel):
    """Query parameters for filtering items"""
    department_id: Optional[int] = None
    category_id: Optional[int] = None
    item_type_id: Optional[int] = None
    brand: Optional[str] = None
    size_id: Optional[int] = None
    color_primary_id: Optional[int] = None
    condition_id: Optional[int] = None
    status_id: Optional[int] = None
    location_id: Optional[int] = None
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    on_sale: Optional[bool] = None
    season: Optional[str] = None
    tag_ids: Optional[List[int]] = None
    search: Optional[str] = None  # Search in description, brand, etc.
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: Optional[str] = Field(default="date_added")  # date_added, price, brand, etc.
    sort_order: Optional[str] = Field(default="desc")  # asc or desc


# ============================================================================
# Bulk Operation Schemas
# ============================================================================

class BulkUpdateStatus(BaseModel):
    """Update status for multiple items"""
    item_ids: List[int]
    status_id: int
    notes: Optional[str] = None


class BulkUpdateLocation(BaseModel):
    """Update location for multiple items"""
    item_ids: List[int]
    location_id: int
    notes: Optional[str] = None


class BulkUpdatePrice(BaseModel):
    """Update prices for multiple items"""
    item_ids: List[int]
    price: Optional[float] = Field(default=None, ge=0)
    on_sale: Optional[bool] = None
    sale_price: Optional[float] = Field(default=None, ge=0)


class BulkDelete(BaseModel):
    """Delete multiple items"""
    item_ids: List[int]
    reason: Optional[str] = None