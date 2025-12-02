#!/usr/bin/env python3
"""
Update the item_photos table to use the generic stock images.
Maps each item to an appropriate image based on its item_type.

Run this AFTER download_images.py
Usage: python update_photo_paths.py
"""

import sqlite3
import os

DATABASE_PATH = "inventory.db"

# Map item_type_id to the appropriate image filename
# Based on the item_types from seed_database.py
ITEM_TYPE_TO_IMAGE = {
    # Women's Tops (category 1)
    1: 'tshirt.jpg',      # T-Shirt
    2: 'blouse.jpg',      # Blouse
    3: 'tank_top.jpg',    # Tank Top
    4: 'sweater.jpg',     # Sweater
    5: 'cardigan.jpg',    # Cardigan
    6: 'crop_top.jpg',    # Crop Top
    
    # Women's Bottoms (category 2)
    7: 'jeans.jpg',       # Jeans
    8: 'skirt.jpg',       # Skirt
    9: 'shorts.jpg',      # Shorts
    10: 'leggings.jpg',   # Leggings
    11: 'trousers.jpg',   # Trousers
    
    # Women's Dresses (category 3)
    12: 'maxi_dress.jpg',     # Maxi Dress
    13: 'mini_dress.jpg',     # Mini Dress
    14: 'midi_dress.jpg',     # Midi Dress
    15: 'sundress.jpg',       # Sundress
    16: 'cocktail_dress.jpg', # Cocktail Dress
    
    # Women's Outerwear (category 4)
    17: 'jacket.jpg',     # Jacket
    18: 'blazer.jpg',     # Blazer
    19: 'coat.jpg',       # Coat
    20: 'vest.jpg',       # Vest
    
    # Women's Shoes (category 5)
    21: 'boots.jpg',      # Boots
    22: 'sneakers.jpg',   # Sneakers
    23: 'heels.jpg',      # Heels
    24: 'flats.jpg',      # Flats
    25: 'sandals.jpg',    # Sandals
    
    # Women's Accessories (category 6)
    26: 'handbag.jpg',    # Handbag
    27: 'backpack.jpg',   # Backpack
    28: 'scarf.jpg',      # Scarf
    29: 'hat.jpg',        # Hat
    30: 'belt.jpg',       # Belt
    
    # Men's Tops (category 7)
    31: 'tshirt.jpg',     # T-Shirt
    32: 'button_up.jpg',  # Button-Up Shirt
    33: 'polo.jpg',       # Polo Shirt
    34: 'sweater.jpg',    # Sweater
    35: 'hoodie.jpg',     # Hoodie
    
    # Men's Bottoms (category 8)
    36: 'jeans.jpg',      # Jeans
    37: 'chinos.jpg',     # Chinos
    38: 'shorts.jpg',     # Shorts
    39: 'sweatpants.jpg', # Sweatpants
    
    # Men's Outerwear (category 9)
    40: 'jacket.jpg',     # Jacket
    41: 'blazer.jpg',     # Blazer
    42: 'coat.jpg',       # Coat
    43: 'vest.jpg',       # Vest
    
    # Men's Shoes (category 10)
    44: 'sneakers.jpg',     # Sneakers
    45: 'boots.jpg',        # Boots
    46: 'dress_shoes.jpg',  # Dress Shoes
    47: 'sandals.jpg',      # Sandals
    
    # Men's Accessories (category 11)
    48: 'watch.jpg',      # Watch
    49: 'backpack.jpg',   # Backpack
    50: 'hat.jpg',        # Hat
    51: 'belt.jpg',       # Belt
    
    # Kids Tops (category 12)
    52: 'tshirt.jpg',     # T-Shirt
    53: 'sweater.jpg',    # Sweater
    54: 'hoodie.jpg',     # Hoodie
    
    # Kids Bottoms (category 13)
    55: 'jeans.jpg',      # Jeans
    56: 'shorts.jpg',     # Shorts
    57: 'leggings.jpg',   # Leggings
    
    # Kids Dresses (category 14)
    58: 'dress.jpg',      # Dress
    
    # Kids Outerwear (category 15)
    59: 'jacket.jpg',     # Jacket
    60: 'coat.jpg',       # Coat
    
    # Kids Shoes (category 16)
    61: 'sneakers.jpg',   # Sneakers
    62: 'boots.jpg',      # Boots
    63: 'sandals.jpg',    # Sandals
    
    # Unisex Tops (category 17)
    64: 'tshirt.jpg',     # T-Shirt
    65: 'hoodie.jpg',     # Hoodie
    66: 'tank_top.jpg',   # Tank Top
    
    # Unisex Bottoms (category 18)
    67: 'jeans.jpg',      # Jeans
    68: 'joggers.jpg',    # Joggers
    69: 'shorts.jpg',     # Shorts
    
    # Unisex Outerwear (category 19)
    70: 'windbreaker.jpg',  # Windbreaker
    71: 'bomber.jpg',       # Bomber Jacket
    
    # Unisex Accessories (category 20)
    72: 'tote_bag.jpg',     # Tote Bag
    73: 'beanie.jpg',       # Beanie
    74: 'baseball_cap.jpg', # Baseball Cap
}

def update_photo_paths():
    """Update item_photos table with correct image paths based on item types."""
    
    print("\n" + "="*60)
    print("Updating Photo Paths in Database")
    print("="*60 + "\n")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # First, clear existing photos
    cursor.execute("DELETE FROM item_photos")
    print("✓ Cleared existing photo records")
    
    # Get all items with their item_type_id
    cursor.execute("SELECT item_id, item_type_id FROM items")
    items = cursor.fetchall()
    
    # Insert new photo records for each item
    photo_id = 1
    photos_added = 0
    
    for item_id, item_type_id in items:
        # Get the appropriate image for this item type
        image_filename = ITEM_TYPE_TO_IMAGE.get(item_type_id, 'tshirt.jpg')  # Default to tshirt
        file_path = f'/images/items/{image_filename}'
        
        # Insert photo record
        cursor.execute("""
            INSERT INTO item_photos (photo_id, item_id, file_path, is_primary, sort_order, uploaded_date)
            VALUES (?, ?, ?, 1, 1, datetime('now'))
        """, (photo_id, item_id, file_path))
        
        photo_id += 1
        photos_added += 1
    
    conn.commit()
    conn.close()
    
    print(f"✓ Added {photos_added} photo records")
    print("\n" + "="*60)
    print("✅ Photo paths updated successfully!")
    print("="*60 + "\n")

def verify_images_exist():
    """Check which images exist and which are missing."""
    
    print("\n" + "="*60)
    print("Checking Image Files")
    print("="*60 + "\n")
    
    # Get unique images needed
    unique_images = set(ITEM_TYPE_TO_IMAGE.values())
    
    existing = []
    missing = []
    
    for image in sorted(unique_images):
        path = os.path.join('images/items', image)
        if os.path.exists(path):
            existing.append(image)
        else:
            missing.append(image)
    
    if existing:
        print(f"✓ Found {len(existing)} images")
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} images:")
        for img in missing:
            print(f"   - images/items/{img}")
        print("\n   Run 'python download_images.py' to download them.")
    else:
        print("\n✅ All required images are present!")
    
    return len(missing) == 0

if __name__ == "__main__":
    # Check if images exist first
    all_present = verify_images_exist()
    
    if not all_present:
        response = input("\nSome images are missing. Update database anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            exit(0)
    
    # Update the database
    update_photo_paths()
    
    print("Done! Your items now have photo paths assigned.")
    print("\nNote: Make sure your FastAPI app serves the /images/items/ directory")
    print("as static files for the images to display properly.")
