import sqlite3
import os

DB_NAME = "Brey&Brew.db"

def create_connection():
    """Establishes and returns a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def setup_database():
    """
    Initializes the database structure.
    Reads 'schema.sql' to create tables if they don't exist.
    """
    conn = create_connection()
    cursor = conn.cursor()
    if os.path.exists('schema.sql'):
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())
        conn.commit()
    conn.close()

# --- USER FUNCTIONS ---
def validate_login(username, password):
    """
    Checks if a username/password combination exists.
    Returns the user tuple if found, None otherwise.
    Uses parameterized queries (?) to prevent SQL Injection.
    """
    conn = create_connection()
    cursor = conn.cursor()
    # UPDATED TABLE: User
    cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, password):
    """Inserts a new user into the User table."""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        # UPDATED TABLE: User
        cursor.execute("INSERT INTO User (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Handles case where username already exists (UNIQUE constraint)
        return False

def fetch_all_users():
    """Retrieves all registered users for the Staff List tab."""
    conn = create_connection()
    cursor = conn.cursor()
    # UPDATED TABLE: User
    cursor.execute("SELECT user_id, username, role FROM User") 
    users = cursor.fetchall()
    conn.close()
    return users

# --- DASHBOARD STATS ---
def get_dashboard_stats():
    """Calculates total revenue and total order count for the Home tab."""
    conn = create_connection()
    cursor = conn.cursor()
    # Calculate revenue: Sum of (quantity * unit_price) from OrderItem table
    cursor.execute("SELECT SUM(quantity * unit_price) FROM OrderItem")
    revenue = cursor.fetchone()[0]
    if revenue is None: revenue = 0
    
    # Calculate count: Total rows in [Order] table
    cursor.execute("SELECT COUNT(*) FROM [Order]")
    count = cursor.fetchone()[0]
    conn.close()
    return revenue, count

# --- PRODUCT FUNCTIONS ---
def fetch_all_products():
    """Retrieves all product details."""
    conn = create_connection()
    cursor = conn.cursor()
    # UPDATED TABLE: Product
    cursor.execute("SELECT * FROM Product")
    items = cursor.fetchall()
    conn.close()
    return items

def insert_product(name, desc, price, image_path):
    """Adds a new product to the inventory."""
    conn = create_connection()
    cursor = conn.cursor()
    # UPDATED TABLE: Product
    cursor.execute("INSERT INTO Product (name, description, price, image_path) VALUES (?, ?, ?, ?)",
                   (name, desc, price, image_path))
    conn.commit()
    conn.close()

def update_product_data(prod_id, name, desc, price, image_path):
    """Updates details of an existing product based on ID."""
    conn = create_connection()
    cursor = conn.cursor()
    # UPDATED TABLE: Product
    cursor.execute("UPDATE Product SET name=?, description=?, price=?, image_path=? WHERE product_id=?",
                   (name, desc, price, image_path, prod_id))
    conn.commit()
    conn.close()

def delete_product_data(prod_id):
    """Removes a product from the inventory."""
    conn = create_connection()
    cursor = conn.cursor()
    # UPDATED TABLE: Product
    cursor.execute("DELETE FROM Product WHERE product_id=?", (prod_id,))
    conn.commit()
    conn.close()

# --- ORDER FUNCTIONS ---
def save_order(user_id, cart_data):
    """
    Transactional function to save a new order.
    1. Creates the main Order record.
    2. Iterates through the cart to create OrderItem records linked to the Order.
    """
    conn = create_connection()
    cursor = conn.cursor()
    
    # Step 1: Create Order linked to the User
    cursor.execute("INSERT INTO [Order] (user_id) VALUES (?)", (user_id,))
    new_order_id = cursor.lastrowid # Get the ID of the order just created
    
    # Step 2: Insert items
    for item in cart_data:
        # Store unit_price explicitly to preserve historical pricing
        cursor.execute("INSERT INTO OrderItem (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                       (new_order_id, item['id'], item['qty'], item['price']))
    conn.commit()
    conn.close()

def fetch_orders_by_status(status=None):
    """
    Retrieves orders for the Kitchen Monitor.
    Joins [Order], User, and OrderItem tables to calculate totals dynamically.
    """
    conn = create_connection()
    cursor = conn.cursor()
    
    # Base Query: Get Order ID, Staff Name, and Calculated Total
    base_query = """
        SELECT o.order_id, u.username, 
               (SELECT SUM(quantity * unit_price) FROM OrderItem WHERE order_id = o.order_id) as total_amount,
               o.status, o.order_date 
        FROM [Order] o
        JOIN User u ON o.user_id = u.user_id
    """
    
    if status:
        cursor.execute(base_query + " WHERE o.status=? ORDER BY o.order_id DESC", (status,))
    else:
        cursor.execute(base_query + " ORDER BY o.order_id DESC")
        
    items = cursor.fetchall()
    # Clean up None values if an order has no items
    cleaned_items = []
    for item in items:
        i = list(item)
        if i[2] is None: i[2] = 0.0
        cleaned_items.append(i)

    conn.close()
    return cleaned_items

def update_order_status(order_id, new_status):
    """Updates the status (e.g., Pending -> Complete)."""
    conn = create_connection()
    cursor = conn.cursor()
    # UPDATED TABLE: [Order]
    cursor.execute("UPDATE [Order] SET status=? WHERE order_id=?", (new_status, order_id))
    conn.commit()
    conn.close()

def fetch_sales_history():
    """
    Retrieves only 'Complete' orders for the History tab.
    Uses LEFT JOIN to include orders even if items are missing (edge case safety).
    """
    conn = create_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT o.order_id, u.username, 
           SUM(oi.quantity * oi.unit_price) as total_amount, 
           o.status, o.order_date, COUNT(oi.item_id)
    FROM [Order] o
    JOIN User u ON o.user_id = u.user_id
    LEFT JOIN OrderItem oi ON o.order_id = oi.order_id
    WHERE o.status = 'Complete'
    GROUP BY o.order_id
    ORDER BY o.order_id DESC
    """
    cursor.execute(query)
    history = cursor.fetchall()
    conn.close()
    return history

def get_order_items(order_id):
    """Fetches specific line items for a given order ID (for receipt view)."""
    conn = create_connection()
    cursor = conn.cursor()
    # UPDATED TABLES: OrderItem, Product
    query = """
        SELECT oi.quantity, p.name 
        FROM OrderItem oi
        JOIN Product p ON oi.product_id = p.product_id
        WHERE oi.order_id=?
    """
    cursor.execute(query, (order_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def delete_order_data(order_id):
    """
    Deletes an order and its associated items.
    Must delete from OrderItem first (Foreign Key constraint) then [Order].
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM OrderItem WHERE order_id=?", (order_id,))
    cursor.execute("DELETE FROM [Order] WHERE order_id=?", (order_id,))
    conn.commit()
    conn.close()