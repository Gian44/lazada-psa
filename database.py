import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite Database: {e}")

    def create_table(self, keyword):
        # Replace spaces with underscores in table name
        table_name = f"products_{keyword.replace(' ', '_')}"
        query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price TEXT NOT NULL,
                    sold TEXT NOT NULL,
                    link TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );"""
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return table_name
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            return None
        
    def clear_table(self, table_name):
        query = f"DELETE FROM {table_name}"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Cleared table: {table_name}")
            return True
        except sqlite3.Error as e:
            print(f"Error clearing table {table_name}: {e}")
            return False
        
    def insert_product(self, table_name, product):
        query = f"""INSERT INTO {table_name} (name, price, sold, link)
                   VALUES (?, ?, ?, ?);"""
        try:
            self.cursor.execute(query, (product['name'], product['price'], product['sold'], product['link']))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting product: {e}")

    def get_products(self, table_name, sort_option='default'):
        base_query = f"""SELECT name, price, sold, link FROM {table_name}"""
        
        if sort_option == 'price_low_to_high':
            base_query += """
                ORDER BY 
                    CAST(REPLACE(REPLACE(price, '₱', ''), ',', '') AS REAL) ASC,
                    CASE 
                        WHEN sold LIKE '%K%' THEN 
                            CAST(REPLACE(REPLACE(REPLACE(sold, ' sold/month', ''), 'K', ''), '+', '') AS REAL) * 1000
                        WHEN sold LIKE '%+%' THEN 
                            10000
                        ELSE 
                            CAST(REPLACE(REPLACE(sold, ' sold/month', ''), ',', '') AS INTEGER)
                    END DESC"""
        elif sort_option == 'price_high_to_low':
            base_query += """
                ORDER BY 
                    CAST(REPLACE(REPLACE(price, '₱', ''), ',', '') AS REAL) DESC,
                    CASE 
                        WHEN sold LIKE '%K%' THEN 
                            CAST(REPLACE(REPLACE(REPLACE(sold, ' sold/month', ''), 'K', ''), '+', '') AS REAL) * 1000
                        WHEN sold LIKE '%+%' THEN 
                            10000
                        ELSE 
                            CAST(REPLACE(REPLACE(sold, ' sold/month', ''), ',', '') AS INTEGER)
                    END DESC"""
        elif sort_option == 'sold_high_to_low':
            base_query += """
                ORDER BY 
                    CASE 
                        WHEN sold LIKE '%K%' THEN 
                            CAST(REPLACE(REPLACE(REPLACE(sold, ' sold/month', ''), 'K', ''), '+', '') AS REAL) * 1000
                        WHEN sold LIKE '%+%' THEN 
                            10000
                        ELSE 
                            CAST(REPLACE(REPLACE(sold, ' sold/month', ''), ',', '') AS INTEGER)
                    END DESC,
                    CAST(REPLACE(REPLACE(price, '₱', ''), ',', '') AS REAL) ASC"""
        elif sort_option == 'sold_low_to_high':
            base_query += """
                ORDER BY 
                    CASE 
                        WHEN sold LIKE '%K%' THEN 
                            CAST(REPLACE(REPLACE(REPLACE(sold, ' sold/month', ''), 'K', ''), '+', '') AS REAL) * 1000
                        WHEN sold LIKE '%+%' THEN 
                            10000
                        ELSE 
                            CAST(REPLACE(REPLACE(sold, ' sold/month', ''), ',', '') AS INTEGER)
                    END ASC,
                    CAST(REPLACE(REPLACE(price, '₱', ''), ',', '') AS REAL) ASC"""
        else:  # default
            base_query += """ ORDER BY timestamp DESC"""
            
        try:
            self.cursor.execute(base_query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving products: {e}")
            return []
        
    def get_all_product_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'products_%'"
        try:
            self.cursor.execute(query)
            tables = self.cursor.fetchall()
            # Extract keywords from table names (remove 'products_' prefix)
            return [table[0].replace('products_', '').replace('_', ' ') for table in tables]
        except sqlite3.Error as e:
            print(f"Error getting tables: {e}")
            return []
        
    def close(self):
        if self.conn:
            self.conn.close()
