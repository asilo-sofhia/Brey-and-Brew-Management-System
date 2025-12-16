# Brey&Brew Management System ☕

> **A comprehensive Point of Sale (POS) and management system designed for coffee shop operations.**

## 📖 Project Overview
The **Brey&Brew Management System** is a desktop application developed to streamline daily store operations. It replaces manual, paper-based workflows with an integrated digital solution that handles order processing, sales tracking, and inventory management.

<img width="679" height="584" alt="logo" src="https://github.com/user-attachments/assets/88e4f3fb-36d3-410a-8b9a-7e1f91d5238a" />

## ✨ Key Features

### 🔐 User Authentication
* Secure Login and Sign-up system.
* Role-based access (Manager/Staff) stored in the database.
<img width="1491" height="967" alt="authentication" src="https://github.com/user-attachments/assets/574e395b-68e0-4b1b-915f-b5a81723bd29" />

### 📊 Dashboard
* **Real-time Analytics:** View Total Revenue and Total Orders at a glance.
* Data is dynamically aggregated from the database.

### 🛒 Point of Sale (POS)
* **Product Selection:** Visual menu with images.
* **Cart Management:** Add items, update quantities, or remove items before checkout.
* **Snapshot Pricing:** The system records the price *at the moment of sale* to ensure historical accuracy, even if menu prices change later.

### 📦 Product Management (CRUD)
* Full capability to **Create, Read, Update, and Delete** products.
* Upload and manage product images.
* Search functionality to quickly find items.

### 🍳 Kitchen Monitor
* Real-time display of incoming "Pending" orders.
* Kitchen staff can view order details and mark them as "Complete".
* Status updates reflect immediately in the sales history.

### 📈 Sales History
* A read-only ledger of all completed transactions.
* Displays Order ID, Cashier, Total Amount, and Date.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** Tkinter & Tkinter.ttk
* **Database:** SQLite3
* **Image Processing:** Pillow (PIL)
* **System:** OS Module for dynamic path handling

---

## 🗄️ Database Architecture
The database (`Brey&Brew.db`) follows strict **3rd Normal Form (3NF)** to ensure data integrity and eliminate redundancy.

### Schema Overview
1.  **User Table:** Stores staff credentials and roles.
2.  **Product Table:** Stores menu items, descriptions, and current prices.
3.  **[Order] Table:** Acts as the transaction header (Who sold it, when, and status).
4.  **OrderItem Table:** An associative entity linking Orders and Products.

### Key Design Decision: Snapshot Pricing
We implemented a `unit_price` column in the `OrderItem` table. This ensures that financial reports remain accurate regardless of future price adjustments in the `Product` table.

---

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/brey-and-brew.git](https://github.com/your-username/brey-and-brew.git)
    cd brey-and-brew
    ```

2.  **Install dependencies:**
    You need the `Pillow` library for image handling.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application:**
    ```bash
    python main.py
    ```
    *Note: The database (`Brey&Brew.db`) and tables will be created automatically via `schema.sql` upon the first run.*

---

## 👤 Author
**Sofhia Aubrey M. Asilo**
*December 2025*
