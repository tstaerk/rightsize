import streamlit as st
from PIL import Image
import io

st.title("🖼️ Image Converter & Resizer")

# Initialize session state for rotation
if "rotation" not in st.session_state:
    st.session_state.rotation = 0

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp", "gif", "webp"])

output_formats = ["JPEG", "PNG", "WEBP", "BMP", "PDF"]
default_format = "JPEG"

if uploaded_file:
    # Load image
    image = Image.open(uploaded_file)

    # File info
    uploaded_file.seek(0)
    original_size_kb = round(len(uploaded_file.read()) / 1024, 2)

    # Rotate button
    if st.button("↻ Rotate 90° clockwise"):
        st.session_state.rotation = (st.session_state.rotation + 90) % 360

    # Apply rotation
    if st.session_state.rotation != 0:
        image = image.rotate(-st.session_state.rotation, expand=True)

    # Original image info
    st.markdown(f"**Original Image:** {image.width} × {image.height} px — {original_size_kb} KB")

    # Scale and crop layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Scale")
        scale_input = st.text_input(" ", placeholder="e.g. 1024x768 or 50%", label_visibility="collapsed")

    with col2:
        st.markdown("#### Crop")
        crop_top_col, crop_top_input = st.columns([1, 2])
        with crop_top_col:
            st.markdown("Top")
        with crop_top_input:
            crop_top = st.number_input(" ", min_value=0, value=0, label_visibility="collapsed", key="crop_top")

        crop_left_col, crop_left_input = st.columns([1, 2])
        with crop_left_col:
            st.markdown("Left")
        with crop_left_input:
            crop_left = st.number_input(" ", min_value=0, value=0, label_visibility="collapsed", key="crop_left")

        crop_right_col, crop_right_input = st.columns([1, 2])
        with crop_right_col:
            st.markdown("Right")
        with crop_right_input:
            crop_right = st.number_input(" ", min_value=0, value=0, label_visibility="collapsed", key="crop_right")

        crop_bottom_col, crop_bottom_input = st.columns([1, 2])
        with crop_bottom_col:
            st.markdown("Bottom")
        with crop_bottom_input:
            crop_bottom = st.number_input(" ", min_value=0, value=0, label_visibility="collapsed", key="crop_bottom")

    crop_box = None
    left = crop_left
    top = crop_top
    right = image.width - crop_right
    bottom = image.height - crop_bottom
    if left < right and top < bottom:
        crop_box = (left, top, right, bottom)
    else:
        st.error("❌ Crop values are too large or invalid.")

    scale_valid = True
    new_width, new_height = image.width, image.height

    if scale_input:
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

    if scale_valid and crop_box:
        processed_image = image.crop(crop_box)
        processed_image = processed_image.resize((new_width, new_height))
    elif crop_box:
        processed_image = image.crop(crop_box)
    elif scale_valid and scale_input:
        processed_image = image.resize((new_width, new_height))
    else:
        processed_image = image

    buf = io.BytesIO()
    output_col1, output_col2 = st.columns([2, 1])

    with output_col2:
        output_format = st.selectbox("Format", output_formats, index=output_formats.index(default_format), label_visibility="collapsed")

    if output_format == "PDF":
        if processed_image.mode in ("RGBA", "P"):
            processed_image = processed_image.convert("RGB")
        processed_image.save(buf, format="PDF")
        mime_type = "application/pdf"
        file_ext = "pdf"
    else:
        if output_format == "JPEG":
            processed_image = processed_image.convert("RGB")
        processed_image.save(buf, format=output_format)
        mime_type = f"image/{output_format.lower()}"
        file_ext = output_format.lower()

    buf.seek(0)
    file_size_kb = round(len(buf.getvalue()) / 1024, 2)
    result_width, result_height = processed_image.width, processed_image.height

    st.markdown(f"**Converted Image:** {result_width} × {result_height} px — {file_size_kb} KB")
    st.image(processed_image, use_container_width=True)

    with output_col1:
        st.download_button(
            label=f"📥 Download as {output_format}",
            data=buf,
            file_name=f"converted_image.{file_ext}",
            mime=mime_type
        )
