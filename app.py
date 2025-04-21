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
    # Load the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    st.markdown("### Resize Options")
    width = st.number_input("Width", value=image.width)
    height = st.number_input("Height", value=image.height)

    st.markdown("### Output Format")
    output_format = st.selectbox("Choose output format", output_formats, index=output_formats.index(default_format))

    # Convert and download
    if st.button("Convert & Download"):
        # Resize
        resized_image = image.resize((int(width), int(height)))

        # Convert and save to buffer
        buf = io.BytesIO()
        save_format = "JPEG" if output_format == "JPEG" else output_format
        if output_format == "JPEG":
            resized_image = resized_image.convert("RGB")  # JPEG doesn't support transparency
        resized_image.save(buf, format=save_format)
        buf.seek(0)

        # Create download button
        st.download_button(
            label=f"📥 Download as {output_format}",
            data=buf,
            file_name=f"converted_image.{output_format.lower()}",
            mime=f"image/{output_format.lower()}"
        )
