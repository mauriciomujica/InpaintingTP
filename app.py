import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
import io
from rembg import remove, new_session
from lama_cleaner.model.lama import LaMa
from lama_cleaner.schema import Config
import google.generativeai as genai

st.set_page_config(layout="wide")
st.title("Eliminación de Objetos con Inpainting🎨")
st.write("Esta aplicación permite eliminar objetos de imágenes utilizando técnicas de inpainting. Sube una imagen, selecciona una máscara automática o dibuja una personalizada, y genera una versión inpintada. Opcionalmente, analiza las mejoras con Gemini.")

# Sidebar settings
st.sidebar.header("Configuraciones⚙️")
mask_option = st.sidebar.selectbox("Opción de Máscara", ["Usar Máscara Automática", "Dibujar Máscara Personalizada"])
hd_strategy = st.sidebar.selectbox("Estrategia HD", ["ORIGINAL", "RESIZE", "CROP"])
hd_strategy_crop_trigger_size = st.sidebar.slider("Tamaño de Activación de Recorte", 100, 2000, 512)
hd_strategy_crop_margin = st.sidebar.slider("Margen de Recorte", 0, 200, 32)
hd_strategy_resize_limit = st.sidebar.slider("Límite de Redimensionamiento", 100, 2000, 512)

st.sidebar.header("Análisis con Gemini🤖")
gemini_api_key = st.sidebar.text_input("Clave API de Gemini", type="password")
enable_gemini = st.sidebar.checkbox("Habilitar Análisis con Gemini", False)
gemini_model = st.sidebar.selectbox("Modelo de Gemini", ["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-pro"], disabled=not enable_gemini)

# Main app
uploaded_file = st.file_uploader("Subir una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)
    h, w = img_np.shape[:2]

    st.subheader("Enmascaramiento")

    if mask_option == "Usar Máscara Automática":
        session = new_session()
        masked = remove(image, session=session)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Imagen Original", width=400)
        with col2:
            st.image(masked, caption="Imagen con Máscara Automática", width=400)

        mask_np = ((np.array(masked)[:, :, 3] > 0) * 255).astype(np.uint8)
        st.success("Usando máscara automática para inpainting.")
    else:
        st.subheader("Dibujar Máscara Personalizada")
        brush_size = st.slider("Tamaño del Pincel", 1, 100, 10)

        # Create canvas for mask drawing
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Red fill for mask
            stroke_width=brush_size,
            stroke_color="#FF0000",  # Red stroke
            background_image=image,
            height=h,
            width=w,
            drawing_mode="freedraw",
            key="canvas",
        )

        if canvas_result.image_data is not None:
            # Extract mask from canvas
            mask = canvas_result.image_data[:, :, -1]  # Alpha channel
            mask_np = (mask > 0).astype(np.uint8) * 255
            st.success("Máscara personalizada dibujada. Listo para inpainting.")
        else:
            mask_np = np.zeros((h, w), dtype=np.uint8)
            st.warning("No se dibujó máscara. Usando máscara vacía.")

    # Inpainting section
    st.subheader("Inpainting")
    if st.button("Inpintar Imagen"):
        with st.spinner("Inpintando..."):
            # Initialize LaMa model
            lama = LaMa("cpu")
            config = Config(
                ldm_steps=50,
                hd_strategy=hd_strategy,
                hd_strategy_crop_trigger_size=hd_strategy_crop_trigger_size,
                hd_strategy_crop_margin=hd_strategy_crop_margin,
                hd_strategy_resize_limit=hd_strategy_resize_limit,
            )
            result_bgr = lama(img_np, mask_np, config)
            result_bgr = result_bgr.astype(np.uint8)
            result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)
            inpainted_img = Image.fromarray(result_rgb)

        st.session_state.original_img = image
        st.session_state.inpainted_img = inpainted_img
        st.success("¡Inpainting completado!")

    if 'inpainted_img' in st.session_state:
        st.image(st.session_state.inpainted_img, caption="Imagen Inpintada", width=400)

        # Download button
        buf = io.BytesIO()
        st.session_state.inpainted_img.save(buf, format="PNG")
        buf.seek(0)
        st.download_button(
            label="Descargar Imagen Inpintada",
            data=buf,
            file_name="inpainted.png",
            mime="image/png",
            key="download",
        )

        # Gemini Analysis
        if enable_gemini:
            if st.button("Analizar con Gemini"):
                if gemini_api_key:
                    with st.spinner("Analizando con Gemini..."):
                        try:
                            genai.configure(api_key=gemini_api_key)
                            model = genai.GenerativeModel(gemini_model)

                            # Convert images to bytes
                            original_buf = io.BytesIO()
                            st.session_state.original_img.save(original_buf, format="PNG")
                            original_buf.seek(0)

                            inpainted_buf = io.BytesIO()
                            st.session_state.inpainted_img.save(inpainted_buf, format="PNG")
                            inpainted_buf.seek(0)

                            # Upload files
                            original_file = genai.upload_file(original_buf, mime_type="image/png")
                            inpainted_file = genai.upload_file(inpainted_buf, mime_type="image/png")

                            # Generate analysis
                            response = model.generate_content([
                                "Compara la imagen original y la imagen inpintada. Evalúa las mejoras realizadas por el proceso de inpainting. Proporciona un análisis detallado de los cambios y la calidad. No agregues introducciones ni preámbulos, ve directo al análisis. Responde en español.",
                                original_file,
                                inpainted_file
                            ])

                            analysis = response.text

                            st.subheader("Análisis con Gemini")
                            st.write(analysis)

                        except Exception as e:
                            st.error(f"Análisis con Gemini falló: {str(e)}")
                else:
                    st.warning("Se requiere la clave API de Gemini para el análisis.")
