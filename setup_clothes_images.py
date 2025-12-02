#!/usr/bin/env python3
"""
Copy and rename clothing images from /clothes to /images/items/
and update the database paths.
"""

import shutil
import os
import sqlite3

# Source and destination
SOURCE_DIR = "clothes"
DEST_DIR = "images/items"

# Mapping from your filenames to expected filenames
# your_name -> database_name
FILENAME_MAP = {
    'bagpack.jpeg': 'backpack.jpeg',
    'baseball_cap.jpeg': 'baseball_cap.jpeg',
    'beanie.jpeg': 'beanie.jpeg',
    'belt.jpeg': 'belt.jpeg',
    'blazer.jpeg': 'blazer.jpeg',
    'blouse.jpeg': 'blouse.jpeg',
    'bomber.jpeg': 'bomber.jpeg',
    'boots.jpeg': 'boots.jpeg',
    'button_up.jpeg': 'button_up.jpeg',
    'cardigan.jpeg': 'cardigan.jpeg',
    'chinos.jpeg': 'chinos.jpeg',
    'coat.jpeg': 'coat.jpeg',
    'cocktail_dress.jpeg': 'cocktail_dress.jpeg',
    'crop_top.jpeg': 'crop_top.jpeg',
    'dress.jpeg': 'dress.jpeg',
    'dress_shoes.jpeg': 'dress_shoes.jpeg',
    'flats.jpeg': 'flats.jpeg',
    'handbag.jpeg': 'handbag.jpeg',
    'hat.jpeg': 'hat.jpeg',
    'heels.jpeg': 'heels.jpeg',
    'hoodie.jpeg': 'hoodie.jpeg',
    'jacket.jpeg': 'jacket.jpeg',
    'jeans.jpeg': 'jeans.jpeg',
    'joggers.jpeg': 'joggers.jpeg',
    'leggings.jpeg': 'leggings.jpeg',
    'maxi_dress.jpeg': 'maxi_dress.jpeg',
    'midi_dress.jpeg': 'midi_dress.jpeg',
    'mini_dress.jpeg': 'mini_dress.jpeg',
    'polo.jpeg': 'polo.jpeg',
    'sandal.jpeg': 'sandals.jpeg',      # singular -> plural
    'scraf.jpeg': 'scarf.jpeg',          # typo fix
    'shorts.jpeg': 'shorts.jpeg',
    'skirt.jpeg': 'skirt.jpeg',
    'sneakers.jpeg': 'sneakers.jpeg',
    'sundress.jpeg': 'sundress.jpeg',
    'sweater.jpeg': 'sweater.jpeg',
    'sweatpants.jpeg': 'sweatpants.jpeg',
    't_shirt.jpeg': 'tshirt.jpeg',       # t_shirt -> tshirt
    'tank_top.jpeg': 'tank_top.jpeg',
    'tote_bag.jpeg': 'tote_bag.jpeg',
    'trouser.jpeg': 'trousers.jpeg',     # singular -> plural
    'vest.jpeg': 'vest.jpeg',
    'watch.jpeg': 'watch.jpeg',
    'windbreaker.jpeg': 'windbreaker.jpeg',
}

# Item type ID to image filename mapping (same as update_photo_paths.py but with .jpeg)
ITEM_TYPE_TO_IMAGE = {
    1: 'tshirt.jpeg', 2: 'blouse.jpeg', 3: 'tank_top.jpeg',
    4: 'sweater.jpeg', 5: 'cardigan.jpeg', 6: 'crop_top.jpeg',
    7: 'jeans.jpeg', 8: 'skirt.jpeg', 9: 'shorts.jpeg',
    10: 'leggings.jpeg', 11: 'trousers.jpeg',
    12: 'maxi_dress.jpeg', 13: 'mini_dress.jpeg', 14: 'midi_dress.jpeg',
    15: 'sundress.jpeg', 16: 'cocktail_dress.jpeg',
    17: 'jacket.jpeg', 18: 'blazer.jpeg', 19: 'coat.jpeg', 20: 'vest.jpeg',
    21: 'boots.jpeg', 22: 'sneakers.jpeg', 23: 'heels.jpeg',
    24: 'flats.jpeg', 25: 'sandals.jpeg',
    26: 'handbag.jpeg', 27: 'backpack.jpeg', 28: 'scarf.jpeg',
    29: 'hat.jpeg', 30: 'belt.jpeg',
    31: 'tshirt.jpeg', 32: 'button_up.jpeg', 33: 'polo.jpeg',
    34: 'sweater.jpeg', 35: 'hoodie.jpeg',
    36: 'jeans.jpeg', 37: 'chinos.jpeg', 38: 'shorts.jpeg', 39: 'sweatpants.jpeg',
    40: 'jacket.jpeg', 41: 'blazer.jpeg', 42: 'coat.jpeg', 43: 'vest.jpeg',
    44: 'sneakers.jpeg', 45: 'boots.jpeg', 46: 'dress_shoes.jpeg', 47: 'sandals.jpeg',
    48: 'watch.jpeg', 49: 'backpack.jpeg', 50: 'hat.jpeg', 51: 'belt.jpeg',
    52: 'tshirt.jpeg', 53: 'sweater.jpeg', 54: 'hoodie.jpeg',
    55: 'jeans.jpeg', 56: 'shorts.jpeg', 57: 'leggings.jpeg',
    58: 'dress.jpeg',
    59: 'jacket.jpeg', 60: 'coat.jpeg',
    61: 'sneakers.jpeg', 62: 'boots.jpeg', 63: 'sandals.jpeg',
    64: 'tshirt.jpeg', 65: 'hoodie.jpeg', 66: 'tank_top.jpeg',
    67: 'jeans.jpeg', 68: 'joggers.jpeg', 69: 'shorts.jpeg',
    70: 'windbreaker.jpeg', 71: 'bomber.jpeg',
    72: 'tote_bag.jpeg', 73: 'beanie.jpeg', 74: 'baseball_cap.jpeg',
}

def copy_and_rename_images():
    """Copy images from clothes/ to images/items/ with correct names."""
    print("\n" + "="*60)
    print("Copying and Renaming Images")
    print("="*60 + "\n")
    
    os.makedirs(DEST_DIR, exist_ok=True)
    
    copied = 0
    for src_name, dest_name in FILENAME_MAP.items():
        src_path = os.path.join(SOURCE_DIR, src_name)
        dest_path = os.path.join(DEST_DIR, dest_name)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            if src_name != dest_name:
                print(f"  ✓ {src_name} -> {dest_name}")
            else:
                print(f"  ✓ {src_name}")
            copied += 1
        else:
            print(f"  ✗ Missing: {src_name}")
    
    print(f"\nCopied {copied} images to {DEST_DIR}/")
    return copied

def update_database():
    """Update item_photos table with correct paths."""
    print("\n" + "="*60)
    print("Updating Database")
    print("="*60 + "\n")
    
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Clear existing photos
    cursor.execute("DELETE FROM item_photos")
    print("✓ Cleared existing photo records")
    
    # Get all items
    cursor.execute("SELECT item_id, item_type_id FROM items")
    items = cursor.fetchall()
    
    # Insert new photo records
    photo_id = 1
    for item_id, item_type_id in items:
        image_filename = ITEM_TYPE_TO_IMAGE.get(item_type_id, 'tshirt.jpeg')
        file_path = f'/images/items/{image_filename}'
        
        cursor.execute("""
            INSERT INTO item_photos (photo_id, item_id, file_path, is_primary, sort_order, uploaded_date)
            VALUES (?, ?, ?, 1, 1, datetime('now'))
        """, (photo_id, item_id, file_path))
        
        photo_id += 1
    
    conn.commit()
    conn.close()
    
    print(f"✓ Added {photo_id - 1} photo records")
    print("\n✅ Database updated!")

if __name__ == "__main__":
    copied = copy_and_rename_images()
    if copied > 0:
        update_database()
        print("\n🎉 Done! Your clothing images are ready.")
        print("   Start the server with: python main.py")
        print("   View an image at: http://localhost:8000/images/items/jeans.jpeg")
