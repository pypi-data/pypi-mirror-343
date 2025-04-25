"""Styling utilities for Acroplans branding."""

import streamlit as st

# Acroplans brand colors with complete information
BRAND_COLORS = {
    # Blue (primary) - RoyalBlue
    "primary": "#155fac",                  # HEX
    "primary_rgb": "rgb(21, 95, 172)",     # RGB
    "primary_hsl": "hsl(210.7, 78.1%, 37.6%)",  # HSL
    
    # Orange (secondary)
    "secondary": "#fdb31a",                  # HEX
    "secondary_rgb": "rgb(253, 179, 26)",    # RGB
    "secondary_hsl": "hsl(41.4, 83%, 59.9%)", # HSL
    
    # Supporting colors
    "accent": "#F8F9FA",        # Light accent color
    "background": "#FFFFFF",    # White background
    "text": "#212529",          # Text color
    "success": "#37B76A",       # Success color
    "warning": "#FFC107",       # Warning color
    "error": "#DC3545",         # Error color
}

def get_color_palette():
    """Return the Acroplans color palette."""
    return BRAND_COLORS

def apply_corporate_theme():
    """Apply the Acroplans corporate theme to the Streamlit app."""
    # CSS for custom styling
    custom_css = f"""
    <style>
        /* Main elements */
        .reportview-container .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: {BRAND_COLORS['primary']};
            font-family: 'Segoe UI', sans-serif;
        }}
        
        /* Buttons */
        .stButton>button {{
            background-color: {BRAND_COLORS['primary']};
            color: white;
            border-radius: 4px;
            border: none;
            padding: 0.5rem 1rem;
        }}
        .stButton>button:hover {{
            background-color: {BRAND_COLORS['secondary']};
        }}
        
        /* Sidebar */
        .sidebar .sidebar-content {{
            background-color: {BRAND_COLORS['background']};
        }}
        
        /* Custom DocMind class */
        .docmind-container {{
            border: 1px solid {BRAND_COLORS['accent']};
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            background-color: rgba(255, 209, 102, 0.05);
        }}
    </style>
    """
    
    # Inject custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)