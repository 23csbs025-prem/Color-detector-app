import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# ----------------------------
# Load the dataset
# ----------------------------
@st.cache_data
def load_colors():
    # If your CSV has a header row (color,color_name,hex,R,G,B)
    return pd.read_csv("colors.csv")

colors_df = load_colors()

# ----------------------------
# Helper function to get closest color name
# ----------------------------
def get_color_name(R, G, B):
    minimum = float("inf")
    cname = ""
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, "R"])) + abs(G - int(colors_df.loc[i, "G"])) + abs(B - int(colors_df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = colors_df.loc[i, "color_name"]
    return cname

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Color Detector", layout="centered")
st.title("🎨 Image Color Detector")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Open image with PIL
    image = Image.open(uploaded_file)
    st.write("Click on the image to detect colors:")

    # Get click coordinates
    coords = streamlit_image_coordinates(image, key="pil")

    if coords is not None:
        x, y = coords["x"], coords["y"]

        # Convert image to numpy
        img_np = np.array(image)
        R, G, B = img_np[y, x]

        color_name = get_color_name(R, G, B)

        st.markdown(f"**Detected Color:** {color_name}")
        st.write(f"RGB Values: ({R}, {G}, {B})")

        # Show a box filled with the detected color
        st.markdown(
            f"<div style='width:100px; height:50px; background-color:rgb({R},{G},{B}); border:1px solid #000;'></div>",
            unsafe_allow_html=True
        )

