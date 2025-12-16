import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import database as db  # Import local database module for backend logic

class CoffeeShopApp:
    """
    Main Application Class for Brey&Brew Management System.
    Handles the Graphical User Interface (GUI) using Tkinter.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Brey&Brew Management System")
        self.root.geometry("1200x750")
        
        # --- 1. DEFINE VARIABLES ---
        # State variables to track the active user and current shopping cart
        self.current_user_id = None 
        self.current_username = None 
        self.cart_data = [] # List of dictionaries to hold temporary order items
        self.img_cache = [] # Prevents garbage collection of images in Treeviews

        # --- 2. SET WINDOW ICON ---
        # Dynamically load the window icon relative to the script location
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "images", "coffee-cup.png")
            if os.path.exists(icon_path):
                icon_img = tk.PhotoImage(file=icon_path) 
                self.root.iconphoto(False, icon_img)
        except Exception as e:
            print(f"Icon Load Error: {e}")

        # --- 3. START DATABASE & UI ---
        # Initialize database tables and show the initial login screen
        db.setup_database()
        self.show_login_screen()

    # ================= LOGIN SCREEN =================
    def show_login_screen(self):
        """Renders the login interface with background image."""
        self.clear_frame() # Wipe previous UI elements

        # Attempt to load and set the background image
        try:
            base_folder = os.path.dirname(os.path.abspath(__file__))
            bg_path = os.path.join(base_folder, "images", "beans.jpg")
            bg_image = Image.open(bg_path).resize((1570, 1000), Image.Resampling.LANCZOS)
            self.login_bg_img = ImageTk.PhotoImage(bg_image)
            tk.Label(self.root, image=self.login_bg_img).place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            self.root.configure(bg="#f0f0f0") # Fallback color if image fails

        # Container frame for login inputs
        login_frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # UI Elements: Title, Inputs, Buttons
        tk.Label(login_frame, text="BREY&BREW", font=("Georgia", 20, "bold"), bg="white", fg="#333").pack(pady=(0, 20))
        
        tk.Label(login_frame, text="Username:", bg="white").pack(anchor="w")
        self.entry_user = tk.Entry(login_frame, width=30)
        self.entry_user.pack(pady=5)
        self.entry_user.bind('<Return>', lambda event: self.entry_pass.focus()) # Bind Enter key to next field

        tk.Label(login_frame, text="Password:", bg="white").pack(anchor="w", pady=(10, 0))
        self.entry_pass = tk.Entry(login_frame, show="*", width=30) # Mask password input
        self.entry_pass.pack(pady=5)
        self.entry_pass.bind('<Return>', lambda event: self.login()) # Bind Enter key to submit

        tk.Button(login_frame, text="Login", command=self.login, bg="#4CAF50", fg="white", width=25).pack(pady=(20, 5))
        tk.Button(login_frame, text="Sign Up", command=self.signup, bg="#2196F3", fg="white", width=25).pack(pady=5)

    def login(self):
        """Validates credentials against the database."""
        user = db.validate_login(self.entry_user.get(), self.entry_pass.get())
        if user:
            # Store session data: (user_id, username, password, role)
            self.current_user_id = user[0] 
            self.current_username = user[1]
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def signup(self):
        """Registers a new user."""
        if db.create_user(self.entry_user.get(), self.entry_pass.get()):
            messagebox.showinfo("Success", "Account Created! Please Login.")
        else:
            messagebox.showerror("Error", "Username already exists.")

    # ================= DASHBOARD =================
    def show_dashboard(self):
        """Sets up the main navigation tabs and header."""
        self.clear_frame()
        
        # Header Bar
        header = tk.Frame(self.root, bg="#333", height=50)
        header.pack(fill="x")
        tk.Label(header, text=f"Staff: {self.current_username}", fg="white", bg="#333", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(header, text="Logout", command=self.show_login_screen, bg="#d9534f", fg="white").pack(side="right", padx=10, pady=5)

        # Tab Control
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize Frames for each tab
        self.tab_home = tk.Frame(notebook)
        self.tab_products = tk.Frame(notebook)
        self.tab_orders = tk.Frame(notebook)
        self.tab_status = tk.Frame(notebook)
        self.tab_history = tk.Frame(notebook) 
        self.tab_users = tk.Frame(notebook)   

        # Add tabs to notebook
        notebook.add(self.tab_home, text="Home Dashboard")
        notebook.add(self.tab_products, text="Manage Products")
        notebook.add(self.tab_orders, text="Take Order")
        notebook.add(self.tab_status, text="Kitchen Monitor")
        notebook.add(self.tab_history, text="Sales History")
        notebook.add(self.tab_users, text="Staff List")

        # Build content for each tab
        self.build_home_tab()
        self.build_product_tab()
        self.build_order_tab()
        self.build_status_tab()
        self.build_history_tab() 
        self.build_users_tab()   

    # ================= HOME TAB =================
    def build_home_tab(self):
        """Displays overview statistics and branding."""
        self.tab_home.configure(bg="white")
        center_frame = tk.Frame(self.tab_home, bg="white")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load Logo
        try:
            base_folder = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_folder, "images", "logo.png")
            load = Image.open(image_path).resize((320, 300), Image.Resampling.LANCZOS)
            self.home_logo_img = ImageTk.PhotoImage(load)
            tk.Label(center_frame, image=self.home_logo_img, bg="white", bd=0).pack(pady=(0, 20))
        except Exception:
            tk.Label(center_frame, text="BREY&BREW Overview", font=("Georgia", 28, "bold"), fg="#333", bg="white").pack(pady=(0, 30))

        # Statistics Section
        stats_frame = tk.Frame(center_frame, bg="white")
        stats_frame.pack(pady=10)

        try:
            revenue, count = db.get_dashboard_stats()
        except: 
            revenue, count = (0.0, 0) 

        self.create_stat_card(stats_frame, "Total Revenue", f"₱{revenue:,.2f}", "#4CAF50", 0)
        self.create_stat_card(stats_frame, "Total Orders", f"{count}", "#2196F3", 1)
        
        tk.Button(center_frame, text="Refresh Data", command=self.refresh_home, font=("Arial", 10)).pack(pady=30)

    def create_stat_card(self, parent, title, value, color, col_index):
        """Helper function to create styled statistic cards."""
        frame = tk.Frame(parent, bg=color, width=200, height=100)
        frame.grid(row=0, column=col_index, padx=20, pady=10)
        frame.pack_propagate(False) 
        tk.Label(frame, text=title, bg=color, fg="white", font=("Arial", 12)).pack(pady=(20, 5))
        tk.Label(frame, text=value, bg=color, fg="white", font=("Arial", 18, "bold")).pack()

    def refresh_home(self):
        """Reloads the home tab to update stats."""
        for w in self.tab_home.winfo_children(): w.destroy()
        self.build_home_tab()

    # ================= USERS TAB =================
    def build_users_tab(self):
        """Displays a list of registered staff members."""
        style = ttk.Style()
        style.configure("Standard.Treeview", rowheight=30)

        tk.Label(self.tab_users, text="Registered Staff Members", font=("Georgia", 16, "bold")).pack(pady=15)
        tk.Button(self.tab_users, text="Refresh List", command=self.load_users).pack(pady=5)

        # Treeview Configuration
        columns = ("ID", "Username", "Role")
        self.user_tree = ttk.Treeview(self.tab_users, columns=columns, show="headings", style="Standard.Treeview")
        self.user_tree.heading("ID", text="User ID"); self.user_tree.column("ID", width=60, anchor="center")
        self.user_tree.heading("Username", text="Username"); self.user_tree.column("Username", width=150, anchor="center")
        self.user_tree.heading("Role", text="Role"); self.user_tree.column("Role", width=100, anchor="center")
        self.user_tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.load_users()

    def load_users(self):
        """Fetches users from DB and populates the Treeview."""
        for row in self.user_tree.get_children(): self.user_tree.delete(row)
        try:
            for user in db.fetch_all_users(): self.user_tree.insert("", tk.END, values=user)
        except: pass

    # ================= SALES HISTORY TAB =================
    def build_history_tab(self):
        """Displays completed transaction history."""
        tk.Label(self.tab_history, text="Transaction History (Completed)", font=("Georgia", 16, "bold")).pack(pady=15)
        tk.Button(self.tab_history, text="Refresh Data", command=self.load_history).pack(pady=5)

        columns = ("ID", "Cashier", "Total", "Date", "Items")
        self.hist_tree = ttk.Treeview(self.tab_history, columns=columns, show="headings", style="Standard.Treeview")
        # Define Columns
        self.hist_tree.heading("ID", text="Order ID"); self.hist_tree.column("ID", width=60, anchor="center")
        self.hist_tree.heading("Cashier", text="Cashier"); self.hist_tree.column("Cashier", width=120, anchor="center")
        self.hist_tree.heading("Total", text="Total"); self.hist_tree.column("Total", width=100, anchor="center")
        self.hist_tree.heading("Date", text="Date"); self.hist_tree.column("Date", width=150, anchor="center")
        self.hist_tree.heading("Items", text="Items"); self.hist_tree.column("Items", width=80, anchor="center")
        self.hist_tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.load_history()

    def load_history(self):
        """Fetches sales data from DB and populates the Treeview."""
        for row in self.hist_tree.get_children(): self.hist_tree.delete(row)
        try:
            for row in db.fetch_sales_history():
                vals = (row[0], row[1], f"₱{row[2]:.2f}", row[4], row[5])
                self.hist_tree.insert("", tk.END, values=vals)
        except: pass

    # ================= PRODUCT TAB =================
    def build_product_tab(self):
        """Interface for CRUD operations on Products."""
        style = ttk.Style()
        style.configure("Tall.Treeview", rowheight=110) # Taller rows for images

        # --- Left Side: Input Form ---
        form_frame = tk.Frame(self.tab_products, width=300, padx=10, pady=10)
        form_frame.pack(side="left", fill="y")
        
        tk.Label(form_frame, text="Product Details", font=("Georgia", 14, "bold")).pack(pady=10)
        
        # Inputs
        tk.Label(form_frame, text="Name").pack(anchor="w")
        self.p_name = tk.Entry(form_frame)
        self.p_name.pack(fill="x")
        self.p_name.bind('<Return>', lambda event: self.p_desc.focus())

        tk.Label(form_frame, text="Description").pack(anchor="w")
        self.p_desc = tk.Entry(form_frame)
        self.p_desc.pack(fill="x")
        self.p_desc.bind('<Return>', lambda event: self.p_price.focus())

        tk.Label(form_frame, text="Price").pack(anchor="w")
        self.p_price = tk.Entry(form_frame)
        self.p_price.pack(fill="x")
        self.p_price.bind('<Return>', lambda event: self.p_image.focus())

        tk.Label(form_frame, text="Image Path").pack(anchor="w")
        self.p_image = tk.Entry(form_frame)
        self.p_image.pack(fill="x")
        self.p_image.bind('<Return>', lambda event: self.create_product())

        # CRUD Buttons
        tk.Button(form_frame, text="Browse...", command=self.browse_image).pack(fill="x", pady=2)
        tk.Button(form_frame, text="Create", bg="#4CAF50", fg="white", command=self.create_product).pack(fill="x", pady=5)
        tk.Button(form_frame, text="Update", bg="#FFC107", command=self.update_product).pack(fill="x", pady=2)
        tk.Button(form_frame, text="Delete", bg="#F44336", fg="white", command=self.delete_product).pack(fill="x", pady=2)
        tk.Button(form_frame, text="Clear", command=self.clear_product_form).pack(fill="x", pady=5)

        # --- Right Side: Product List ---
        right_frame = tk.Frame(self.tab_products)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Search Bar
        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        tk.Label(search_frame, text="Search Product:").pack(side="left")
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change) # Auto-search on typing
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Product Table with Image Support
        cols = ("ID", "Name", "Price", "Desc", "Path")
        style.configure("Tall.Treeview", indent=0) 
        self.prod_tree = ttk.Treeview(right_frame, columns=cols, show="tree headings", style="Tall.Treeview")
        self.prod_tree["displaycolumns"] = ("ID", "Name", "Price", "Desc")

        # Column Config
        self.prod_tree.heading("#0", text="Image", anchor="center")
        self.prod_tree.column("#0", width=120, anchor="center", stretch=False)
        self.prod_tree.heading("ID", text="Prod ID", anchor="center")
        self.prod_tree.column("ID", width=50, anchor="center")
        self.prod_tree.heading("Name", text="Name", anchor="center")
        self.prod_tree.column("Name", width=150, anchor="center") 
        self.prod_tree.heading("Price", text="Price", anchor="center")
        self.prod_tree.column("Price", width=80, anchor="center")
        self.prod_tree.heading("Desc", text="Description", anchor="center")
        self.prod_tree.column("Desc", width=200, anchor="w") 

        self.prod_tree.pack(fill="both", expand=True)
        self.prod_tree.bind("<ButtonRelease-1>", self.select_product) # Populate form on click
        self.load_products()

    def browse_image(self):
        """Opens file dialog to select an image."""
        f = filedialog.askopenfilename(filetypes=(("png", "*.png"), ("jpg", "*.jpg")))
        self.p_image.delete(0, tk.END); self.p_image.insert(0, f)

    def on_search_change(self, *args):
        """Event handler for live search."""
        self.load_products(query=self.search_var.get())

    def load_products(self, query=""):
        """Fetches products and renders them with images."""
        for row in self.prod_tree.get_children(): self.prod_tree.delete(row)
        self.img_cache = [] # Reset image cache
        base_dir = os.path.dirname(os.path.abspath(__file__))

        for row in db.fetch_all_products():
            row_id, name, desc, price, rel_path = row
            # Filter by search query
            if query and query.lower() not in name.lower(): continue 

            # Load Image
            full_path = os.path.join(base_dir, rel_path) if rel_path else ""
            display_img = None
            if full_path and os.path.exists(full_path):
                try:
                    load = Image.open(full_path).resize((100, 100))
                    display_img = ImageTk.PhotoImage(load)
                    self.img_cache.append(display_img) # Keep reference
                except: pass

            formatted_price = f"₱{price:,.2f}" 
            vals = (row_id, name, formatted_price, desc, rel_path)

            if display_img: self.prod_tree.insert("", "end", text="", image=display_img, values=vals)
            else: self.prod_tree.insert("", "end", text="No Img", values=vals)

    def create_product(self):
        """Validates inputs and adds a new product to DB."""
        if not self.p_name.get() or not self.p_price.get():
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
        try:
            price_value = float(self.p_price.get())
            db.insert_product(self.p_name.get(), self.p_desc.get(), price_value, self.p_image.get())
            self.load_products(); self.clear_product_form(); self.load_order_menu()
        except: messagebox.showerror("Error", "Invalid Input")

    def update_product(self):
        """Updates the selected product in the DB."""
        if hasattr(self, 'selected_prod_id'):
            db.update_product_data(self.selected_prod_id, self.p_name.get(), self.p_desc.get(), float(self.p_price.get()), self.p_image.get())
            self.load_products(); self.load_order_menu()

    def delete_product(self):
        """Removes the selected product from the DB."""
        if hasattr(self, 'selected_prod_id'):
            db.delete_product_data(self.selected_prod_id)
            self.load_products(); self.clear_product_form(); self.load_order_menu()

    def select_product(self, event):
        """Populates the input form when a table row is clicked."""
        sel = self.prod_tree.focus()
        if not sel: return
        val = self.prod_tree.item(sel, 'values')
        if val and len(val) >= 5:
            self.clear_product_form(); self.selected_prod_id = val[0]
            self.p_name.insert(0, val[1])
            self.p_price.insert(0, val[2].replace("₱", "")) 
            self.p_desc.insert(0, val[3])
            self.p_image.insert(0, val[4])

    def clear_product_form(self):
        """Resets the input fields."""
        self.p_name.delete(0, tk.END); self.p_desc.delete(0, tk.END); self.p_price.delete(0, tk.END); self.p_image.delete(0, tk.END)

    # ================= ORDER TAB =================
    def build_order_tab(self):
        """Interface for selecting products and adding to cart."""
        left = tk.Frame(self.tab_orders, padx=10, pady=10, width=400)
        left.pack(side="left", fill="both", expand=True)

        # Product Selector
        self.product_listbox = tk.Listbox(left, height=10)
        self.product_listbox.pack(fill="x", pady=5)
        self.product_listbox.bind('<<ListboxSelect>>', self.show_selected_details)
        
        # Selection Preview
        self.lbl_preview = tk.Label(left, text="Item: ")
        self.lbl_preview.pack()
        self.img_label = tk.Label(left)
        self.img_label.pack(pady=5)
        self.order_qty = tk.Spinbox(left, from_=1, to=100)
        self.order_qty.pack()
        self.order_qty.bind('<Return>', lambda event: self.add_to_cart())
        tk.Button(left, text="Add to Cart", command=self.add_to_cart, bg="#2196F3", fg="white").pack(fill="x", pady=10)

        # Cart View (Right Side)
        right = tk.Frame(self.tab_orders, bg="#ddd", padx=10, width=300)
        right.pack(side="right", fill="both", expand=True)

        self.cart_tree = ttk.Treeview(right, columns=("Item", "Quantity", "Total"), show="headings")
        self.cart_tree.heading("Item", text="Item"); self.cart_tree.column("Item", width=120, anchor="center")
        self.cart_tree.heading("Quantity", text="Quantity"); self.cart_tree.column("Quantity", width=50, anchor="center")
        self.cart_tree.heading("Total", text="Total"); self.cart_tree.column("Total", width=80, anchor="center")
        self.cart_tree.pack(side="top", fill="both", expand=True, pady=(10, 5))
        self.cart_tree.bind("<<TreeviewSelect>>", self.on_cart_select)

        # Cart Controls
        btn_frame = tk.Frame(right, bg="#ddd")
        btn_frame.pack(side="top", fill="x", pady=5)
        tk.Button(btn_frame, text="Update Quantity", command=self.update_cart_item, bg="#FFC107").pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="Remove Item", command=self.remove_cart_item, bg="#F44336", fg="white").pack(side="left", expand=True, fill="x", padx=2)

        self.lbl_total = tk.Label(right, text="Total: ₱0.00", font=("Arial", 14, "bold"), bg="#ddd", fg="#d9534f")
        self.lbl_total.pack(side="bottom", pady=10)
        tk.Button(right, text="Checkout", command=self.checkout, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(side="bottom", fill="x", pady=5)

        self.menu_items = []; self.load_order_menu()

    def on_cart_select(self, event):
        """Syncs cart selection back to product list for editing."""
        selected_row = self.cart_tree.selection()
        if not selected_row: return
        cart_item = self.cart_tree.item(selected_row, 'values')
        if not cart_item: return
        product_name = cart_item[0]
        current_qty = cart_item[1]
        
        # Find matching item in menu list
        found_index = -1
        for index, item in enumerate(self.menu_items):
            if item[1] == product_name: 
                found_index = index
                break
        
        # Highlight and set quantity
        if found_index != -1:
            self.product_listbox.selection_clear(0, tk.END)
            self.product_listbox.selection_set(found_index)
            self.product_listbox.see(found_index)
            self.product_listbox.activate(found_index)
            self.order_qty.delete(0, tk.END)
            self.order_qty.insert(0, current_qty)
            self.show_selected_details(None)

    def remove_cart_item(self):
        """Removes selected item from the internal cart list."""
        sel = self.cart_tree.selection()
        if not sel: return
        idx = self.cart_tree.index(sel[0])
        del self.cart_data[idx]
        self.update_cart_view()

    def update_cart_item(self):
        """Updates quantity of selected cart item."""
        sel = self.cart_tree.selection()
        if not sel: return
        idx = self.cart_tree.index(sel[0])
        try:
            new_qty = int(self.order_qty.get())
            if new_qty <= 0: return 
        except ValueError: return
        item = self.cart_data[idx]
        item['qty'] = new_qty
        item['subtotal'] = item['price'] * new_qty
        self.update_cart_view()

    def load_order_menu(self):
        """Populates the listbox with available products."""
        self.product_listbox.delete(0, tk.END); self.menu_items = []
        for p in db.fetch_all_products():
            self.menu_items.append(p); self.product_listbox.insert(tk.END, f"{p[1]} - ₱{p[3]}")

    def show_selected_details(self, event):
        """Updates preview area when a product is clicked."""
        sel = self.product_listbox.curselection()
        if sel:
            item = self.menu_items[sel[0]]
            self.lbl_preview.config(text=f"Item: {item[1]} (₱{item[3]})")
            # Load Image Preview
            base_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(base_dir, item[4]) if item[4] else ""
            if full_path and os.path.exists(full_path):
                try:
                    img = ImageTk.PhotoImage(Image.open(full_path).resize((150, 150)))
                    self.img_label.config(image=img); self.img_label.image = img
                except: self.img_label.config(image='')
            else: self.img_label.config(image='')

    def add_to_cart(self):
        """Adds selected item to the temporary cart list."""
        sel = self.product_listbox.curselection()
        if not sel: return
        item = self.menu_items[sel[0]] 
        qty = int(self.order_qty.get())
        
        self.cart_data.append({
            "id": item[0],    # Store Product ID for database
            "name": item[1], 
            "price": item[3], 
            "qty": qty, 
            "subtotal": item[3] * qty
        })
        self.update_cart_view()

    def update_cart_view(self):
        """Refreshes the cart Treeview and calculates grand total."""
        for row in self.cart_tree.get_children(): self.cart_tree.delete(row)
        total = sum(i["subtotal"] for i in self.cart_data)
        for i in self.cart_data: self.cart_tree.insert("", tk.END, values=(i["name"], i["qty"], f"₱{i['subtotal']}"))
        self.lbl_total.config(text=f"Total: ₱{total}"); self.current_total_value = total

    def checkout(self):
        """Finalizes order and saves to database."""
        if not self.cart_data: return
        # Send user_id and cart items to database module
        db.save_order(self.current_user_id, self.cart_data)
        
        messagebox.showinfo("Success", "Order Saved!")
        self.cart_data=[]; self.update_cart_view()
        self.load_order_status() # Update kitchen view
        self.refresh_home()      # Update stats
        self.load_history()      # Update history

    # ================= KITCHEN TAB =================
    def build_status_tab(self):
        """Interface for monitoring and updating order status."""
        control_frame = tk.Frame(self.tab_status, pady=10, bg="#eee")
        control_frame.pack(fill="x")
        
        btn_container = tk.Frame(control_frame, bg="#eee")
        btn_container.pack() 

        # Control Buttons
        tk.Button(btn_container, text="Refresh List", command=self.load_order_status).pack(side="left", padx=10)
        tk.Button(btn_container, text="Mark Selected as Complete", bg="#4CAF50", fg="white", command=self.mark_order_complete).pack(side="left", padx=10)
        tk.Button(btn_container, text="Delete Order", bg="#d9534f", fg="white", command=self.delete_order).pack(side="left", padx=10)

        # Content Layout
        content_frame = tk.Frame(self.tab_status)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = tk.Frame(content_frame, width=700)
        left_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(left_frame, text="Incoming Orders", font=("Georgia", 12, "bold")).pack(pady=(0, 10))
        
        # Order Queue Treeview
        cols = ("ID", "Cashier", "Total", "Status", "Date")
        self.status_tree = ttk.Treeview(left_frame, columns=cols, show="headings", style="Standard.Treeview")
        self.status_tree.heading("ID", text="Order ID", anchor="center"); self.status_tree.column("ID", width=60, anchor="center")
        self.status_tree.heading("Cashier", text="Cashier", anchor="center"); self.status_tree.column("Cashier", width=100, anchor="center")
        self.status_tree.heading("Total", text="Total", anchor="center"); self.status_tree.column("Total", width=60, anchor="center")
        self.status_tree.heading("Status", text="Status", anchor="center"); self.status_tree.column("Status", width=80, anchor="center")
        self.status_tree.heading("Date", text="Date", anchor="center"); self.status_tree.column("Date", width=140, anchor="center")
        
        self.status_tree.pack(fill="both", expand=True)
        # Color Coding for status
        self.status_tree.tag_configure("Pending", background="#ffcccc") 
        self.status_tree.tag_configure("Complete", background="#ccffcc")
        self.status_tree.bind("<<TreeviewSelect>>", self.show_kitchen_details)

        # Order Details View (Receipt style)
        right_frame = tk.Frame(content_frame, bg="white", width=400, bd=2, relief="sunken")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right_frame, text="Order Details", font=("Georgia", 14, "bold"), bg="white").pack(pady=10)
        self.kitchen_details_list = tk.Listbox(right_frame, font=("Courier", 12), bg="white", bd=0, highlightthickness=0)
        self.kitchen_details_list.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_order_status()

    def load_order_status(self):
        """Fetches active orders."""
        for row in self.status_tree.get_children(): self.status_tree.delete(row)
        self.kitchen_details_list.delete(0, tk.END) 
        
        for order in db.fetch_orders_by_status():
            o_id, cashier, total_val, status, date = order
            fmt_total = f"₱{total_val:,.2f}"
            # Apply color tag based on status
            self.status_tree.insert("", tk.END, values=(o_id, cashier, fmt_total, status, date), tags=(status,))

    def show_kitchen_details(self, event):
        """Shows specific items for the selected order."""
        sel = self.status_tree.selection()
        if not sel: return
        item = self.status_tree.item(sel)
        order_id = item['values'][0]

        self.kitchen_details_list.delete(0, tk.END)
        self.kitchen_details_list.insert(tk.END, f"Order #{order_id}")
        self.kitchen_details_list.insert(tk.END, "-"*30)

        try:
            items = db.get_order_items(order_id) 
            for qty, name in items:
                self.kitchen_details_list.insert(tk.END, f"{qty}x {name}")
        except AttributeError:
             self.kitchen_details_list.insert(tk.END, "Error: Update database.py")

    def mark_order_complete(self):
        """Updates status to Complete in DB."""
        sel = self.status_tree.selection()
        if not sel: 
            messagebox.showwarning("Warning", "Select an order first!")
            return
        item = self.status_tree.item(sel)
        order_id = item['values'][0]
        db.update_order_status(order_id, "Complete")
        self.load_order_status()
        self.load_history() 
        messagebox.showinfo("Success", f"Order #{order_id} Completed!")

    def delete_order(self):
        """Permanently removes an order."""
        sel = self.status_tree.selection()
        if not sel: 
            messagebox.showwarning("Warning", "Select an order to delete!")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to permanently delete this order?"):
            return

        item = self.status_tree.item(sel)
        order_id = item['values'][0]
        db.delete_order_data(order_id)
        # Refresh all views
        self.load_order_status()
        self.load_history()
        self.refresh_home()
        self.kitchen_details_list.delete(0, tk.END)
        messagebox.showinfo("Success", f"Order #{order_id} has been deleted.")
        
    def clear_frame(self):
        """Utility to remove all widgets from the main window."""
        for w in self.root.winfo_children(): w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeShopApp(root)
    root.mainloop()