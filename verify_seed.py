#!/usr/bin/env python3
"""
Verify the database was seeded correctly.
Run: python verify_seed.py
"""
import sqlite3
import sys

def verify():
    """Check that all tables have the expected data."""
    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        # Expected counts
        expected = {
            'departments': 4,
            'categories': 20,
            'item_types': 74,
            'sizes': 48,
            'colors': 28,
            'tags': 30,
            'conditions': 4,
            'item_status': 5,
            'locations': 12,
            'items': 50,
            'item_tags': 123,
            'item_photos': 21,
            'item_history': 8
        }
        
        print("\n" + "="*60)
        print("DATABASE VERIFICATION")
        print("="*60)
        
        all_good = True
        for table, expected_count in expected.items():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            actual_count = cursor.fetchone()[0]
            
            status = "✓" if actual_count == expected_count else "✗"
            if actual_count != expected_count:
                all_good = False
                print(f"  {status} {table.ljust(15)}: {actual_count:>4} (expected {expected_count})")
            else:
                print(f"  {status} {table.ljust(15)}: {actual_count:>4}")
        
        print("="*60)
        
        if all_good:
            print("✅ SUCCESS! Database is fully populated!")
            conn.close()
            return True
        else:
            print("⚠️  Some tables have unexpected counts.")
            conn.close()
            return False
            
    except sqlite3.OperationalError as e:
        print(f"\n❌ Database error: {e}")
        print("   Make sure inventory.db exists and tables are created.")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)

