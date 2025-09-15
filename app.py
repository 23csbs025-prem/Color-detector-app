import streamlit as st
import pandas as pd
import cv2
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates

# Load the color dataset
# Ensure colors.csv is in the same directory as app.py
df = pd.read_csv("colors.csv")

# Function to get the closest color name from RGB values
def get_color_name(R, G, B):
    min_dist = float('inf')
    closest_color_name = "Unknown"
    for i in range(len(df)):
        d = np.sqrt(
            (R - df.loc[i, "R"]) ** 2
            + (G - df.loc[i, "G"]) ** 2
            + (B - df.loc[i, "B"]) ** 2
        )
        if d < min_dist:
            min_dist = d
            closest_color_name = df.loc[i, "color_name"]
    return closest_color_name

# Streamlit app layout
st.title("🎨 Image Color Detector")
st.markdown("Upload an image and **click anywhere on it** to see the color details.")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image using OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Use the custom component to display the image and capture clicks
    value = streamlit_image_coordinates(image, key="image_click")

    if value:
        # Get the pixel coordinates from the click
        x = int(value["x"])
        y = int(value["y"])

        # Get BGR values (OpenCV reads in BGR)
        b, g, r = image[y, x]
        
        # Convert to RGB
        rgb_tuple = (int(r), int(g), int(b))
        
        # Get color name
        color_name = get_color_name(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
        
        st.subheader("Detected Color Details:")
        st.write(f"**Color Name:** {color_name}")
        st.write(f"**RGB Values:** {rgb_tuple}")
        
        # Display a color box
        st.color_picker("Color Reference", f"#{rgb_tuple[0]:02x}{rgb_tuple[1]:02x}{rgb_tuple[2]:02x}")