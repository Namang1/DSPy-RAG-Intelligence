# 09. Implemented Enhancements & Deviations

This document tracks features and architectural decisions implemented that extend beyond or deviate from the original requirements.

## 1. Custom TOON Regex Parser
**Deviation**: The original requirement suggested using the `toon-python` library.
**Implementation**: Due to runtime issues (`ModuleNotFoundError` and `AttributeError`), we implemented a robust **Custom Regex Parser** (`app/core/parsers/toon_parser.py`).
*   **Why**: To ensure stability and handle LLM output quirks (like markdown code fencing) that strict libraries might reject.
*   **Result**: The system can now parse loosely formatted TOON outputs resiliently.

## 2. Dual Structured Output Support (Adapter Pattern)
**Enhancement**: The system was required to support structured output, but we implemented a **Dynamic Switch** between **TOON** and **BAML**.
*   **Implementation**: `AnswerGenerator` acts as an adapter.
*   **UI Integration**: Users can toggle between `text`, `toon`, and `baml` modes in the Sidebar at runtime. This allows for A/B testing of output formats.

## 3. "Transparent Brain" Visualization
**Enhancement**: We went beyond standard logging to create a "Glass Box" UI.
*   **Internal Monologue**: The Streamlit UI exposes the internal `confidence`, `sources`, and `raw_format` parsing via expanders.
*   **Critic Loop Visualization**: We specifically visualize the multi-turn dialogue between the **Critic** and **Reviser** agents, showing the `Correction Iterations` and `Quality Scores` to the user in real-time.

## 4. Human-in-the-Loop Feedback System
**Enhancement**: We implemented a complete feedback loop for future optimization.
*   **FeedbackManager**: A persistent storage class (`app/core/optimization/feedback.py`) that saves data to `data/feedback.jsonl`.
*   **UI Integration**: Added a "Teach the Agent" form allowing users to:
    1.  Edit the agent's answer.
    2.  Rate the quality (1-10).
    3.  Save the correction as a "Golden Example" for DSPy compilation.

## 5. Knowledge Dashboard
**Enhancement**: Added a dedicated **Dashboard Tab** in the UI.
*   **Purpose**: To verify and manage the collected training data.
*   **Features**: View KPIs (Total Corrections, Avg Score) and download the dataset as JSONL.
