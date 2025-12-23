import streamlit as st
import pandas as pd
from app.core.optimization.feedback import FeedbackManager

def render_dashboard():
    st.header("📊 Knowledge Base & Optimization Dashboard")
    
    fm = FeedbackManager()
    examples = fm.load_examples()
    
    if not examples:
        st.info("No feedback data collected yet. Start using the Chat to teach the agent!")
        return

    # Convert to DataFrame for display
    df = pd.DataFrame(examples)
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total User Corrections", len(df))
    col2.metric("Avg. Quality Score", f"{df['score'].mean():.2f}/10")
    col3.metric("Last Update", pd.to_datetime(df['timestamp']).max().strftime("%Y-%m-%d %H:%M"))
    
    st.divider()
    
    # Data View
    st.subheader("📝 Golden Examples (Training Data)")
    st.caption("This data will be used to compile/optimize the DSPy modules.")
    
    st.dataframe(
        df[["timestamp", "question", "corrected_answer", "score", "metadata"]],
        use_container_width=True,
        hide_index=True
    )
    
    # Simple Download
    st.download_button(
        label="Download Training Data (JSONL)",
        data=open(fm.filepath).read(),
        file_name="feedback.jsonl",
        mime="application/json"
    )
