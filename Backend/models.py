from datetime import datetime
from typing import Optional, List
from sqlalchemy import Boolean, Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


item_tags = Table(
    'item_tags',
    Base.metadata,
    Column('item_id', Integer, ForeignKey('items.item_id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.tag_id', ondelete='CASCADE'), primary_key=True)
)


class Department(Base):
    __tablename__ = 'departments'
    
    department_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    department_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    categories: Mapped[List["Category"]] = relationship("Category", back_populates="department")
    items: Mapped[List["Item"]] = relationship("Item", back_populates="department")


class Category(Base):
    __tablename__ = 'categories'
    
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String, nullable=False)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.department_id'), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    department: Mapped["Department"] = relationship("Department", back_populates="categories")
    item_types: Mapped[List["ItemType"]] = relationship("ItemType", back_populates="category")
    items: Mapped[List["Item"]] = relationship("Item", back_populates="category")


class ItemType(Base):
    __tablename__ = 'item_types'
    
    item_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_type_name: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.category_id'), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    category: Mapped["Category"] = relationship("Category", back_populates="item_types")
    items: Mapped[List["Item"]] = relationship("Item", back_populates="item_type")


class Size(Base):
    __tablename__ = 'sizes'
    
    size_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    size_value: Mapped[str] = mapped_column(String, nullable=False)
    size_system: Mapped[str] = mapped_column(String, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    items: Mapped[List["Item"]] = relationship("Item", back_populates="size")


class Color(Base):
    __tablename__ = 'colors'
    
    color_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    color_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    color_family: Mapped[str] = mapped_column(String, nullable=False)
    hex_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    
    items_primary: Mapped[List["Item"]] = relationship(
        "Item", foreign_keys="Item.color_primary_id", back_populates="color_primary"
    )
    items_secondary: Mapped[List["Item"]] = relationship(
        "Item", foreign_keys="Item.color_secondary_id", back_populates="color_secondary"
    )


class Tag(Base):
    __tablename__ = 'tags'
    
    tag_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tag_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    tag_category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    items: Mapped[List["Item"]] = relationship("Item", secondary=item_tags, back_populates="tags")


class Condition(Base):
    __tablename__ = 'conditions'
    
    condition_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    condition_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    
    items: Mapped[List["Item"]] = relationship("Item", back_populates="condition")


class ItemStatus(Base):
    __tablename__ = 'item_status'
    
    status_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_available_for_sale: Mapped[bool] = mapped_column(Boolean, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    
    items: Mapped[List["Item"]] = relationship("Item", back_populates="status")


class Location(Base):
    __tablename__ = 'locations'
    
    location_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    location_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    items: Mapped[List["Item"]] = relationship("Item", back_populates="current_location")


class Item(Base):
    __tablename__ = 'items'
    
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.department_id'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.category_id'), nullable=False)
    item_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('item_types.item_type_id'), nullable=False)
    brand: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    size_id: Mapped[int] = mapped_column(Integer, ForeignKey('sizes.size_id'), nullable=False)
    color_primary_id: Mapped[int] = mapped_column(Integer, ForeignKey('colors.color_id'), nullable=False)
    color_secondary_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('colors.color_id'), nullable=True)
    material: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    condition_id: Mapped[int] = mapped_column(Integer, ForeignKey('conditions.condition_id'), nullable=False)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey('item_status.status_id'), nullable=False)
    current_location_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('locations.location_id'), nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    original_price: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    on_sale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sale_price: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    internal_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    customer_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    season: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_added: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    date_sold: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    department: Mapped["Department"] = relationship("Department", back_populates="items")
    category: Mapped["Category"] = relationship("Category", back_populates="items")
    item_type: Mapped["ItemType"] = relationship("ItemType", back_populates="items")
    size: Mapped["Size"] = relationship("Size", back_populates="items")
    color_primary: Mapped["Color"] = relationship("Color", foreign_keys=[color_primary_id], back_populates="items_primary")
    color_secondary: Mapped[Optional["Color"]] = relationship("Color", foreign_keys=[color_secondary_id], back_populates="items_secondary")
    condition: Mapped["Condition"] = relationship("Condition", back_populates="items")
    status: Mapped["ItemStatus"] = relationship("ItemStatus", back_populates="items")
    current_location: Mapped[Optional["Location"]] = relationship("Location", back_populates="items")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=item_tags, back_populates="items")
    photos: Mapped[List["ItemPhoto"]] = relationship("ItemPhoto", back_populates="item", cascade="all, delete-orphan")
    history: Mapped[List["ItemHistory"]] = relationship("ItemHistory", back_populates="item", cascade="all, delete-orphan")


class ItemPhoto(Base):
    __tablename__ = 'item_photos'
    
    photo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('items.item_id', ondelete='CASCADE'), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    uploaded_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    
    item: Mapped["Item"] = relationship("Item", back_populates="photos")


class ItemHistory(Base):
    __tablename__ = 'item_history'
    
    history_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey('items.item_id', ondelete='CASCADE'), nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    action_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    old_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    item: Mapped["Item"] = relationship("Item", back_populates="history")
