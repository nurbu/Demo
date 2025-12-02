#!/usr/bin/env python3
import sqlite3
import subprocess
import sys

print("Running seed script...")
result = subprocess.run([sys.executable, 'seed_database.py'], capture_output=True, text=True)
print("Seed script output:")
print(result.stdout)
if result.stderr:
    print("Errors:")
    print(result.stderr)

print("\n" + "="*60)
print("Checking database...")
print("="*60)

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

try:
    cursor.execute('SELECT COUNT(*) FROM items')
    items = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM departments')
    depts = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM categories')
    cats = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM tags')
    tags = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM sizes')
    sizes = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM colors')
    colors = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM item_types')
    item_types = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM locations')
    locations = cursor.fetchone()[0]
    
    print(f"\nItems: {items}")
    print(f"Departments: {depts}")
    print(f"Categories: {cats}")
    print(f"Tags: {tags}")
    print(f"Sizes: {sizes}")
    print(f"Colors: {colors}")
    print(f"Item Types: {item_types}")
    print(f"Locations: {locations}")
    print("="*60)
    
    if items == 50 and depts == 4 and cats == 20:
        print("\n✅ SUCCESS! Database successfully populated!")
        print(f"   • {items} items loaded")
        print(f"   • {depts} departments")
        print(f"   • {cats} categories")
        print(f"   • {tags} tags")
        print(f"   • {sizes} sizes")
        print(f"   • {colors} colors")
    else:
        print(f"\n⚠️  Database may not be fully populated")
        print(f"   Expected: 50 items, 4 departments, 20 categories")
        print(f"   Got: {items} items, {depts} departments, {cats} categories")
        
except Exception as e:
    print(f"\n❌ Error checking database: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()


