import streamlit as st
from PIL import Image
import io

# Title
st.title("🖼️ Image Converter & Resizer")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp", "gif", "webp"])

# Supported formats
output_formats = ["JPEG", "PNG", "WEBP", "BMP"]
default_format = "JPEG"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)

    st.markdown("### Resize Mode")
    resize_mode = st.radio("Choose resize mode", ["Scale", "Crop"])

    new_width, new_height = image.width, image.height
    scale_valid = True

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
        new_width = st.number_input("Width", value=image.width)
        new_height = st.number_input("Height", value=image.height)

    output_format = st.selectbox("Choose output format", output_formats, index=output_formats.index(default_format))

    if st.button("Convert & Download") and (resize_mode == "Crop" or scale_valid):
        resized_image = image.resize((int(new_width), int(new_height)))

        buf = io.BytesIO()
        if output_format == "JPEG":
            resized_image = resized_image.convert("RGB")
        resized_image.save(buf, format=output_format)
        buf.seek(0)

        st.download_button(
            label=f"📥 Download as {output_format}",
            data=buf,
            file_name=f"converted_image.{output_format.lower()}",
            mime=f"image/{output_format.lower()}"
        )
