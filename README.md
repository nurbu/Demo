# Academy St. Thrift Inventory API

A complete FastAPI-based inventory management system for a thrift store.

## 📁 Project Structure

```
inventory-api/
├── main.py                 # FastAPI application entry point
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic schemas for validation
├── database.py            # Database configuration and session management
├── crud.py                # CRUD operations for all models
├── routes_items.py        # API routes for items
├── routes_reference.py    # API routes for reference tables
├── requirements.txt       # Python dependencies
└── inventory.db          # SQLite database (created automatically)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Database

The application uses SQLite by default. The database file `inventory.db` will be created automatically in the project root when you first run the application.

### Database Schema

**13 Tables:**
- **Reference Tables**: Departments, Categories, Item_Types, Sizes, Colors, Tags, Conditions, Item_Status
- **Main Tables**: Items, Locations
- **Junction Tables**: item_tags (Items ↔ Tags)
- **Supporting Tables**: Item_Photos, Item_History

### Environment Variables

You can override the database URL with an environment variable:

```bash
export DATABASE_URL="sqlite:///./inventory.db"
```

## 🛣️ API Endpoints

### Health Check
- `GET /` - API information
- `GET /health` - Health check

### Items
- `GET /items/` - List all items (with filtering, searching, pagination)
- `POST /items/` - Create a new item
- `GET /items/{item_id}` - Get item by ID
- `PATCH /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item
- `GET /items/{item_id}/photos` - Get item photos
- `POST /items/{item_id}/photos` - Add photo to item
- `GET /items/{item_id}/history` - Get item history
- `POST /items/bulk/update-status` - Bulk update status
- `POST /items/bulk/update-location` - Bulk update location
- `POST /items/bulk/update-price` - Bulk update prices
- `POST /items/bulk/delete` - Bulk delete items

### Reference Tables
Each reference table has standard CRUD endpoints:
- `GET /{resource}/` - List all
- `POST /{resource}/` - Create new
- `GET /{resource}/{id}` - Get by ID
- `PATCH /{resource}/{id}` - Update
- `DELETE /{resource}/{id}` - Delete

Resources:
- `/departments`
- `/categories`
- `/item-types`
- `/sizes`
- `/colors`
- `/tags`
- `/conditions`
- `/item-statuses`
- `/locations`

## 📝 Example Usage

### Create a New Item

```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "department_id": 1,
    "category_id": 1,
    "item_type_id": 1,
    "brand": "Nike",
    "size_id": 4,
    "color_primary_id": 1,
    "condition_id": 1,
    "status_id": 1,
    "price": 29.99,
    "description": "Vintage Nike T-Shirt",
    "tag_ids": [1, 5, 12]
  }'
```

### Get Items with Filtering

```bash
# Get all items in Women's department, size Medium, on sale
curl "http://localhost:8000/items/?department_id=1&size_id=4&on_sale=true&page=1&page_size=20"
```

### Search Items

```bash
# Search for "Nike" in description, brand, or customer notes
curl "http://localhost:8000/items/?search=Nike"
```

### Bulk Update Status

```bash
curl -X POST "http://localhost:8000/items/bulk/update-status" \
  -H "Content-Type: application/json" \
  -d '{
    "item_ids": [1, 2, 3],
    "status_id": 2,
    "notes": "Items sold at sale event"
  }'
```

## 🔍 Advanced Filtering

The `/items/` endpoint supports comprehensive filtering:

- **department_id, category_id, item_type_id** - Filter by hierarchy
- **brand** - Search by brand (case-insensitive)
- **size_id, color_primary_id** - Filter by size/color
- **condition_id, status_id** - Filter by condition/status
- **location_id** - Filter by location
- **min_price, max_price** - Price range filtering
- **on_sale** - Filter sale items
- **season** - Filter by season
- **tag_ids** - Filter by tags (items with any of these tags)
- **search** - Full-text search in description, brand, customer notes
- **page, page_size** - Pagination (default: page=1, page_size=20)
- **sort_by, sort_order** - Sorting (e.g., sort_by=price, sort_order=asc)

## 🗄️ Database Management

### Initialize Database

The database is automatically initialized when the app starts. To manually reset:

```python
from database import reset_db
reset_db()  # ⚠️ WARNING: This deletes all data!
```

### Using Database Session

In your own scripts:

```python
from database import DatabaseSession
from models import Item

with DatabaseSession() as db:
    items = db.query(Item).all()
    for item in items:
        print(item.description)
```

## 🛠️ Development

### Running Tests

(You'll need to add your own tests)

```bash
pytest
```

### Code Style

```bash
# Format code
black .

# Lint
flake8 .
```

## 🔐 Production Deployment

1. **Set environment variables:**
   ```bash
   export DATABASE_URL="your-production-database-url"
   ```

2. **Update CORS settings** in `main.py`:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

3. **Run with production server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

4. **Use a production database** (PostgreSQL recommended):
   ```bash
   pip install psycopg2-binary
   export DATABASE_URL="postgresql://user:password@localhost/dbname"
   ```

## 📚 Key Features

- ✅ Complete CRUD operations for all models
- ✅ Advanced filtering and searching
- ✅ Pagination support
- ✅ Automatic history tracking
- ✅ Bulk operations
- ✅ Foreign key constraints
- ✅ Cascade deletes for related data
- ✅ Comprehensive API documentation
- ✅ Error handling with detailed messages
- ✅ CORS support for frontend integration

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License
