import streamlit as st
from PIL import Image
import io
import base64

st.title("🖼️ Image Converter & Resizer")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp", "gif", "webp"])

output_formats = ["JPEG", "PNG", "WEBP", "BMP", "PDF"]
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
        crop_left = st.number_input("Left", value=0, min_value=0, max_value=image.width - 1)
        crop_top = st.number_input("Top", value=0, min_value=0, max_value=image.height - 1)
        crop_right = st.number_input("Right", value=0, min_value=0, max_value=image.width - crop_left - 1)
        crop_bottom = st.number_input("Bottom", value=0, min_value=0, max_value=image.height - crop_top - 1)

        left = crop_left
        top = crop_top
        right = image.width - crop_right
        bottom = image.height - crop_bottom

        if left < right and top < bottom:
            crop_box = (left, top, right, bottom)
            preview_cropped = image.crop(crop_box)
            st.image(preview_cropped, caption="🔍 Cropped Preview", use_container_width=True)
        else:
            st.error("❌ Crop values are too large or invalid.")

    output_format = st.selectbox("Choose output format", output_formats, index=output_formats.index(default_format))

    if (resize_mode == "Crop" and crop_box) or (resize_mode == "Scale" and scale_valid):
        processed_image = image

        if resize_mode == "Crop" and crop_box:
            processed_image = image.crop(crop_box)
        elif resize_mode == "Scale":
            processed_image = image.resize((int(new_width), int(new_height)))

        buf = io.BytesIO()
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

        # For clipboard copy
        img_copy_buf = io.BytesIO()
        processed_image.save(img_copy_buf, format="PNG")
        img_copy_buf.seek(0)
        img_base64 = base64.b64encode(img_copy_buf.read()).decode("utf-8")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.download_button(
                label=f"📥 Convert and Download as {output_format}",
                data=buf,
                file_name=f"converted_image.{file_ext}",
                mime=mime_type
            )

        with col2:
            st.markdown(
                f"""
                <button onclick="copyImage()" style="margin-top: 22px;">📋 Copy to Clipboard</button>
                <script>
                async function copyImage() {{
                    const base64 = "{img_base64}";
                    const blob = await (await fetch("data:image/png;base64," + base64)).blob();
                    await navigator.clipboard.write([
                        new ClipboardItem({{"image/png": blob}})
                    ]);
                    alert("✅ Image copied to clipboard");
                }}
                </script>
                """,
                unsafe_allow_html=True
            )

