import streamlit as st
from PIL import Image
import io

st.title("🖼️ Image Converter & Resizer")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp", "gif", "webp"])

output_formats = ["JPEG", "PNG", "WEBP", "BMP"]
default_format = "JPEG"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)

    st.markdown("### Resize Mode")
    resize_mode = st.radio("Choose resize mode", ["Scale", "Crop"])

    new_width, new_height = image.width, image.height
    scale_valid = True
    crop_box = None

    if resize_mode == "Scale":
        scale_input = st.text_input("Enter scale (e.g. `50%`, `1024x768`)", value="100%")

        if "x" in scale_input.lower():
            try:
                w, h = scale_input.lower().split("x")
                new_width = int(w.strip())
                new_height = int(h.strip())
            except:
                scale_valid = False
                st.error("❌ Invalid format. Use e.g. `800x600`")
        elif "%" in scale_input:
            try:
                scale = int(scale_input.replace("%", "").strip()) / 100.0
                new_width = int(image.width * scale)
                new_height = int(image.height * scale)
            except:
                scale_valid = False
                st.error("❌ Invalid percentage. Use e.g. `75%`")
        else:
            scale_valid = False
            st.error("❌ Use format like `1024x768` or `75%`")

    else:
        st.markdown("#### Crop X pixels from each side")
        crop_left = st.number_input("Left", value=
