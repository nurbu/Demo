"""
Complete Database Seeding Script
Run this to populate your database with all the seed data from relations.rtf

Usage:
    python load_seed_data.py
"""
from sqlalchemy import create_engine, text
from models import Base

def load_seed_data():
    """Load all seed data from the extracted SQL file"""
    
    # 1. Create database connection
    print("Creating database connection...")
    engine = create_engine('sqlite:///./inventory.db', echo=False)
    
    # 2. Create all tables from models
    print("Creating database tables from models...")
    Base.metadata.create_all(engine)
    print("✓ Tables created")
    
    # 3. Read and execute the SQL file
    print("\nLoading seed data...")
    
    with open('seed_data.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Remove single-line comments (-- comments)
    # Split by newlines, filter out comment lines, then rejoin
    lines = sql_content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove inline comments (everything after --)
        if '--' in line:
            # Check if it's not inside a string
            comment_pos = line.find('--')
            # Simple check: if there's an odd number of quotes before --, it might be in a string
            # For simplicity, just remove comments that are clearly not in strings
            if comment_pos > 0 and line[comment_pos-1] not in ["'", '"']:
                line = line[:comment_pos].rstrip()
        cleaned_lines.append(line)
    
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Split into individual statements by semicolon
    statements = [s.strip() for s in cleaned_content.split(';') if s.strip()]
    
    # Execute each statement
    with engine.begin() as conn:  # Use begin() for transaction management
        try:
            insert_count = 0
            for statement in statements:
                if statement and 'INSERT INTO' in statement.upper():
                    # Extract table name for better logging
                    try:
                        table_name = statement.split('INSERT INTO')[1].split('(')[0].strip()
                        insert_count += 1
                        print(f"  {insert_count}. Inserting into {table_name}...")
                    except:
                        print(f"  {insert_count + 1}. Executing INSERT statement...")
                        insert_count += 1
                    
                    conn.execute(text(statement))
                    print(f"     ✓ Done")
            
            print("\n✅ All seed data loaded successfully!")
            
            # Print summary (need a new connection for queries after transaction)
            print("\n" + "="*50)
            print("DATABASE SUMMARY")
            print("="*50)
            
            # Count records in each table
            tables = [
                'departments', 'categories', 'item_types', 'sizes', 
                'colors', 'tags', 'conditions', 'item_status', 
                'locations', 'items', 'item_tags', 'item_photos', 'item_history'
            ]
            
            with engine.connect() as summary_conn:
                for table in tables:
                    try:
                        result = summary_conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.scalar()
                        print(f"  {table.ljust(20)}: {count:,} records")
                    except Exception as e:
                        print(f"  {table.ljust(20)}: Error - {e}")
            
            print("="*50)
            
        except Exception as e:
            print(f"\n❌ Error loading seed data: {e}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    load_seed_data()