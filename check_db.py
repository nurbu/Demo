#!/usr/bin/env python3
"""
Quick database check script.
Run: python check_db.py
"""
import sqlite3
import sys

def check():
    """Check current database state."""
    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        tables = [
            'departments', 'categories', 'item_types', 'sizes', 
            'colors', 'tags', 'conditions', 'item_status', 
            'locations', 'items', 'item_tags', 'item_photos', 'item_history'
        ]
        
        print("\n" + "="*60)
        print("DATABASE STATUS")
        print("="*60)
        
        total = 0
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total += count
                print(f"  {table.ljust(15)}: {count:>4} records")
            except sqlite3.OperationalError:
                print(f"  {table.ljust(15)}: TABLE NOT FOUND")
        
        print("="*60)
        print(f"  Total records: {total}")
        print("="*60)
        
        conn.close()
        
        if total > 0:
            print("✅ Database has data!")
            return True
        else:
            print("⚠️  Database is empty. Run: python run_seed.py")
            return False
            
    except sqlite3.OperationalError as e:
        print(f"\n❌ Database error: {e}")
        print("   Run 'python main.py' first to create the database.")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = check()
    sys.exit(0 if success else 1)

