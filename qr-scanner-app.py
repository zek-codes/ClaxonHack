import cv2
import streamlit as st
import numpy as np
from PIL import Image

st.title("QR Code Comparison System")

# Initialize the QR Code detector
qr_detector = cv2.QRCodeDetector()

# Upload sections for test QR code and reference QR code
test_qr_file = st.file_uploader("Upload the Test QR Code", type=["png", "jpg", "jpeg"])
reference_qr_file = st.file_uploader("Upload the Reference QR Code for Comparison", type=["png", "jpg", "jpeg"])

# Function to decode QR code from an uploaded image file
def decode_qr_code(uploaded_file):
    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(uploaded_file)
        image = np.array(image)

        # Convert to BGR format for OpenCV
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Detect and decode the QR code
        data, vertices_array, _ = qr_detector.detectAndDecode(image_bgr)

        # Draw a rectangle around the detected QR code
        if vertices_array is not None:
            for i in range(len(vertices_array)):
                pt1 = tuple(vertices_array[i][0])
                pt2 = tuple(vertices_array[(i + 1) % len(vertices_array)][0])
                cv2.line(image_bgr, pt1, pt2, (0, 255, 0), 2)

        # Convert image back to RGB format for displaying
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        return data, image_rgb

    return None, None

# Decoding and displaying uploaded QR codes
test_qr_data, test_qr_image = None, None
reference_qr_data, reference_qr_image = None, None

# Decode test QR code if uploaded
if test_qr_file:
    st.write("Decoding Test QR Code...")
    test_qr_data, test_qr_image = decode_qr_code(test_qr_file)
    if test_qr_data:
        st.image(test_qr_image, caption="Test QR Code with Highlight", use_column_width=True)
        st.write(f"Test QR Code Data: {test_qr_data}")
    else:
        st.warning("No QR code detected in the test QR code image.")

# Decode reference QR code if uploaded
if reference_qr_file:
    st.write("Decoding Reference QR Code...")
    reference_qr_data, reference_qr_image = decode_qr_code(reference_qr_file)
    if reference_qr_data:
        st.image(reference_qr_image, caption="Reference QR Code with Highlight", use_column_width=True)
        st.write(f"Reference QR Code Data: {reference_qr_data}")
    else:
        st.warning("No QR code detected in the reference QR code image.")

# Function to compare two QR codes
def compare_qr_codes(test_data, reference_data):
    if test_data and reference_data:
        if test_data == reference_data:
            st.success("Authentication Successful! The QR codes match.")
        else:
            st.error("Authentication Failed! The QR codes do not match.")
    else:
        st.warning("Both QR codes must be uploaded and contain detectable QR code data.")

# Button to trigger the comparison
if st.button("Compare QR Codes"):
    compare_qr_codes(test_qr_data, reference_qr_data)
