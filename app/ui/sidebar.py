import streamlit as st
from app.config import Config

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key Management
        api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY or "")
        if api_key:
            Config.OPENAI_API_KEY = api_key
            # In a real app, we might want to re-init DSPy here if changed
        
        st.divider()
        
        # Output Format Selection
        st.subheader("🧠 Cognition Mode")
        output_format = st.radio(
            "Output Structure",
            options=["text", "toon", "baml"],
            index=0,
            help="Choose how the AI structures its internal thought process."
        )
        
        st.info(
            f"""
            **Current Mode: {output_format.upper()}**
            
            - **Text**: Standard unstructured response.
            - **TOON**: Token-Oriented Object Notation (Compact).
            - **BAML**: Strongly Typed Object (Reliable).
            """
        )
        
        return {"output_format": output_format}
