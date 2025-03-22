import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import base64
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Mandala Generator",
    page_icon="🔮",
    layout="centered"
)

# App title and styling
st.markdown("""
# 🔮 Mandala Art Generator
Generate beautiful black and white mandala art from a single word inspiration.
""")

# Sidebar for API key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    st.markdown("---")
    st.markdown("## About")
    st.markdown("""
    This app uses OpenAI's DALL-E 3 to generate unique mandala art based on your inspiration.
    
    Provide a single word, and the AI will create a beautiful black and white mandala design for you.
    """)

# Function to generate the mandala image
def generate_mandala(prompt, api_key):
    if not api_key:
        return None, "Please enter an OpenAI API key in the sidebar."
    
    openai.api_key = api_key
    
    # Enhance the prompt to create a mandala
    enhanced_prompt = f"Create a detailed black and white symmetric mandala design inspired by the concept of '{prompt}'. The mandala should be intricate, perfectly symmetrical, and feature detailed patterns. Use only black and white colors with clear contrast. The design should be centered and circular with radiating patterns. Make it high-resolution and suitable for printing."
    
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            style="vivid"
        )
        
        image_url = response.data[0].url
        
        # Download the image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        
        return image, None
    except Exception as e:
        return None, f"Error: {str(e)}"

# Function to create a download link for the image
def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">Download {text}</a>'
    return href

# Main app layout
word_inspiration = st.text_input("Enter a word for inspiration:", placeholder="e.g., ocean, serenity, forest, cosmos")

generate_button = st.button("Generate Mandala Art")

# Store generated image in session state
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
    st.session_state.error_message = None
    st.session_state.last_prompt = None

# Generate image when button is clicked
if generate_button and word_inspiration:
    with st.spinner("Creating your mandala art..."):
        image, error = generate_mandala(word_inspiration, api_key)
        st.session_state.generated_image = image
        st.session_state.error_message = error
        st.session_state.last_prompt = word_inspiration

# Display image or error
if st.session_state.generated_image:
    st.markdown(f"### Mandala inspired by: '{st.session_state.last_prompt}'")
    # Fixed: Replaced deprecated use_column_width with use_container_width
    st.image(st.session_state.generated_image, use_container_width=True)
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mandala_{st.session_state.last_prompt}_{timestamp}.png"
    
    # Create download button
    st.markdown(get_image_download_link(st.session_state.generated_image, filename, "Image"), unsafe_allow_html=True)
    
    # Additional download options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save as High Resolution"):
            # Save high resolution version
            high_res_filename = f"mandala_{st.session_state.last_prompt}_{timestamp}_high_res.png"
            st.session_state.generated_image.save(high_res_filename, "PNG")
            st.success(f"High resolution image saved as {high_res_filename}")
    
    with col2:
        if st.button("Generate Another"):
            st.session_state.generated_image = None
            st.session_state.last_prompt = None
            st.experimental_rerun()

elif st.session_state.error_message:
    st.error(st.session_state.error_message)

# Display examples and tips at the bottom
with st.expander("Tips for better mandalas"):
    st.markdown("""
    - Try using abstract concepts like "tranquility", "harmony", or "infinity"
    - Nature-related words often create beautiful patterns
    - Emotional words can lead to interesting designs
    - Try combining words like "ocean-calm" or "forest-mystery"
    """)