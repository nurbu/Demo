#!/usr/bin/env python3
"""Seeds the inventory database with reference data and sample items."""

import sqlite3
import os

DATABASE_PATH = "inventory.db"


def connect_db():
    return sqlite3.connect(DATABASE_PATH)


def clear_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    cursor.execute("PRAGMA foreign_keys = OFF")
    for (table_name,) in tables:
        if table_name != 'sqlite_sequence':
            cursor.execute(f"DELETE FROM {table_name}")
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()


def seed_departments(conn):
    data = [
        (1, "Women's", 1, 1), (2, "Men's", 2, 1),
        (3, 'Kids', 3, 1), (4, 'Unisex', 4, 1)
    ]
    conn.executemany(
        "INSERT INTO departments (department_id, department_name, sort_order, active) VALUES (?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_categories(conn):
    data = [
        (1, 'Tops', 1, 1, 1), (2, 'Bottoms', 1, 2, 1), (3, 'Dresses', 1, 3, 1),
        (4, 'Outerwear', 1, 4, 1), (5, 'Shoes', 1, 5, 1), (6, 'Accessories', 1, 6, 1),
        (7, 'Tops', 2, 1, 1), (8, 'Bottoms', 2, 2, 1), (9, 'Outerwear', 2, 3, 1),
        (10, 'Shoes', 2, 4, 1), (11, 'Accessories', 2, 5, 1),
        (12, 'Tops', 3, 1, 1), (13, 'Bottoms', 3, 2, 1), (14, 'Dresses', 3, 3, 1),
        (15, 'Outerwear', 3, 4, 1), (16, 'Shoes', 3, 5, 1),
        (17, 'Tops', 4, 1, 1), (18, 'Bottoms', 4, 2, 1), (19, 'Outerwear', 4, 3, 1),
        (20, 'Accessories', 4, 4, 1)
    ]
    conn.executemany(
        "INSERT INTO categories (category_id, category_name, department_id, sort_order, active) VALUES (?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_item_types(conn):
    data = [
        (1, 'T-Shirt', 1, 1, 1), (2, 'Blouse', 1, 2, 1), (3, 'Tank Top', 1, 3, 1),
        (4, 'Sweater', 1, 4, 1), (5, 'Cardigan', 1, 5, 1), (6, 'Crop Top', 1, 6, 1),
        (7, 'Jeans', 2, 1, 1), (8, 'Skirt', 2, 2, 1), (9, 'Shorts', 2, 3, 1),
        (10, 'Leggings', 2, 4, 1), (11, 'Trousers', 2, 5, 1),
        (12, 'Maxi Dress', 3, 1, 1), (13, 'Mini Dress', 3, 2, 1), (14, 'Midi Dress', 3, 3, 1),
        (15, 'Sundress', 3, 4, 1), (16, 'Cocktail Dress', 3, 5, 1),
        (17, 'Jacket', 4, 1, 1), (18, 'Blazer', 4, 2, 1), (19, 'Coat', 4, 3, 1), (20, 'Vest', 4, 4, 1),
        (21, 'Boots', 5, 1, 1), (22, 'Sneakers', 5, 2, 1), (23, 'Heels', 5, 3, 1),
        (24, 'Flats', 5, 4, 1), (25, 'Sandals', 5, 5, 1),
        (26, 'Handbag', 6, 1, 1), (27, 'Backpack', 6, 2, 1), (28, 'Scarf', 6, 3, 1),
        (29, 'Hat', 6, 4, 1), (30, 'Belt', 6, 5, 1),
        (31, 'T-Shirt', 7, 1, 1), (32, 'Button-Up Shirt', 7, 2, 1), (33, 'Polo Shirt', 7, 3, 1),
        (34, 'Sweater', 7, 4, 1), (35, 'Hoodie', 7, 5, 1),
        (36, 'Jeans', 8, 1, 1), (37, 'Chinos', 8, 2, 1), (38, 'Shorts', 8, 3, 1), (39, 'Sweatpants', 8, 4, 1),
        (40, 'Jacket', 9, 1, 1), (41, 'Blazer', 9, 2, 1), (42, 'Coat', 9, 3, 1), (43, 'Vest', 9, 4, 1),
        (44, 'Sneakers', 10, 1, 1), (45, 'Boots', 10, 2, 1), (46, 'Dress Shoes', 10, 3, 1), (47, 'Sandals', 10, 4, 1),
        (48, 'Watch', 11, 1, 1), (49, 'Backpack', 11, 2, 1), (50, 'Hat', 11, 3, 1), (51, 'Belt', 11, 4, 1),
        (52, 'T-Shirt', 12, 1, 1), (53, 'Sweater', 12, 2, 1), (54, 'Hoodie', 12, 3, 1),
        (55, 'Jeans', 13, 1, 1), (56, 'Shorts', 13, 2, 1), (57, 'Leggings', 13, 3, 1),
        (58, 'Dress', 14, 1, 1), (59, 'Jacket', 15, 1, 1), (60, 'Coat', 15, 2, 1),
        (61, 'Sneakers', 16, 1, 1), (62, 'Boots', 16, 2, 1), (63, 'Sandals', 16, 3, 1),
        (64, 'T-Shirt', 17, 1, 1), (65, 'Hoodie', 17, 2, 1), (66, 'Tank Top', 17, 3, 1),
        (67, 'Jeans', 18, 1, 1), (68, 'Joggers', 18, 2, 1), (69, 'Shorts', 18, 3, 1),
        (70, 'Windbreaker', 19, 1, 1), (71, 'Bomber Jacket', 19, 2, 1),
        (72, 'Tote Bag', 20, 1, 1), (73, 'Beanie', 20, 2, 1), (74, 'Baseball Cap', 20, 3, 1)
    ]
    conn.executemany(
        "INSERT INTO item_types (item_type_id, item_type_name, category_id, sort_order, active) VALUES (?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_sizes(conn):
    data = [
        (1, 'XXS', 'Letter', 1, None), (2, 'XS', 'Letter', 2, None),
        (3, 'S', 'Letter', 3, None), (4, 'M', 'Letter', 4, None),
        (5, 'L', 'Letter', 5, None), (6, 'XL', 'Letter', 6, None),
        (7, 'XXL', 'Letter', 7, None), (8, 'XXXL', 'Letter', 8, None),
        (9, '0', 'US Numeric', 10, None), (10, '2', 'US Numeric', 11, None),
        (11, '4', 'US Numeric', 12, None), (12, '6', 'US Numeric', 13, None),
        (13, '8', 'US Numeric', 14, None), (14, '10', 'US Numeric', 15, None),
        (15, '12', 'US Numeric', 16, None), (16, '14', 'US Numeric', 17, None),
        (17, '16', 'US Numeric', 18, None), (18, '18', 'US Numeric', 19, None),
        (19, '20', 'US Numeric', 20, None), (20, '22', 'US Numeric', 21, None),
        (21, '24', 'US Numeric', 22, None),
        (22, '26', 'Waist', 30, None), (23, '28', 'Waist', 31, None),
        (24, '29', 'Waist', 32, None), (25, '30', 'Waist', 33, None),
        (26, '31', 'Waist', 34, None), (27, '32', 'Waist', 35, None),
        (28, '33', 'Waist', 36, None), (29, '34', 'Waist', 37, None),
        (30, '36', 'Waist', 38, None), (31, '38', 'Waist', 39, None),
        (32, '40', 'Waist', 40, None), (33, '42', 'Waist', 41, None),
        (34, '6', 'Shoes', 50, None), (35, '6.5', 'Shoes', 51, None),
        (36, '7', 'Shoes', 52, None), (37, '7.5', 'Shoes', 53, None),
        (38, '8', 'Shoes', 54, None), (39, '8.5', 'Shoes', 55, None),
        (40, '9', 'Shoes', 56, None), (41, '9.5', 'Shoes', 57, None),
        (42, '10', 'Shoes', 58, None), (43, '10.5', 'Shoes', 59, None),
        (44, '11', 'Shoes', 60, None), (45, '11.5', 'Shoes', 61, None),
        (46, '12', 'Shoes', 62, None), (47, '13', 'Shoes', 63, None),
        (48, 'One Size', 'Universal', 100, None)
    ]
    conn.executemany(
        "INSERT INTO sizes (size_id, size_value, size_system, sort_order, notes) VALUES (?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_colors(conn):
    data = [
        (1, 'Black', 'Neutrals', '#000000', 1), (2, 'White', 'Neutrals', '#FFFFFF', 2),
        (3, 'Gray', 'Neutrals', '#808080', 3), (4, 'Beige', 'Neutrals', '#F5F5DC', 4),
        (5, 'Cream', 'Neutrals', '#FFFDD0', 5),
        (6, 'Navy', 'Blues', '#000080', 10), (7, 'Royal Blue', 'Blues', '#4169E1', 11),
        (8, 'Sky Blue', 'Blues', '#87CEEB', 12), (9, 'Teal', 'Blues', '#008080', 13),
        (10, 'Red', 'Reds', '#FF0000', 20), (11, 'Burgundy', 'Reds', '#800020', 21),
        (12, 'Pink', 'Pinks', '#FFC0CB', 30), (13, 'Hot Pink', 'Pinks', '#FF69B4', 31),
        (14, 'Blush', 'Pinks', '#FFB6C1', 32),
        (15, 'Forest Green', 'Greens', '#228B22', 40), (16, 'Olive', 'Greens', '#808000', 41),
        (17, 'Mint', 'Greens', '#98FF98', 42),
        (18, 'Yellow', 'Yellows', '#FFFF00', 50), (19, 'Mustard', 'Yellows', '#FFDB58', 51),
        (20, 'Orange', 'Oranges', '#FFA500', 60), (21, 'Rust', 'Oranges', '#B7410E', 61),
        (22, 'Purple', 'Purples', '#800080', 70), (23, 'Lavender', 'Purples', '#E6E6FA', 71),
        (24, 'Brown', 'Browns', '#A52A2A', 80), (25, 'Tan', 'Browns', '#D2B48C', 81),
        (26, 'Denim Blue', 'Blues', '#1560BD', 14),
        (27, 'Multicolor', 'Special', None, 100), (28, 'Print/Pattern', 'Special', None, 101)
    ]
    conn.executemany(
        "INSERT INTO colors (color_id, color_name, color_family, hex_code, sort_order) VALUES (?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_tags(conn):
    data = [
        (1, 'Vintage', 'Era', None, 1), (2, 'Y2K', 'Era', None, 1),
        (3, '90s', 'Era', None, 1), (4, '80s', 'Era', None, 1),
        (5, '70s', 'Era', None, 1), (6, 'Retro', 'Era', None, 1),
        (7, 'Boho', 'Style', None, 1), (8, 'Minimalist', 'Style', None, 1),
        (9, 'Grunge', 'Style', None, 1), (10, 'Preppy', 'Style', None, 1),
        (11, 'Streetwear', 'Style', None, 1), (12, 'Punk', 'Style', None, 1),
        (13, 'Romantic', 'Style', None, 1), (14, 'Sporty', 'Style', None, 1),
        (15, 'Designer', 'Feature', None, 1), (16, 'Sustainable', 'Feature', None, 1),
        (17, 'Handmade', 'Feature', None, 1), (18, 'Rare Find', 'Feature', None, 1),
        (19, 'Plus Size', 'Feature', None, 1), (20, 'Petite', 'Feature', None, 1),
        (21, 'Formal', 'Occasion', None, 1), (22, 'Casual', 'Occasion', None, 1),
        (23, 'Workwear', 'Occasion', None, 1), (24, 'Party', 'Occasion', None, 1),
        (25, 'Festival', 'Occasion', None, 1),
        (26, 'Floral', 'Pattern', None, 1), (27, 'Striped', 'Pattern', None, 1),
        (28, 'Plaid', 'Pattern', None, 1), (29, 'Solid', 'Pattern', None, 1),
        (30, 'Graphic', 'Pattern', None, 1)
    ]
    conn.executemany(
        "INSERT INTO tags (tag_id, tag_name, tag_category, description, active) VALUES (?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_conditions(conn):
    data = [
        (1, 'Excellent', 'Like new, no visible wear', 1),
        (2, 'Good', 'Gently used, minor wear', 2),
        (3, 'Fair', 'Noticeable wear but functional', 3),
        (4, 'Poor', 'Significant wear, may have defects', 4)
    ]
    conn.executemany(
        "INSERT INTO conditions (condition_id, condition_name, description, sort_order) VALUES (?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_item_status(conn):
    data = [
        (1, 'Available', 'Ready for sale', 1, 1),
        (2, 'Sold', 'Purchased', 0, 2),
        (3, 'Processing', 'Being prepared', 0, 3),
        (4, 'On Hold', 'Reserved', 0, 4),
        (5, 'Removed', 'No longer available', 0, 5)
    ]
    conn.executemany(
        "INSERT INTO item_status (status_id, status_name, description, is_available_for_sale, sort_order) VALUES (?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_locations(conn):
    data = [
        (1, 'Sales Floor - Rack A', 'Sales Floor', None, 1),
        (2, 'Sales Floor - Rack B', 'Sales Floor', None, 1),
        (3, 'Sales Floor - Rack C', 'Sales Floor', None, 1),
        (4, 'Sales Floor - Rack D', 'Sales Floor', None, 1),
        (5, 'Sales Floor - Shoe Display', 'Sales Floor', None, 1),
        (6, 'Sales Floor - Accessories Wall', 'Sales Floor', None, 1),
        (7, 'Back Room - Bin 1', 'Storage', None, 1),
        (8, 'Back Room - Bin 2', 'Storage', None, 1),
        (9, 'Back Room - Bin 3', 'Storage', None, 1),
        (10, 'Processing Area', 'Processing', None, 1),
        (11, 'Clearance Section', 'Sales Floor', None, 1),
        (12, 'Window Display', 'Sales Floor', None, 1)
    ]
    conn.executemany(
        "INSERT INTO locations (location_id, location_name, location_type, description, active) VALUES (?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_items(conn):
    data = [
        (1, 1, 1, 1, 'Urban Outfitters', 3, 2, None, 'Cotton', 1, 1, 1, 18.00, None, 0, None,
         'Vintage white graphic tee with retro band logo', None, 'Perfect vintage find!', 'All Season', '2024-01-15', None),
        (2, 1, 2, 7, "Levi's", 27, 26, None, 'Denim', 2, 1, 1, 45.00, None, 0, None,
         'Classic 501 high-waisted jeans in perfect condition', None, 'Iconic 501s', 'All Season', '2024-01-16', None),
        (3, 1, 3, 12, 'Free People', 13, 26, None, 'Cotton Blend', 1, 1, 2, 65.00, None, 0, None,
         'Flowy bohemian maxi dress with floral details', None, 'Boho dream dress', 'Spring/Summer', '2024-01-17', None),
        (4, 2, 7, 32, 'Brooks Brothers', 5, 6, None, 'Cotton', 1, 1, 3, 28.00, None, 0, None,
         'Crisp navy button-up shirt for work or formal', None, 'Professional essential', 'All Season', '2024-01-18', None),
        (5, 1, 5, 21, 'Dr. Martens', 38, 1, None, 'Leather', 2, 1, 5, 85.00, None, 0, None,
         'Black combat boots, gently worn', 'Minor scuffs on toe', 'Timeless boots', 'All Season', '2024-01-19', None),
        (6, 1, 1, 4, 'Gap', 4, 24, None, 'Wool Blend', 1, 1, 1, 32.00, None, 0, None,
         'Cozy brown knit sweater, fall essential', None, 'Warm and comfortable', 'Fall/Winter', '2024-01-20', None),
        (7, 2, 8, 36, 'Wrangler', 27, 26, None, 'Denim', 2, 1, 3, 38.00, None, 0, None,
         'Vintage Wrangler denim with character', None, 'Authentic vintage', 'All Season', '2024-01-21', None),
        (8, 1, 6, 26, 'Coach', 48, 24, None, 'Leather', 1, 1, 6, 125.00, None, 0, None,
         'Vintage Coach leather handbag, mint condition', None, 'Rare vintage find!', 'All Season', '2024-01-22', None),
        (9, 4, 17, 64, 'Nike', 5, 1, None, 'Cotton', 2, 1, 3, 15.00, None, 0, None,
         'Black Nike tee with swoosh', None, 'Athletic essential', 'All Season', '2024-01-23', None),
        (10, 1, 1, 2, 'Anthropologie', 12, 13, None, 'Silk', 1, 1, 2, 48.00, None, 0, None,
         'Blush pink blouse with delicate ruffles', None, 'Romantic and elegant', 'Spring/Summer', '2024-01-24', None),
    ]
    conn.executemany("""
        INSERT INTO items (
            item_id, department_id, category_id, item_type_id, brand, size_id,
            color_primary_id, color_secondary_id, material, condition_id, status_id,
            current_location_id, price, original_price, on_sale, sale_price,
            description, internal_notes, customer_notes, season, date_added, date_sold
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()


def seed_item_tags(conn):
    data = [
        (1, 1), (1, 2), (1, 30), (2, 1), (2, 22), (3, 7), (3, 26), (3, 22),
        (4, 10), (4, 23), (4, 29), (5, 9), (5, 22), (5, 18), (6, 22), (6, 29),
        (7, 1), (7, 22), (8, 1), (8, 15), (8, 18), (9, 14), (9, 22), (9, 29),
        (10, 13), (10, 23)
    ]
    conn.executemany("INSERT INTO item_tags (item_id, tag_id) VALUES (?, ?)", data)
    conn.commit()


def seed_item_photos(conn):
    data = [
        (1, 1, '/images/items/item1_front.jpg', 1, 1, '2024-01-15 10:00:00'),
        (2, 2, '/images/items/item2_front.jpg', 1, 1, '2024-01-16 10:00:00'),
        (3, 3, '/images/items/item3_front.jpg', 1, 1, '2024-01-17 10:00:00'),
        (4, 4, '/images/items/item4_front.jpg', 1, 1, '2024-01-18 10:00:00'),
        (5, 5, '/images/items/item5_pair.jpg', 1, 1, '2024-01-19 10:00:00'),
    ]
    conn.executemany(
        "INSERT INTO item_photos (photo_id, item_id, file_path, is_primary, sort_order, uploaded_date) VALUES (?, ?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def seed_item_history(conn):
    data = [
        (1, 1, 'created', '2024-01-15 10:00:00', None, None, 'Item added'),
        (2, 2, 'created', '2024-01-16 10:00:00', None, None, 'Item added'),
        (3, 8, 'created', '2024-01-22 10:00:00', None, None, 'Vintage Coach bag'),
        (4, 8, 'price_change', '2024-01-22 14:00:00', '150.00', '125.00', 'Price adjusted'),
    ]
    conn.executemany(
        "INSERT INTO item_history (history_id, item_id, action, action_date, old_value, new_value, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        data
    )
    conn.commit()


def main():
    if not os.path.exists(DATABASE_PATH):
        print(f"Database '{DATABASE_PATH}' not found. Run the app first to create it.")
        return
    
    conn = connect_db()
    
    print("Clearing existing data...")
    clear_tables(conn)
    
    print("Seeding reference tables...")
    seed_departments(conn)
    seed_categories(conn)
    seed_item_types(conn)
    seed_sizes(conn)
    seed_colors(conn)
    seed_tags(conn)
    seed_conditions(conn)
    seed_item_status(conn)
    seed_locations(conn)
    
    print("Seeding items...")
    seed_items(conn)
    seed_item_tags(conn)
    seed_item_photos(conn)
    seed_item_history(conn)
    
    conn.close()
    print("Done! Database seeded.")


if __name__ == "__main__":
    main()
