# Eliminación de Objetos con Inpainting

> Una aplicación web que permite eliminar objetos no deseados de imágenes utilizando técnicas de inpainting y analizar las mejoras con IA generativa.

## Descripción

Esta aplicación resuelve el problema de eliminar objetos distractores de imágenes de manera eficiente, algo común en diseño gráfico y edición fotográfica. Está diseñada para diseñadores gráficos freelance, quienes necesitan herramientas rápidas y precisas para editar fotos de clientes sin dedicar horas a trabajo manual tedioso.

Utiliza tecnologías de IA avanzadas: el modelo LaMa para inpainting basado en difusión, y Gemini de Google para análisis visual inteligente. Lo que lo diferencia es la combinación de procesamiento automático y personalizado de máscaras, junto con un análisis detallado de las mejoras, todo en una interfaz intuitiva y accesible.

## User Persona

**Nombre**: María González  
**Contexto**: Diseñadora gráfica freelance de 28-35 años con experiencia intermedia-alta en herramientas de edición de imágenes y IA básica.  
**Problema**: Necesita eliminar objetos no deseados de fotos para clientes, pero las herramientas tradicionales son lentas y requieren mucho trabajo manual.  
**Solución**: La aplicación permite subir imágenes, seleccionar máscaras automática o dibujar personalizadas, procesar con inpainting y analizar mejoras con Gemini, ahorrando tiempo y mejorando calidad.

## Demo

[![Watch the video](https://img.youtube.com/vi/reb0jGRN2vc/default.jpg)](https://youtu.be/reb0jGRN2vc)

## Características

- Procesamiento con modelo LaMa para inpainting de alta calidad
- Análisis visual con Gemini 2.0 para evaluación de mejoras
- Interfaz intuitiva en Streamlit con opciones en español
- Comparación lado a lado de imágenes original y procesada
- Máscaras automáticas con rembg o personalizadas con dibujo interactivo
- Análisis opcional de mejoras con IA generativa

## Tecnologías Utilizadas

**Frontend:**
- Streamlit 1.40.0

**Modelos de IA:**
- LaMa - Para restauración de imágenes mediante inpainting
- Gemini 2.0 - Para análisis visual y comparación de imágenes
- rembg - Para segmentación automática de objetos

**Procesamiento:**
- PIL/Pillow
- NumPy
- OpenCV
- Torch

**Deployment:**
- Ejecutable localmente con Python

## Arquitectura del Sistema

Usuario → Interfaz Streamlit → Selección de máscara → Modelo LaMa para inpainting → Opcional: Análisis con Gemini → Resultados

La interfaz Streamlit maneja la entrada del usuario y visualización. El modelo LaMa procesa la imagen con la máscara para generar la versión inpintada. Gemini analiza las diferencias entre original e inpintada para proporcionar feedback detallado.

## Pasos

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
# Crear archivo .env
echo "GOOGLE_API_KEY=tu_key_aqui" > .env
```

5. Ejecutar aplicación:
```bash
streamlit run app.py
```

## Uso

1. Abre la aplicación ejecutando `streamlit run app.py`
2. Sube una imagen en formato PNG, JPG o JPEG
3. Selecciona "Opción de Máscara" en la barra lateral: automática o personalizada
4. Si eliges automática, se genera la máscara automáticamente
5. Si eliges personalizada, dibuja sobre la imagen en el canvas
6. Haz click en "Inpintar Imagen" para procesar
7. Revisa la imagen resultante y descargala si deseas
8. Opcionalmente, habilita "Análisis con Gemini" en la barra lateral, ingresa tu API key, selecciona un modelo y haz click en "Analizar con Gemini" para obtener una evaluación

## Decisiones de Diseño

### Por qué Streamlit
Streamlit permite crear interfaces web rápidas y simples, promoviendo transparencia en el proceso de IA al mostrar claramente cada paso sin ocultar complejidades técnicas.

### Por qué LaMa
LaMa ofrece un balance óptimo entre calidad de inpainting y velocidad de procesamiento, siendo accesible y efectivo para restauración de imágenes en contextos reales.

### Por qué Gemini
Proporciona análisis valioso para el usuario, evaluando mejoras de manera objetiva, lo que ayuda a medir el éxito del proceso y satisface la necesidad de calidad en entregas profesionales.

## Principios de Human-AI Interaction Aplicados

**Transparencia**: La aplicación muestra claramente qué hace cada modelo y cómo se procesa la imagen, sin cajas negras.

**Control**: El usuario tiene control total sobre la selección de máscara, parámetros de procesamiento y cuándo activar análisis.

**Explicabilidad**: Los resultados de Gemini explican las mejoras realizadas, ayudando al usuario a entender el valor del procesamiento.

**Manejo de errores**: Errores se comunican claramente con mensajes en español, indicando qué falló y posibles soluciones.

## Conceptos de Procesamiento Digital Aplicados

- **Restauración de imágenes**: Inpainting como técnica de reconstrucción de áreas faltantes usando modelos de difusión.
- **Filtrado espacial**: Aplicación de máscaras binarias para definir áreas a procesar.
- **Transformaciones de intensidad**: Ajustes en canales RGB durante el procesamiento con OpenCV.
- **Segmentación automática**: Uso de rembg para detección de objetos basada en IA.

## Limitaciones Conocidas

- Funciona mejor con imágenes de resolución media (hasta 1024x1024) y objetos bien definidos.
- Tiempo de procesamiento: 10-30 segundos dependiendo del hardware y tamaño de imagen.
- Tamaño máximo recomendado: 2000x2000 píxeles.
- No funciona bien con texturas muy complejas o iluminación extrema.
- Requiere conexión a internet para análisis con Gemini.

## Trabajo Futuro

- Procesamiento por lotes para múltiples imágenes.
- Más opciones de modelos de inpainting (como Stable Diffusion).
- Integración con almacenamiento en la nube.
- Mejoras en la interfaz de dibujo con herramientas avanzadas.

## Reflexiones y Aprendizajes

Construir esta aplicación me enseñó la importancia de integrar múltiples modelos de IA de manera coherente, equilibrando usabilidad y potencia técnica. Los desafíos principales fueron encontrar los modelos adecuados y optimizar el rendimiento del inpainting local. Usé IA generativa para generar prompts efectivos y analizar resultados. La próxima vez, planificaría mejor la arquitectura modular desde el inicio para facilitar extensiones futuras.

## Autor

**Mauricio Mujica**  
Estudiante de Tecnicatura Superior en Ciencias de Datos e IA - IFTS 24  
Materia: Procesamiento Digital de Imágenes e Introducción a Visión por Computadora  
Año: 2025

https://github.com/mauriciomujica
## Licencia

MIT License

## Agradecimientos

- Profesor: Matías Barreto
- Herramientas de IA utilizadas: Kilo Code

---

**Trabajo Integrador N°2 - IFTS 24 - 2025**