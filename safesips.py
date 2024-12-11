import streamlit as st
import sqlite3
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import qrcode
import cv2
import io

def setup_database():
    conn = sqlite3.connect("brand_truth.db")
    cursor = conn.cursor()

    # Create products table with qr_code_data column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        product_name TEXT,
        qr_code_data TEXT UNIQUE,
        manufacturing_date TEXT,
        expiry_date TEXT,
        additional_info TEXT,
        image BLOB
    )
    """)

    # Add the qr_code_data column if it does not exist (to fix the schema)
    try:
        cursor.execute("ALTER TABLE products ADD COLUMN qr_code_data TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY,
        qr_code_data TEXT,
        location TEXT,
        FOREIGN KEY (qr_code_data) REFERENCES products (qr_code_data)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_ratings (
        id INTEGER PRIMARY KEY,
        qr_code_data TEXT,
        rating INTEGER,
        FOREIGN KEY (qr_code_data) REFERENCES products (qr_code_data)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)
    
    cursor.execute("SELECT * FROM admin WHERE username = 'delta'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO admin (username, password) VALUES ('delta', '4523')")
    
    conn.commit()
    conn.close()

# --- Generate QR Code ---
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# --- Decode QR Code ---
def decode_qr_code(image):
    img_array = np.array(image.convert("RGB"))
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img_array)
    return data

# --- Add New Product ---
def add_product(product_name, qr_code_data, manufacturing_date, expiry_date, additional_info, image):
    conn = sqlite3.connect("brand_truth.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO products (product_name, qr_code_data, manufacturing_date, expiry_date, additional_info, image)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product_name, qr_code_data, manufacturing_date, expiry_date, additional_info, image))
        conn.commit()
        st.success(f"Product '{product_name}' added successfully!")
    except sqlite3.IntegrityError:
        st.error("This QR code data already exists in the database.")
    conn.close()

# --- Add Location ---
def add_location(qr_code_data, location):
    conn = sqlite3.connect("brand_truth.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO locations (qr_code_data, location)
        VALUES (?, ?)
    """, (qr_code_data, location))
    conn.commit()
    conn.close()

# --- Add Product Rating ---
def add_rating(qr_code_data, rating):
    conn = sqlite3.connect("brand_truth.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO product_ratings (qr_code_data, rating)
        VALUES (?, ?)
    """, (qr_code_data, rating))
    conn.commit()
    conn.close()

# --- Admin Panel ---
def admin_panel():
    st.markdown("<h3 style='color: #FF5722;'>Admin Panel</h3>", unsafe_allow_html=True)
    admin_menu = st.selectbox("Admin Actions", ["View Products 📊", "Dashboard 📊", "View Locations 📍"])

    if admin_menu == "View Products 📊":
        conn = sqlite3.connect("brand_truth.db")
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, qr_code_data, manufacturing_date, expiry_date, additional_info FROM products")
        rows = cursor.fetchall()
        conn.close()
        if rows:
            df = pd.DataFrame(rows, columns=["Product Name", "QR Code Data", "Manufacturing Date", "Expiry Date", "Additional Info"])
            st.dataframe(df)
        else:
            st.info("No products found in the database.")

    elif admin_menu == "Dashboard 📊":
        conn = sqlite3.connect("brand_truth.db")
        cursor = conn.cursor()

        # Total Products
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]

        # Average Ratings
        cursor.execute("""
        SELECT products.product_name, AVG(product_ratings.rating) AS avg_rating
        FROM products
        LEFT JOIN product_ratings ON products.qr_code_data = product_ratings.qr_code_data
        GROUP BY products.product_name
        """)
        ratings = cursor.fetchall()
        conn.close()

        st.metric("Total Verified Products", total_products)
        st.markdown("### Product Ratings")
        if ratings:
            ratings_df = pd.DataFrame(ratings, columns=["Product Name", "Average Rating"])
            st.dataframe(ratings_df)
        else:
            st.info("No ratings available yet.")

    elif admin_menu == "View Locations 📍":
        conn = sqlite3.connect("brand_truth.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT products.product_name, locations.location
        FROM locations
        JOIN products ON products.qr_code_data = locations.qr_code_data
        """)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            st.markdown("### Locations of Products")
            df = pd.DataFrame(rows, columns=["Product Name", "Location"])
            st.dataframe(df)
        else:
            st.info("No locations recorded yet.")

# --- Main Application ---
def main():
    setup_database()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    st.title("🌌 Brand Truth: Product Authentication & Transparency")
    st.sidebar.title("Navigation")
    tabs = st.sidebar.radio("Navigate to:", ["Home 🏠", "Verify Product 🔍", "Search Locations 🌐", "Login 🔑", "Admin Panel 🔧"], index=0)

    if tabs == "Home 🏠":
        st.markdown("<h3 style='color: #4CAF50;'>Welcome to Brand Truth</h3>", unsafe_allow_html=True)
        st.image("https://via.placeholder.com/800x400.png?text=Brand+Truth+Product+Verification", use_container_width=True)
        st.markdown("""
        Brand Truth ensures the authenticity of products, providing transparency and building trust with consumers.  
        **Features:**  
        - Verify products using QR codes.  
        - Locate authentic products in your area.  
        - Admins can manage products and locations.  
        """)

    elif tabs == "Verify Product 🔍":
        st.subheader("Scan QR Code for Product Verification")
        qr_code_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

        if qr_code_file:
            image = Image.open(qr_code_file)
            qr_code_data = decode_qr_code(image)

            if qr_code_data:
                # Verify authenticity by querying the database
                conn = sqlite3.connect("brand_truth.db")
                cursor = conn.cursor()
                cursor.execute("SELECT product_name, qr_code_data, image FROM products WHERE qr_code_data = ?", (qr_code_data,))
                product = cursor.fetchone()
                conn.close()

                if product:
                    product_name, _, product_image = product
                    st.success(f"Product '{product_name}' is authentic!")

                    # Show product image after verification
                    if product_image:
                        image = Image.open(io.BytesIO(product_image))
                        st.image(image, caption="Authentic Product Image", use_column_width=True)

                    # Allow user to rate the product and add retailer location
                    rating = st.slider("Rate the product quality", 1, 5)
                    location = st.text_input("Enter retailer location")

                    if st.button("Submit Rating and Location"):
                        if location:
                            add_rating(qr_code_data, rating)
                            add_location(qr_code_data, location)
                            st.success("Rating and location added successfully!")
                        else:
                            st.error("Please provide a location.")

                else:
                    st.error("Product not found in the database. This may be a counterfeit.")
            else:
                st.error("Invalid QR code.")

    elif tabs == "Search Locations 🌐":
        product_name = st.text_input("Enter product name")
        if product_name:
            conn = sqlite3.connect("brand_truth.db")
            cursor = conn.cursor()
            cursor.execute("""
            SELECT products.product_name, locations.location, AVG(product_ratings.rating) AS avg_rating
            FROM locations
            JOIN products ON products.qr_code_data = locations.qr_code_data
            LEFT JOIN product_ratings ON products.qr_code_data = product_ratings.qr_code_data
            WHERE products.product_name LIKE ?
            GROUP BY locations.location
            """, ('%' + product_name + '%',))
            rows = cursor.fetchall()
            conn.close()

            if rows:
                st.markdown("### Retailer Locations for Product")
                df = pd.DataFrame(rows, columns=["Product Name", "Location", "Average Rating"])
                st.dataframe(df)
            else:
                st.info("No products found in this location.")

    elif tabs == "Login 🔑":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            conn = sqlite3.connect("brand_truth.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
            if cursor.fetchone():
                st.session_state.logged_in = True
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid username or password.")

    elif tabs == "Admin Panel 🔧" and st.session_state.logged_in:
        admin_panel()
    elif tabs == "Admin Panel 🔧" and not st.session_state.logged_in:
        st.error("Please log in first.")

if __name__ == "__main__":
    main()
