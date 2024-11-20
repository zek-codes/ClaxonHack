import streamlit as st
import sqlite3
from PIL import Image
import pandas as pd
import numpy as np
import cv2

# --- Database Setup ---
def setup_database():
    conn = sqlite3.connect("qr_codes.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drinks (
        id INTEGER PRIMARY KEY,
        drink_name TEXT,
        qr_code TEXT UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY,
        qr_code TEXT,
        location TEXT,
        FOREIGN KEY (qr_code) REFERENCES drinks (qr_code)
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

# --- QR Code Decoding ---
def decode_qr_code(image):
    img_array = np.array(image.convert("RGB"))
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img_array)
    return data

# --- Verify Admin Credentials ---
def verify_admin(username, password):
    conn = sqlite3.connect("qr_codes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# --- Add New Location ---
def add_location(qr_code, location):
    conn = sqlite3.connect("qr_codes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drinks WHERE qr_code = ?", (qr_code,))
    if cursor.fetchone():
        cursor.execute("INSERT INTO locations (qr_code, location) VALUES (?, ?)", (qr_code, location))
        conn.commit()
        st.success("Location added successfully!")
    else:
        st.error("Invalid QR code. No associated drink found.")
    conn.close()

# --- Delete Verified QR Code ---
def delete_verified_qr_code(qr_code):
    conn = sqlite3.connect("qr_codes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM drinks WHERE qr_code = ?", (qr_code,))
    cursor.execute("DELETE FROM locations WHERE qr_code = ?", (qr_code,))
    conn.commit()
    conn.close()

# --- Admin Panel ---
def admin_panel():
    st.markdown("<h3 style='color: #FF5722;'>Admin Panel</h3>", unsafe_allow_html=True)
    admin_menu = st.radio("Admin Actions", ["Add QR Code", "View QR Codes", "Manage Locations"])

    if admin_menu == "Add QR Code":
        drink_name = st.text_input("Enter drink name")
        qr_code_data = st.text_input("Enter QR code data")
        if st.button("Add QR Code"):
            if drink_name and qr_code_data:
                conn = sqlite3.connect("qr_codes.db")
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO drinks (drink_name, qr_code) VALUES (?, ?)", (drink_name, qr_code_data))
                    conn.commit()
                    st.success(f"QR code added successfully for '{drink_name}'!")
                except sqlite3.IntegrityError:
                    st.error("This QR code already exists in the database.")
                conn.close()
            else:
                st.error("Please provide both drink name and QR code data.")

    elif admin_menu == "View QR Codes":
        conn = sqlite3.connect("qr_codes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT drink_name, qr_code FROM drinks")
        rows = cursor.fetchall()
        conn.close()
        if rows:
            df = pd.DataFrame(rows, columns=["Drink Name", "QR Code"])
            st.dataframe(df)
        else:
            st.info("No QR codes found in the database.")

    elif admin_menu == "Manage Locations":
        st.markdown("<h4 style='color: #FF5722;'>Manage Locations</h4>", unsafe_allow_html=True)
        qr_code = st.text_input("Enter QR code")
        location = st.text_input("Enter location")
        if st.button("Add Location"):
            if qr_code and location:
                add_location(qr_code, location)
            else:
                st.error("Please provide both QR code and location.")

        conn = sqlite3.connect("qr_codes.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT drinks.drink_name, locations.qr_code, locations.location
        FROM locations
        JOIN drinks ON drinks.qr_code = locations.qr_code
        """)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            st.markdown("### Locations of Authentic Drinks")
            df = pd.DataFrame(rows, columns=["Drink Name", "QR Code", "Location"])
            st.dataframe(df)
        else:
            st.info("No locations recorded yet.")

# --- Main Application ---
def main():
    setup_database()

    st.title("🌟 SafeSips: Authentic Drink Verification")
    st.sidebar.title("Navigation")
    tabs = st.sidebar.radio("Navigate to:", ["Home", "Verify Drink", "Search Locations", "Admin Login"])

    if tabs == "Home":
        st.markdown("<h3 style='color: #4CAF50;'>Welcome to SafeSips</h3>", unsafe_allow_html=True)
        st.image("https://via.placeholder.com/800x400.png?text=SafeSips+Drink+Verification", use_container_width=True)  # Replace this URL with an actual image relevant to the home page
        st.markdown("""
        SafeSips ensures the authenticity of Delta Beverages' drinks, protecting customers and maintaining trust in the brand.  
        **Features:**  
        - Verify drinks using QR codes.  
        - Locate authentic drinks in your area.  
        - Admins can manage QR codes and locations.
        """)

    elif tabs == "Verify Drink":
        st.markdown("<h3 style='color: #4CAF50;'>Verify Drink Authenticity</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a QR code image", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded QR Code", use_container_width=True)
            qr_data = decode_qr_code(image)
            if qr_data:
                st.info(f"Decoded QR Code Data: {qr_data}")
                conn = sqlite3.connect("qr_codes.db")
                cursor = conn.cursor()
                cursor.execute("SELECT drink_name FROM drinks WHERE qr_code = ?", (qr_data,))
                result = cursor.fetchone()
                if result:
                    st.success(f"Valid QR code for the drink: {result[0]}")
                    delete_verified_qr_code(qr_data)
                    st.info(f"The QR code for {result[0]} has been deleted from the database after verification.")
                else:
                    st.error("Invalid QR code! This product may be counterfeit.")
                conn.close()
            else:
                st.error("No QR code detected. Please upload a valid QR code image.")

    elif tabs == "Search Locations":
        st.markdown("<h3 style='color: #4CAF50;'>Search Authentic Drink Locations</h3>", unsafe_allow_html=True)
        search_query = st.text_input("Enter a location to search")
        if st.button("Search"):
            conn = sqlite3.connect("qr_codes.db")
            cursor = conn.cursor()
            cursor.execute("""
            SELECT drinks.drink_name, locations.qr_code, locations.location
            FROM locations
            JOIN drinks ON drinks.qr_code = locations.qr_code
            WHERE locations.location LIKE ?
            """, ('%' + search_query + '%',))
            rows = cursor.fetchall()
            conn.close()

            if rows:
                df = pd.DataFrame(rows, columns=["Drink Name", "QR Code", "Location"])
                st.dataframe(df)
            else:
                st.error(f"No results found for location: '{search_query}'")

    elif tabs == "Admin Login":
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            st.markdown("<h3 style='color: #FF5722;'>Admin Login</h3>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if verify_admin(username, password):
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    # Directly display the admin panel once logged in
                    st.session_state.admin_logged_in = True
                else:
                    st.error("Invalid username or password.")
        else:
            admin_panel()

if __name__ == "__main__":
    main()
