import streamlit as st
import dspy
from app.config import Config
from app.pipeline.rag_pipeline import RAGPipeline
from app.ui.sidebar import render_sidebar
from app.ui.dashboard import render_dashboard
from app.core.optimization.feedback import FeedbackManager

# Initialize Feedback Manager
feedback_manager = FeedbackManager()

st.set_page_config(
    page_title="DSPy Transparent Brain",
    page_icon="🧠",
    layout="wide"
)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize Pipeline if not ready
    if "rag_pipeline" not in st.session_state:
        # We start with default 'text' but will update if sidebar changes
        # Ideally, we allow dynamic config in the pipeline call
        pass

def main():
    init_session_state()
    
    st.title("🧠 DSPy Self-Optimizing RAG")
    st.caption("Powered by Milvus, DSPy, TOON, and BAML")
    
    # Render Sidebar
    config = render_sidebar()
    output_format = config["output_format"]
    
    # Initialize RAG (lazy init or update on change)
    # For simplicity, we assume RAG is cheap to init or we just pass config
    # But since DSPy modules are stateful, we should ideally keep it.
    # However, 'output_format' changes the AnswerGenerator structure significantly.
    # So we might need to re-instantiate or have the pipeline accept the format at runtime.
    # Our RAGPipeline currently takes output_format in __init__.
    
@st.cache_resource
def setup_dspy():
    # Initialize DSPy globally once
    lm = dspy.LM("openai/gpt-4o-mini", api_key=Config.OPENAI_API_KEY)
    dspy.configure(lm=lm)
    return lm

def main():
    init_session_state()
    setup_dspy()
    
    setup_dspy()
    
    st.title("🧠 DSPy Self-Optimizing RAG")
    st.caption("Powered by Milvus, DSPy, TOON, and BAML")
    
    # Render Sidebar
    config = render_sidebar()
    output_format = config["output_format"]
    
    # Tabs
    tab_chat, tab_dashboard = st.tabs(["💬 Chat", "📊 Dashboard"])
    
    with tab_dashboard:
        render_dashboard()
        
    with tab_chat:
        # Initialize RAG (lazy init or update on change)
        if "current_format" not in st.session_state or st.session_state.current_format != output_format:
            st.session_state.rag_pipeline = RAGPipeline(output_format=output_format)
            st.session_state.current_format = output_format

        # Chat Interface
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "details" in message:
                    with st.expander("🧠 Transparent Brain (Internal Monologue)"):
                        st.json(message["details"])
                    if "critic_history" in message and message["critic_history"]:
                        with st.expander("🕵️ Critic Loop (Self-Correction)"):
                            st.write(" The system critiqued and revised its answer:")
                            for step in message["critic_history"]:
                                st.divider()
                                st.markdown(f"**Iteration {step['iteration']}** (Score: {step['score']}/10)")
                                st.caption(f"Critique: {step['critique']}")
                                if step.get('passed'):
                                    st.success("Pass! ✅")

        if prompt := st.chat_input("Ask a tough question..."):
            # User message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Assistant message
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                brain_placeholder = st.empty()
                critic_placeholder = st.empty()
                
                with st.spinner("Thinking & retrieving..."):
                    try:
                        # Run Pipeline
                        pipeline = st.session_state.rag_pipeline
                        prediction = pipeline(user_query=prompt)
                        
                        # Display Answer
                        # prediction.answer might be an object if BAML, handled by AnswerGenerator mapping
                        answer_text = prediction.answer
                        message_placeholder.markdown(answer_text)
                        
                        # Visualize "Brain" details
                        details = {
                            "confidence": getattr(prediction, "confidence", "N/A"),
                            "sources": getattr(prediction, "sources", []),
                            "retrieved_context": getattr(prediction, "context", [])[:3], # Show top 3
                        }
                        
                        if output_format == "toon":
                            details["raw_format"] = prediction.raw_toon
                        elif output_format == "baml":
                             details["raw_format"] = str(getattr(prediction, "raw_baml", "N/A"))
                        
                        with brain_placeholder.expander("🧠 Transparent Brain (Internal Monologue)"):
                            st.json(details)
                        
                        # Visualize Critic History
                        critic_history = getattr(prediction, "critic_history", [])
                        if critic_history:
                            with critic_placeholder.expander("🕵️ Critic Loop (Self-Correction)"):
                                st.write(" The system critiqued and revised its answer:")
                                for step in critic_history:
                                    st.divider()
                                    st.markdown(f"**Iteration {step['iteration']}** (Score: {step['score']}/10)")
                                    st.caption(f"Critique: {step['critique']}")
                                    if step.get('passed'):
                                        st.success("Pass! ✅")
                        
                        # Save to history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer_text,
                            "details": details,
                            "critic_history": critic_history
                        })
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

        # ---------------------------------------------------------
        # Human-in-the-Loop Feedback Section
        # ---------------------------------------------------------
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
            last_msg = st.session_state.messages[-1]
            last_user_msg = st.session_state.messages[-2] if len(st.session_state.messages) > 1 else None
            
            if last_user_msg and last_user_msg["role"] == "user":
                st.divider()
                st.caption("👨‍🏫 Teach the Agent (Human-in-the-Loop)")
                
                with st.expander("📝 Correct this answer (Add to Training Data)"):
                    with st.form("feedback_form"):
                        question = last_user_msg["content"]
                        current_answer = last_msg["content"]
                        
                        st.write(f"**Question:** {question}")
                        corrected_answer = st.text_area("Corrected Answer", value=current_answer, height=150)
                        score = st.slider("Quality Score (1-10)", 1, 10, 5)
                        
                        if st.form_submit_button("Submit Correction"):
                            feedback_manager.save_feedback(
                                question=question,
                                initial_answer=current_answer,
                                corrected_answer=corrected_answer,
                                score=score,
                                metadata={"output_format": st.session_state.current_format}
                            )
                            st.success("Feedback saved! This example will be used to compile and optimize the agent.")

if __name__ == "__main__":
    main()
