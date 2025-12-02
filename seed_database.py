#!/usr/bin/env python3
"""
Academy St. Thrift Inventory Database Seed Loader
Loads all reference data and sample items into the inventory database.

FIXED VERSION - Uses correct lowercase table names to match SQLAlchemy models
"""

import sqlite3
import os
from datetime import datetime

DATABASE_PATH = "inventory.db"

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE_PATH)

def clear_all_tables(conn):
    """Clear all existing data from tables (for fresh seed)."""
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    # Disable foreign keys temporarily
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    # Delete all data from each table
    for table in tables:
        table_name = table[0]
        if table_name != 'sqlite_sequence':
            try:
                cursor.execute(f"DELETE FROM {table_name}")
                print(f"✓ Cleared table: {table_name}")
            except Exception as e:
                print(f"✗ Error clearing {table_name}: {e}")
    
    # Re-enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    print("\n" + "="*60)

def seed_departments(conn):
    """Seed the departments table."""
    cursor = conn.cursor()
    departments = [
        (1, 'Women\'s', 1, 1),
        (2, 'Men\'s', 2, 1),
        (3, 'Kids', 3, 1),
        (4, 'Unisex', 4, 1)
    ]
    
    cursor.executemany(
        "INSERT INTO departments (department_id, department_name, sort_order, active) VALUES (?, ?, ?, ?)",
        departments
    )
    conn.commit()
    print(f"✓ Seeded {len(departments)} departments")

def seed_categories(conn):
    """Seed the categories table."""
    cursor = conn.cursor()
    categories = [
        (1, 'Tops', 1, 1, 1),
        (2, 'Bottoms', 1, 2, 1),
        (3, 'Dresses', 1, 3, 1),
        (4, 'Outerwear', 1, 4, 1),
        (5, 'Shoes', 1, 5, 1),
        (6, 'Accessories', 1, 6, 1),
        (7, 'Tops', 2, 1, 1),
        (8, 'Bottoms', 2, 2, 1),
        (9, 'Outerwear', 2, 3, 1),
        (10, 'Shoes', 2, 4, 1),
        (11, 'Accessories', 2, 5, 1),
        (12, 'Tops', 3, 1, 1),
        (13, 'Bottoms', 3, 2, 1),
        (14, 'Dresses', 3, 3, 1),
        (15, 'Outerwear', 3, 4, 1),
        (16, 'Shoes', 3, 5, 1),
        (17, 'Tops', 4, 1, 1),
        (18, 'Bottoms', 4, 2, 1),
        (19, 'Outerwear', 4, 3, 1),
        (20, 'Accessories', 4, 4, 1)
    ]
    
    cursor.executemany(
        "INSERT INTO categories (category_id, category_name, department_id, sort_order, active) VALUES (?, ?, ?, ?, ?)",
        categories
    )
    conn.commit()
    print(f"✓ Seeded {len(categories)} categories")

def seed_item_types(conn):
    """Seed the item_types table."""
    cursor = conn.cursor()
    item_types = [
        # Women's Tops
        (1, 'T-Shirt', 1, 1, 1), (2, 'Blouse', 1, 2, 1), (3, 'Tank Top', 1, 3, 1),
        (4, 'Sweater', 1, 4, 1), (5, 'Cardigan', 1, 5, 1), (6, 'Crop Top', 1, 6, 1),
        # Women's Bottoms
        (7, 'Jeans', 2, 1, 1), (8, 'Skirt', 2, 2, 1), (9, 'Shorts', 2, 3, 1),
        (10, 'Leggings', 2, 4, 1), (11, 'Trousers', 2, 5, 1),
        # Women's Dresses
        (12, 'Maxi Dress', 3, 1, 1), (13, 'Mini Dress', 3, 2, 1), (14, 'Midi Dress', 3, 3, 1),
        (15, 'Sundress', 3, 4, 1), (16, 'Cocktail Dress', 3, 5, 1),
        # Women's Outerwear
        (17, 'Jacket', 4, 1, 1), (18, 'Blazer', 4, 2, 1), (19, 'Coat', 4, 3, 1), (20, 'Vest', 4, 4, 1),
        # Women's Shoes
        (21, 'Boots', 5, 1, 1), (22, 'Sneakers', 5, 2, 1), (23, 'Heels', 5, 3, 1),
        (24, 'Flats', 5, 4, 1), (25, 'Sandals', 5, 5, 1),
        # Women's Accessories
        (26, 'Handbag', 6, 1, 1), (27, 'Backpack', 6, 2, 1), (28, 'Scarf', 6, 3, 1),
        (29, 'Hat', 6, 4, 1), (30, 'Belt', 6, 5, 1),
        # Men's Tops
        (31, 'T-Shirt', 7, 1, 1), (32, 'Button-Up Shirt', 7, 2, 1), (33, 'Polo Shirt', 7, 3, 1),
        (34, 'Sweater', 7, 4, 1), (35, 'Hoodie', 7, 5, 1),
        # Men's Bottoms
        (36, 'Jeans', 8, 1, 1), (37, 'Chinos', 8, 2, 1), (38, 'Shorts', 8, 3, 1), (39, 'Sweatpants', 8, 4, 1),
        # Men's Outerwear
        (40, 'Jacket', 9, 1, 1), (41, 'Blazer', 9, 2, 1), (42, 'Coat', 9, 3, 1), (43, 'Vest', 9, 4, 1),
        # Men's Shoes
        (44, 'Sneakers', 10, 1, 1), (45, 'Boots', 10, 2, 1), (46, 'Dress Shoes', 10, 3, 1), (47, 'Sandals', 10, 4, 1),
        # Men's Accessories
        (48, 'Watch', 11, 1, 1), (49, 'Backpack', 11, 2, 1), (50, 'Hat', 11, 3, 1), (51, 'Belt', 11, 4, 1),
        # Kids Tops
        (52, 'T-Shirt', 12, 1, 1), (53, 'Sweater', 12, 2, 1), (54, 'Hoodie', 12, 3, 1),
        # Kids Bottoms
        (55, 'Jeans', 13, 1, 1), (56, 'Shorts', 13, 2, 1), (57, 'Leggings', 13, 3, 1),
        # Kids Dresses
        (58, 'Dress', 14, 1, 1),
        # Kids Outerwear
        (59, 'Jacket', 15, 1, 1), (60, 'Coat', 15, 2, 1),
        # Kids Shoes
        (61, 'Sneakers', 16, 1, 1), (62, 'Boots', 16, 2, 1), (63, 'Sandals', 16, 3, 1),
        # Unisex Tops
        (64, 'T-Shirt', 17, 1, 1), (65, 'Hoodie', 17, 2, 1), (66, 'Tank Top', 17, 3, 1),
        # Unisex Bottoms
        (67, 'Jeans', 18, 1, 1), (68, 'Joggers', 18, 2, 1), (69, 'Shorts', 18, 3, 1),
        # Unisex Outerwear
        (70, 'Windbreaker', 19, 1, 1), (71, 'Bomber Jacket', 19, 2, 1),
        # Unisex Accessories
        (72, 'Tote Bag', 20, 1, 1), (73, 'Beanie', 20, 2, 1), (74, 'Baseball Cap', 20, 3, 1)
    ]
    
    cursor.executemany(
        "INSERT INTO item_types (item_type_id, item_type_name, category_id, sort_order, active) VALUES (?, ?, ?, ?, ?)",
        item_types
    )
    conn.commit()
    print(f"✓ Seeded {len(item_types)} item types")

def seed_sizes(conn):
    """Seed the sizes table."""
    cursor = conn.cursor()
    sizes = [
        # Letter Sizes
        (1, 'XXS', 'Letter', 1, 'Extra Extra Small'),
        (2, 'XS', 'Letter', 2, 'Extra Small'),
        (3, 'S', 'Letter', 3, 'Small'),
        (4, 'M', 'Letter', 4, 'Medium'),
        (5, 'L', 'Letter', 5, 'Large'),
        (6, 'XL', 'Letter', 6, 'Extra Large'),
        (7, 'XXL', 'Letter', 7, 'Extra Extra Large'),
        (8, 'XXXL', 'Letter', 8, '3XL'),
        # US Numeric Sizes
        (9, '0', 'US Numeric', 10, 'US Size 0'),
        (10, '2', 'US Numeric', 11, 'US Size 2'),
        (11, '4', 'US Numeric', 12, 'US Size 4'),
        (12, '6', 'US Numeric', 13, 'US Size 6'),
        (13, '8', 'US Numeric', 14, 'US Size 8'),
        (14, '10', 'US Numeric', 15, 'US Size 10'),
        (15, '12', 'US Numeric', 16, 'US Size 12'),
        (16, '14', 'US Numeric', 17, 'US Size 14'),
        (17, '16', 'US Numeric', 18, 'US Size 16'),
        (18, '18', 'US Numeric', 19, 'US Size 18'),
        (19, '20', 'US Numeric', 20, 'US Size 20'),
        (20, '22', 'US Numeric', 21, 'US Size 22'),
        (21, '24', 'US Numeric', 22, 'US Size 24'),
        # Waist Sizes
        (22, '26', 'Waist', 30, '26" Waist'),
        (23, '28', 'Waist', 31, '28" Waist'),
        (24, '29', 'Waist', 32, '29" Waist'),
        (25, '30', 'Waist', 33, '30" Waist'),
        (26, '31', 'Waist', 34, '31" Waist'),
        (27, '32', 'Waist', 35, '32" Waist'),
        (28, '33', 'Waist', 36, '33" Waist'),
        (29, '34', 'Waist', 37, '34" Waist'),
        (30, '36', 'Waist', 38, '36" Waist'),
        (31, '38', 'Waist', 39, '38" Waist'),
        (32, '40', 'Waist', 40, '40" Waist'),
        (33, '42', 'Waist', 41, '42" Waist'),
        # Shoe Sizes
        (34, '6', 'Shoes', 50, 'Shoe Size 6'),
        (35, '6.5', 'Shoes', 51, 'Shoe Size 6.5'),
        (36, '7', 'Shoes', 52, 'Shoe Size 7'),
        (37, '7.5', 'Shoes', 53, 'Shoe Size 7.5'),
        (38, '8', 'Shoes', 54, 'Shoe Size 8'),
        (39, '8.5', 'Shoes', 55, 'Shoe Size 8.5'),
        (40, '9', 'Shoes', 56, 'Shoe Size 9'),
        (41, '9.5', 'Shoes', 57, 'Shoe Size 9.5'),
        (42, '10', 'Shoes', 58, 'Shoe Size 10'),
        (43, '10.5', 'Shoes', 59, 'Shoe Size 10.5'),
        (44, '11', 'Shoes', 60, 'Shoe Size 11'),
        (45, '11.5', 'Shoes', 61, 'Shoe Size 11.5'),
        (46, '12', 'Shoes', 62, 'Shoe Size 12'),
        (47, '13', 'Shoes', 63, 'Shoe Size 13'),
        # Universal
        (48, 'One Size', 'Universal', 100, 'One Size Fits Most')
    ]
    
    cursor.executemany(
        "INSERT INTO sizes (size_id, size_value, size_system, sort_order, notes) VALUES (?, ?, ?, ?, ?)",
        sizes
    )
    conn.commit()
    print(f"✓ Seeded {len(sizes)} sizes")

def seed_colors(conn):
    """Seed the colors table."""
    cursor = conn.cursor()
    colors = [
        # Neutrals
        (1, 'Black', 'Neutrals', '#000000', 1),
        (2, 'White', 'Neutrals', '#FFFFFF', 2),
        (3, 'Gray', 'Neutrals', '#808080', 3),
        (4, 'Beige', 'Neutrals', '#F5F5DC', 4),
        (5, 'Cream', 'Neutrals', '#FFFDD0', 5),
        # Blues
        (6, 'Navy', 'Blues', '#000080', 10),
        (7, 'Royal Blue', 'Blues', '#4169E1', 11),
        (8, 'Sky Blue', 'Blues', '#87CEEB', 12),
        (9, 'Teal', 'Blues', '#008080', 13),
        (26, 'Denim Blue', 'Blues', '#1560BD', 14),
        # Reds
        (10, 'Red', 'Reds', '#FF0000', 20),
        (11, 'Burgundy', 'Reds', '#800020', 21),
        # Pinks
        (12, 'Pink', 'Pinks', '#FFC0CB', 30),
        (13, 'Hot Pink', 'Pinks', '#FF69B4', 31),
        (14, 'Blush', 'Pinks', '#FFB6C1', 32),
        # Greens
        (15, 'Forest Green', 'Greens', '#228B22', 40),
        (16, 'Olive', 'Greens', '#808000', 41),
        (17, 'Mint', 'Greens', '#98FF98', 42),
        # Yellows
        (18, 'Yellow', 'Yellows', '#FFFF00', 50),
        (19, 'Mustard', 'Yellows', '#FFDB58', 51),
        # Oranges
        (20, 'Orange', 'Oranges', '#FFA500', 60),
        (21, 'Rust', 'Oranges', '#B7410E', 61),
        # Purples
        (22, 'Purple', 'Purples', '#800080', 70),
        (23, 'Lavender', 'Purples', '#E6E6FA', 71),
        # Browns
        (24, 'Brown', 'Browns', '#A52A2A', 80),
        (25, 'Tan', 'Browns', '#D2B48C', 81),
        # Special
        (27, 'Multicolor', 'Special', None, 100),
        (28, 'Print/Pattern', 'Special', None, 101)
    ]
    
    cursor.executemany(
        "INSERT INTO colors (color_id, color_name, color_family, hex_code, sort_order) VALUES (?, ?, ?, ?, ?)",
        colors
    )
    conn.commit()
    print(f"✓ Seeded {len(colors)} colors")

def seed_tags(conn):
    """Seed the tags table."""
    cursor = conn.cursor()
    tags = [
        # Era Tags
        (1, 'Vintage', 'Era', 'Items from past decades', 1),
        (2, 'Y2K', 'Era', 'Late 90s/Early 2000s style', 1),
        (3, '90s', 'Era', '1990s aesthetic', 1),
        (4, '80s', 'Era', '1980s aesthetic', 1),
        (5, '70s', 'Era', '1970s aesthetic', 1),
        (6, 'Retro', 'Era', 'Vintage-inspired', 1),
        # Style Tags
        (7, 'Boho', 'Style', 'Bohemian style', 1),
        (8, 'Minimalist', 'Style', 'Clean, simple design', 1),
        (9, 'Grunge', 'Style', '90s alternative aesthetic', 1),
        (10, 'Preppy', 'Style', 'Classic, polished look', 1),
        (11, 'Streetwear', 'Style', 'Urban, casual style', 1),
        (12, 'Punk', 'Style', 'Alternative, edgy', 1),
        (13, 'Romantic', 'Style', 'Soft, feminine details', 1),
        (14, 'Sporty', 'Style', 'Athletic-inspired', 1),
        # Feature Tags
        (15, 'Designer', 'Feature', 'High-end brand', 1),
        (16, 'Sustainable', 'Feature', 'Eco-friendly material', 1),
        (17, 'Handmade', 'Feature', 'Artisan crafted', 1),
        (18, 'Rare Find', 'Feature', 'Hard to find item', 1),
        (19, 'Plus Size', 'Feature', 'Extended sizing', 1),
        (20, 'Petite', 'Feature', 'Petite sizing', 1),
        # Occasion Tags
        (21, 'Formal', 'Occasion', 'Dressy events', 1),
        (22, 'Casual', 'Occasion', 'Everyday wear', 1),
        (23, 'Workwear', 'Occasion', 'Professional settings', 1),
        (24, 'Party', 'Occasion', 'Night out/celebrations', 1),
        (25, 'Festival', 'Occasion', 'Music festivals, outdoor events', 1),
        # Pattern Tags
        (26, 'Floral', 'Pattern', 'Floral print', 1),
        (27, 'Striped', 'Pattern', 'Striped pattern', 1),
        (28, 'Plaid', 'Pattern', 'Plaid/checkered', 1),
        (29, 'Solid', 'Pattern', 'Solid color', 1),
        (30, 'Graphic', 'Pattern', 'Graphic print/text', 1)
    ]
    
    cursor.executemany(
        "INSERT INTO tags (tag_id, tag_name, tag_category, description, active) VALUES (?, ?, ?, ?, ?)",
        tags
    )
    conn.commit()
    print(f"✓ Seeded {len(tags)} tags")

def seed_conditions(conn):
    """Seed the conditions table."""
    cursor = conn.cursor()
    conditions = [
        (1, 'Excellent', 'Like new, no visible wear or defects', 1),
        (2, 'Good', 'Gently used, minor signs of wear', 2),
        (3, 'Fair', 'Noticeable wear but still functional and wearable', 3),
        (4, 'Poor', 'Significant wear, may have defects', 4)
    ]
    
    cursor.executemany(
        "INSERT INTO conditions (condition_id, condition_name, description, sort_order) VALUES (?, ?, ?, ?)",
        conditions
    )
    conn.commit()
    print(f"✓ Seeded {len(conditions)} conditions")

def seed_item_status(conn):
    """Seed the item_status table."""
    cursor = conn.cursor()
    statuses = [
        (1, 'Available', 'Ready for sale on the floor', 1, 1),
        (2, 'Sold', 'Item has been purchased', 0, 2),
        (3, 'Processing', 'Being entered/prepared, not ready for sale yet', 0, 3),
        (4, 'On Hold', 'Reserved for a customer', 0, 4),
        (5, 'Removed', 'No longer available (donated, damaged, etc.)', 0, 5)
    ]
    
    cursor.executemany(
        "INSERT INTO item_status (status_id, status_name, description, is_available_for_sale, sort_order) VALUES (?, ?, ?, ?, ?)",
        statuses
    )
    conn.commit()
    print(f"✓ Seeded {len(statuses)} item statuses")

def seed_locations(conn):
    """Seed the locations table."""
    cursor = conn.cursor()
    locations = [
        (1, 'Sales Floor - Rack A', 'Sales Floor', 'Main women\'s section, rack A', 1),
        (2, 'Sales Floor - Rack B', 'Sales Floor', 'Main women\'s section, rack B', 1),
        (3, 'Sales Floor - Rack C', 'Sales Floor', 'Men\'s section, rack C', 1),
        (4, 'Sales Floor - Rack D', 'Sales Floor', 'Men\'s section, rack D', 1),
        (5, 'Sales Floor - Shoe Display', 'Sales Floor', 'Shoe display area', 1),
        (6, 'Sales Floor - Accessories Wall', 'Sales Floor', 'Accessories and bags wall', 1),
        (7, 'Back Room - Bin 1', 'Storage', 'Back room storage bin 1', 1),
        (8, 'Back Room - Bin 2', 'Storage', 'Back room storage bin 2', 1),
        (9, 'Back Room - Bin 3', 'Storage', 'Back room storage bin 3', 1),
        (10, 'Processing Area', 'Processing', 'Area for intake and item processing', 1),
        (11, 'Clearance Section', 'Sales Floor', 'Discounted items section', 1),
        (12, 'Window Display', 'Sales Floor', 'Front window display area', 1)
    ]
    
    cursor.executemany(
        "INSERT INTO locations (location_id, location_name, location_type, description, active) VALUES (?, ?, ?, ?, ?)",
        locations
    )
    conn.commit()
    print(f"✓ Seeded {len(locations)} locations")

def seed_items(conn):
    """Seed sample items."""
    cursor = conn.cursor()
    
    items = [
        (1, 1, 1, 1, 'Urban Outfitters', 3, 2, None, 'Cotton', 1, 1, 1, 18.00, None, 0, None, 
         'Vintage white graphic tee with retro band logo, soft and comfortable', None, 'Perfect vintage find!', 'All Season', '2024-01-15', None),
        (2, 1, 2, 7, 'Levi\'s', 27, 26, None, 'Denim', 2, 1, 1, 45.00, None, 0, None, 
         'Classic 501 high-waisted jeans in perfect condition, authentic vintage fit', None, 'Iconic Levi\'s 501s', 'All Season', '2024-01-16', None),
        (3, 1, 3, 12, 'Free People', 13, 26, None, 'Cotton Blend', 1, 1, 2, 65.00, None, 0, None, 
         'Flowy bohemian maxi dress with beautiful floral details, ethereal and romantic', None, 'Boho dream dress', 'Spring/Summer', '2024-01-17', None),
        (4, 2, 7, 32, 'Brooks Brothers', 5, 6, None, 'Cotton', 1, 1, 3, 28.00, None, 0, None, 
         'Crisp navy button-up shirt, perfect for work or formal occasions', None, 'Professional essential', 'All Season', '2024-01-18', None),
        (5, 1, 5, 21, 'Dr. Martens', 38, 1, None, 'Leather', 2, 1, 5, 85.00, None, 0, None, 
         'Classic black Dr. Martens combat boots, gently worn with plenty of life left', 'Minor scuffs on toe', 'Timeless combat boots', 'All Season', '2024-01-19', None),
        (6, 1, 1, 4, 'Gap', 4, 24, None, 'Wool Blend', 1, 1, 1, 32.00, None, 0, None, 
         'Cozy brown knit sweater, perfect fall essential with classic styling', None, 'Warm and comfortable', 'Fall/Winter', '2024-01-20', None),
        (7, 2, 8, 36, 'Wrangler', 27, 26, None, 'Denim', 2, 1, 3, 38.00, None, 0, None, 
         'Vintage Wrangler denim jeans with authentic wear and character', None, 'Authentic vintage denim', 'All Season', '2024-01-21', None),
        (8, 1, 6, 26, 'Coach', 48, 24, None, 'Leather', 1, 1, 6, 125.00, None, 0, None, 
         'Vintage Coach leather handbag in mint condition, timeless design', None, 'Rare vintage Coach find!', 'All Season', '2024-01-22', None),
        (9, 4, 17, 64, 'Nike', 5, 1, None, 'Cotton', 2, 1, 3, 15.00, None, 0, None, 
         'Classic black Nike tee with iconic swoosh, athletic fit', None, 'Athletic essential', 'All Season', '2024-01-23', None),
        (10, 1, 1, 2, 'Anthropologie', 12, 13, None, 'Silk', 1, 1, 2, 48.00, None, 0, None, 
         'Romantic blush pink blouse with delicate ruffle details, elegant and feminine', None, 'Romantic and elegant', 'Spring/Summer', '2024-01-24', None),
        (11, 2, 9, 40, 'Carhartt', 6, 24, None, 'Canvas', 2, 1, 4, 55.00, None, 0, None, 
         'Rugged brown Carhartt work jacket, authentic vintage with character', 'Minor wear on elbows', 'Iconic workwear piece', 'Fall/Winter', '2024-01-25', None),
        (12, 1, 2, 8, 'American Apparel', 11, 1, None, 'Cotton', 1, 1, 1, 22.00, None, 0, None, 
         'High-waisted black mini skirt, versatile and stylish', None, 'Y2K vibes', 'All Season', '2024-01-26', None),
        (13, 1, 3, 16, 'Reformation', 13, 10, None, 'Polyester', 1, 1, 2, 78.00, None, 0, None, 
         'Stunning red cocktail dress perfect for special events, sustainable brand', None, 'Show-stopping dress', 'All Season', '2024-01-27', None),
        (14, 2, 10, 44, 'Converse', 42, 2, None, 'Canvas', 2, 1, 5, 35.00, None, 0, None, 
         'Classic white Chuck Taylor All Stars, vintage condition with character', 'Some yellowing on soles', 'Iconic Converse', 'All Season', '2024-01-28', None),
        (15, 1, 4, 18, 'Banana Republic', 12, 1, None, 'Wool', 1, 1, 2, 68.00, None, 0, None, 
         'Professional black blazer with perfect tailoring, work wardrobe staple', None, 'Perfect professional piece', 'All Season', '2024-01-29', None),
        (16, 1, 1, 6, 'Brandy Melville', 2, 12, None, 'Cotton', 1, 1, 1, 16.00, None, 0, None, 
         'Y2K pink crop top with butterfly print, super trendy and cute', None, 'Y2K aesthetic', 'Spring/Summer', '2024-01-30', None),
        (17, 2, 7, 35, 'Champion', 5, 3, None, 'Cotton Blend', 2, 1, 3, 32.00, None, 0, None, 
         'Vintage gray Champion hoodie, authentic reverse weave construction', None, 'Authentic vintage Champion', 'Fall/Winter', '2024-01-31', None),
        (18, 1, 2, 7, 'Madewell', 26, 26, None, 'Denim', 1, 1, 1, 52.00, None, 0, None, 
         'High-rise skinny jeans in dark wash, modern fit with stretch', None, 'Perfect everyday jeans', 'All Season', '2024-02-01', None),
        (19, 4, 20, 72, 'Baggu', 48, 27, None, 'Nylon', 1, 1, 6, 12.00, None, 0, None, 
         'Colorful reusable tote bag, eco-friendly and practical', None, 'Sustainable shopping', 'All Season', '2024-02-02', None),
        (20, 1, 5, 23, 'Steve Madden', 37, 1, None, 'Faux Leather', 2, 1, 5, 38.00, None, 0, None, 
         'Black strappy heels, barely worn and perfect for parties', None, 'Party-ready heels', 'All Season', '2024-02-03', None),
        (21, 1, 3, 15, 'Zara', 12, 18, None, 'Cotton', 1, 1, 2, 42.00, None, 0, None, 
         'Sunny yellow sundress, perfect for summer days and vacations', None, 'Cheerful summer dress', 'Spring/Summer', '2024-02-04', None),
        (22, 2, 8, 37, 'Dockers', 28, 4, None, 'Chino', 2, 1, 3, 28.00, None, 0, None, 
         'Khaki chinos suitable for casual or work settings, classic fit', None, 'Versatile chinos', 'All Season', '2024-02-05', None),
        (23, 1, 1, 5, 'J.Crew', 13, 6, None, 'Cashmere', 1, 1, 1, 58.00, None, 0, None, 
         'Luxurious navy cashmere cardigan, incredibly soft and warm', None, 'Luxury cashmere', 'Fall/Winter', '2024-02-06', None),
        (24, 2, 11, 48, 'Timex', 48, 1, None, 'Metal', 1, 1, 6, 45.00, None, 0, None, 
         'Classic vintage Timex watch with leather strap, fully functional', None, 'Vintage timepiece', 'All Season', '2024-02-07', None),
        (25, 3, 12, 52, 'Old Navy', 14, 10, None, 'Cotton', 2, 1, 7, 8.00, None, 0, None, 
         'Kids red graphic tee with fun print, good condition', None, 'Fun kids tee', 'All Season', '2024-02-08', None),
        (26, 1, 2, 10, 'Lululemon', 11, 1, None, 'Spandex', 1, 1, 1, 48.00, None, 0, None, 
         'Black high-waisted Lululemon leggings, perfect for activewear or athleisure', None, 'Premium activewear', 'All Season', '2024-02-09', None),
        (27, 1, 6, 28, 'Burberry', 48, 27, None, 'Silk', 1, 1, 6, 95.00, None, 0, None, 
         'Authentic Burberry plaid scarf, designer vintage piece in excellent condition', None, 'Designer vintage scarf', 'Fall/Winter', '2024-02-10', None),
        (28, 2, 7, 33, 'Lacoste', 5, 2, None, 'Pique', 2, 1, 3, 32.00, None, 0, None, 
         'Classic white Lacoste polo shirt with iconic crocodile logo, preppy style', 'Minor fading', 'Preppy classic', 'Spring/Summer', '2024-02-11', None),
        (29, 1, 4, 17, 'The North Face', 13, 10, None, 'Nylon', 1, 1, 2, 72.00, None, 0, None, 
         'Red North Face puffer jacket, warm and stylish for winter', None, 'Warm winter essential', 'Fall/Winter', '2024-02-12', None),
        (30, 1, 5, 24, 'Birkenstock', 38, 24, None, 'Leather', 2, 1, 5, 55.00, None, 0, None, 
         'Brown leather Birkenstock sandals, comfortable and classic', 'Footbed shows wear', 'Comfort classic', 'Spring/Summer', '2024-02-13', None),
        (31, 4, 18, 67, 'Dickies', 28, 1, None, 'Cotton', 1, 1, 4, 38.00, None, 0, None, 
         'Black Dickies work pants, durable and stylish streetwear staple', None, 'Streetwear essential', 'All Season', '2024-02-14', None),
        (32, 1, 1, 3, 'American Eagle', 3, 2, None, 'Cotton', 2, 1, 1, 12.00, None, 0, None, 
         'White ribbed tank top, basic wardrobe essential', None, 'Basic essential', 'Spring/Summer', '2024-02-15', None),
        (33, 2, 8, 38, 'Adidas', 5, 1, None, 'Polyester', 1, 1, 3, 35.00, None, 0, None, 
         'Black Adidas track pants with signature three stripes', None, 'Athletic classic', 'All Season', '2024-02-16', None),
        (34, 1, 3, 13, 'H&M', 11, 22, None, 'Polyester', 1, 1, 2, 28.00, None, 0, None, 
         'Purple mini dress perfect for parties and nights out', None, 'Party dress', 'All Season', '2024-02-17', None),
        (35, 1, 6, 29, 'Goorin Bros', 48, 1, None, 'Wool', 2, 1, 6, 32.00, None, 0, None, 
         'Vintage black fedora hat with classic styling', None, 'Vintage accessory', 'Fall/Winter', '2024-02-18', None),
        (36, 2, 10, 45, 'Red Wing', 43, 24, None, 'Leather', 2, 1, 5, 128.00, None, 0, None, 
         'Classic Red Wing brown work boots, built to last generations', 'Some wear on leather', 'Heritage workwear', 'All Season', '2024-02-19', None),
        (37, 1, 2, 9, 'Forever 21', 10, 26, None, 'Denim', 1, 1, 1, 18.00, None, 0, None, 
         'Denim shorts perfect for summer, comfortable fit', None, 'Summer staple', 'Spring/Summer', '2024-02-20', None),
        (38, 1, 1, 4, 'Uniqlo', 4, 3, None, 'Merino Wool', 1, 1, 1, 42.00, None, 0, None, 
         'Gray minimalist merino wool sweater, quality basics at their best', None, 'Quality minimalist piece', 'Fall/Winter', '2024-02-21', None),
        (39, 2, 9, 41, 'Hugo Boss', 6, 1, None, 'Wool Blend', 1, 1, 4, 98.00, None, 0, None, 
         'Designer black Hugo Boss blazer with sharp tailoring', None, 'Designer tailoring', 'All Season', '2024-02-22', None),
        (40, 4, 19, 70, 'Patagonia', 5, 6, None, 'Nylon', 2, 1, 4, 58.00, None, 0, None, 
         'Navy Patagonia windbreaker, outdoor adventure essential', None, 'Sustainable outdoor gear', 'Spring/Summer', '2024-02-23', None),
        (41, 1, 5, 25, 'Teva', 39, 1, None, 'Synthetic', 2, 1, 5, 32.00, None, 0, None, 
         'Black Teva sport sandals, ready for any adventure', 'Minor wear on straps', 'Adventure ready', 'Spring/Summer', '2024-02-24', None),
        (42, 1, 3, 14, 'Everlane', 13, 1, None, 'Silk', 1, 1, 2, 68.00, None, 0, None, 
         'Elegant black Everlane midi dress from sustainable brand', None, 'Sustainable elegance', 'All Season', '2024-02-25', None),
        (43, 2, 7, 31, 'Hanes', 5, 2, None, 'Cotton', 2, 1, 7, 10.00, None, 0, None, 
         'Pack of white basic Hanes tees, wardrobe essentials', None, 'Basic essentials', 'All Season', '2024-02-26', None),
        (44, 1, 4, 20, 'Mango', 12, 4, None, 'Polyester', 1, 1, 2, 52.00, None, 0, None, 
         'Beige utility vest, trendy layering piece for any outfit', None, 'Trendy layering piece', 'Spring/Summer', '2024-02-27', None),
        (45, 3, 14, 58, 'Gap Kids', 13, 12, None, 'Cotton', 2, 1, 7, 15.00, None, 0, None, 
         'Pink kids dress with fun polka dot pattern', 'Minor fading', 'Cute kids dress', 'Spring/Summer', '2024-02-28', None),
        (46, 1, 6, 30, 'Fossil', 48, 1, None, 'Leather', 1, 1, 6, 42.00, None, 0, None, 
         'Black leather Fossil belt, classic accessory for any wardrobe', None, 'Classic accessory', 'All Season', '2024-03-01', None),
        (47, 2, 8, 39, 'Russell Athletic', 6, 3, None, 'Cotton Blend', 2, 1, 7, 24.00, None, 0, None, 
         'Gray Russell Athletic sweatpants, cozy loungewear', None, 'Comfortable loungewear', 'Fall/Winter', '2024-03-02', None),
        (48, 1, 1, 2, 'Express', 12, 7, None, 'Chiffon', 1, 1, 1, 38.00, None, 0, None, 
         'Royal blue dressy blouse perfect for work or special occasions', None, 'Professional blouse', 'All Season', '2024-03-03', None),
        (49, 4, 20, 73, 'Carhartt', 48, 24, None, 'Acrylic', 2, 1, 6, 18.00, None, 0, None, 
         'Brown knit Carhartt beanie, winter warmth essential', None, 'Winter essential', 'Fall/Winter', '2024-03-04', None),
        (50, 1, 2, 11, 'Eileen Fisher', 16, 1, None, 'Linen', 1, 1, 1, 58.00, None, 0, None, 
         'Black wide-leg linen trousers, elegant comfort from sustainable brand', None, 'Sustainable comfort', 'Spring/Summer', '2024-03-05', None),
    ]
    
    cursor.executemany("""
        INSERT INTO items (
            item_id, department_id, category_id, item_type_id, brand, size_id, 
            color_primary_id, color_secondary_id, material, condition_id, status_id, 
            current_location_id, price, original_price, on_sale, sale_price, 
            description, internal_notes, customer_notes, season, date_added, date_sold
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, items)
    conn.commit()
    print(f"✓ Seeded {len(items)} sample items")

def seed_item_tags(conn):
    """Seed the item_tags junction table."""
    cursor = conn.cursor()
    
    item_tags = [
        (1, 1), (1, 2), (1, 30), (2, 1), (2, 22), (3, 7), (3, 26), (3, 22),
        (4, 10), (4, 23), (4, 29), (5, 9), (5, 22), (5, 18), (6, 22), (6, 29),
        (7, 1), (7, 22), (8, 1), (8, 15), (8, 18), (9, 14), (9, 22), (9, 29),
        (10, 13), (10, 23), (11, 1), (11, 23), (11, 18), (12, 2), (12, 22), (12, 29),
        (13, 21), (13, 24), (13, 16), (14, 1), (14, 22), (15, 23), (15, 10), (15, 29),
        (16, 2), (16, 22), (16, 30), (17, 1), (17, 14), (17, 29), (18, 22), (18, 29),
        (19, 16), (19, 22), (20, 21), (20, 24), (21, 22), (21, 26), (22, 22), (22, 23),
        (23, 23), (23, 10), (23, 29), (24, 1), (24, 18), (25, 22), (25, 30),
        (26, 14), (26, 22), (26, 29), (27, 1), (27, 15), (27, 18), (27, 28),
        (28, 10), (28, 22), (28, 29), (29, 14), (29, 22), (30, 1), (30, 22),
        (31, 11), (31, 22), (31, 29), (32, 22), (32, 29), (33, 14), (33, 22), (33, 27),
        (34, 24), (34, 21), (35, 1), (35, 18), (36, 1), (36, 23), (36, 18), (37, 22),
        (38, 8), (38, 22), (38, 29), (39, 15), (39, 23), (39, 10), (40, 14), (40, 16), (40, 22),
        (41, 14), (41, 22), (42, 16), (42, 21), (42, 8), (43, 22), (43, 29),
        (44, 22), (44, 11), (45, 22), (45, 26), (46, 22), (46, 23), (47, 22), (47, 14),
        (48, 23), (48, 21), (49, 22), (50, 16), (50, 23), (50, 8),
    ]
    
    cursor.executemany(
        "INSERT INTO item_tags (item_id, tag_id) VALUES (?, ?)",
        item_tags
    )
    conn.commit()
    print(f"✓ Seeded {len(item_tags)} item-tag relationships")

def seed_item_photos(conn):
    """Seed sample item_photos for the first 10 items."""
    cursor = conn.cursor()
    
    photos = [
        (1, 1, '/images/items/item1_front.jpg', 1, 1, '2024-01-15 10:00:00'),
        (2, 1, '/images/items/item1_back.jpg', 0, 2, '2024-01-15 10:01:00'),
        (3, 1, '/images/items/item1_detail.jpg', 0, 3, '2024-01-15 10:02:00'),
        (4, 2, '/images/items/item2_front.jpg', 1, 1, '2024-01-16 10:00:00'),
        (5, 2, '/images/items/item2_back.jpg', 0, 2, '2024-01-16 10:01:00'),
        (6, 3, '/images/items/item3_front.jpg', 1, 1, '2024-01-17 10:00:00'),
        (7, 3, '/images/items/item3_detail.jpg', 0, 2, '2024-01-17 10:01:00'),
        (8, 4, '/images/items/item4_front.jpg', 1, 1, '2024-01-18 10:00:00'),
        (9, 5, '/images/items/item5_pair.jpg', 1, 1, '2024-01-19 10:00:00'),
        (10, 5, '/images/items/item5_side.jpg', 0, 2, '2024-01-19 10:01:00'),
        (11, 5, '/images/items/item5_sole.jpg', 0, 3, '2024-01-19 10:02:00'),
        (12, 5, '/images/items/item5_tag.jpg', 0, 4, '2024-01-19 10:03:00'),
        (13, 6, '/images/items/item6_front.jpg', 1, 1, '2024-01-20 10:00:00'),
        (14, 7, '/images/items/item7_front.jpg', 1, 1, '2024-01-21 10:00:00'),
        (15, 7, '/images/items/item7_label.jpg', 0, 2, '2024-01-21 10:01:00'),
        (16, 8, '/images/items/item8_front.jpg', 1, 1, '2024-01-22 10:00:00'),
        (17, 8, '/images/items/item8_interior.jpg', 0, 2, '2024-01-22 10:01:00'),
        (18, 8, '/images/items/item8_logo.jpg', 0, 3, '2024-01-22 10:02:00'),
        (19, 9, '/images/items/item9_front.jpg', 1, 1, '2024-01-23 10:00:00'),
        (20, 10, '/images/items/item10_front.jpg', 1, 1, '2024-01-24 10:00:00'),
        (21, 10, '/images/items/item10_detail.jpg', 0, 2, '2024-01-24 10:01:00'),
    ]
    
    cursor.executemany(
        "INSERT INTO item_photos (photo_id, item_id, file_path, is_primary, sort_order, uploaded_date) VALUES (?, ?, ?, ?, ?, ?)",
        photos
    )
    conn.commit()
    print(f"✓ Seeded {len(photos)} item photos")

def seed_item_history(conn):
    """Seed sample item_history for a few items."""
    cursor = conn.cursor()
    
    # Updated to match SQLAlchemy model columns:
    # history_id, item_id, action, action_date, old_value, new_value, notes
    history = [
        (1, 1, 'created', '2024-01-15 10:00:00', None, None, 'Item added to inventory'),
        (2, 1, 'status_change', '2024-01-15 10:05:00', 'Processing', 'Available', 'Item status changed to Processing'),
        (3, 1, 'status_change', '2024-01-15 11:00:00', 'Processing', 'Available', 'Item status changed to Available'),
        (4, 2, 'created', '2024-01-16 10:00:00', None, None, 'Item added to inventory'),
        (5, 2, 'status_change', '2024-01-16 10:30:00', 'Processing', 'Available', 'Item status changed to Available'),
        (6, 8, 'created', '2024-01-22 10:00:00', None, None, 'Vintage Coach bag received'),
        (7, 8, 'price_change', '2024-01-22 14:00:00', '150.00', '125.00', 'Price adjusted from $150 to $125'),
        (8, 8, 'status_change', '2024-01-22 15:00:00', 'Processing', 'Available', 'Item status changed to Available'),
    ]
    
    cursor.executemany(
        "INSERT INTO item_history (history_id, item_id, action, action_date, old_value, new_value, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        history
    )
    conn.commit()
    print(f"✓ Seeded {len(history)} history records")

def main():
    """Main function to seed the database."""
    print("\n" + "="*60)
    print("Academy St. Thrift Inventory - Database Seed Loader")
    print("="*60 + "\n")
    
    if not os.path.exists(DATABASE_PATH):
        print(f"⚠️  Warning: Database file '{DATABASE_PATH}' not found!")
        print("Please run your FastAPI application first to create the database schema.")
        return
    
    try:
        conn = connect_db()
        
        # Automatically clear existing data
        print("Clearing existing data...")
        clear_all_tables(conn)
        
        print("\n📦 Seeding Reference Tables...")
        print("-" * 60)
        seed_departments(conn)
        seed_categories(conn)
        seed_item_types(conn)
        seed_sizes(conn)
        seed_colors(conn)
        seed_tags(conn)
        seed_conditions(conn)
        seed_item_status(conn)
        seed_locations(conn)
        
        print("\n📦 Seeding Main Data...")
        print("-" * 60)
        seed_items(conn)
        seed_item_tags(conn)
        
        print("\n📦 Seeding Supporting Data...")
        print("-" * 60)
        seed_item_photos(conn)
        seed_item_history(conn)
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ Database seeding completed successfully!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • 4 Departments")
        print(f"   • 20 Categories")
        print(f"   • 74 Item Types")
        print(f"   • 48 Sizes")
        print(f"   • 28 Colors")
        print(f"   • 30 Tags")
        print(f"   • 4 Conditions")
        print(f"   • 5 Item Statuses")
        print(f"   • 12 Locations")
        print(f"   • 50 Sample Items")
        print(f"   • Item Tags, Photos, and History\n")
        
        print("🚀 Your database is now ready to use!")
        print("   Run your FastAPI app: python main.py")
        print("   Visit: http://localhost:8000/docs\n")
        
    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

