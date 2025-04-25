"""UI components for Acroplans branding."""

import os
import base64
import streamlit as st
from PIL import Image
import pkg_resources

# Helper function to get asset path
def get_asset_path(filename):
    """Get the absolute path to an asset file."""
    return pkg_resources.resource_filename("acroplans_branding", f"assets/{filename}")

def get_image_base64(image_path):
    """Convert an image to base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def display_logo(width=None):
    """Display the Acroplans logo.
    
    Args:
        width: Optional width to display the logo
    """
    logo_path = get_asset_path("logo.png")
    image = Image.open(logo_path)
    
    if width:
        st.image(image, width=width)
    else:
        st.image(image)
    
    return image

def display_branded_header(title, subtitle=None, show_logo=True):
    """Display a branded header with optional logo.

    Args:
        title: Main title text
        subtitle: Optional subtitle text
        show_logo: Whether to show the logo
    """
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if show_logo:
            display_logo(width=100)
    
    with col2:
        st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<h3>{subtitle}</h3>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

def display_branded_footer():
    """Display a consistent branded footer."""
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        display_logo(width=50)
    
    with col2:
        st.markdown("© 2025 Acroplans. All rights reserved.")
    
    with col3:
        st.markdown("[Visit Website](https://www.acroplans.com/)")