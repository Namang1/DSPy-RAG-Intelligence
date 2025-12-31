# DSPy Self-Optimizing RAG System

> **Not just another RAG.** This system *learns* from your interactions and *optimizes* its own prompts to get smarter over time.

A next-generation Retrieval-Augmented Generation (RAG) system built with **DSPy** and **Milvus**, designed to demonstrate the power of **Agency** and **Self-Optimization**.

##  Why This is Different

Most RAG systems are black boxes. This one is a **Glass Box**.

1.  ** "Transparent Brain" UI**:
    *   Watch the AI **think**, **retrieve**, and **critique** itself in real-time.
    *   See the raw Structured Output (TOON/BAML) and the internal Confidence Scores.

2.  ** Self-Correcting (Critic Loop)**:
    *   Example: If the answer is "Python is a snake", the Critic Agent intervenes: *"Too literal. The user asks about coding."*
    *   The **Revision Agent** then fixes it *before* you see the result.

3.  ** Human-in-the-Loop Teaching**:
    *   **You are the teacher.** If the AI makes a mistake, click **"Correct this answer"** in the UI.
    *   Your correction is saved as a "Golden Example" to `data/feedback.jsonl`.
    *   DSPy uses this data to **compile and optimize** its own prompts automatically.

##  Tech Stack

*   **Orchestration & Logic**: [DSPy](https://github.com/stanfordnlp/dspy) (Declarative Self-improving Python)
*   **Vector Database**: [Milvus](https://milvus.io/) (via Docker)
*   **Embeddings**: `sentence-transformers` (Local & Fast)
*   **LLMs**: OpenAI (GPT-4o) / Anthropic (Claude 3.5 Sonnet)
*   **UI**: Streamlit (clean, interactive, and fast)

##  Quick Start

### Prerequisites
*   Python 3.9+
*   Docker & Docker Compose (for Milvus)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/DSPy-RAG-Intelligence.git
    cd DSPy-RAG-Intelligence
    ```

2.  **Start Milvus Vector Database**
    ```bash
    docker-compose up -d
    ```

3.  **Install Dependencies (The Fast Way with `uv`)**
    This project uses [uv](https://github.com/astral-sh/uv) for lightning-fast dependency management.

    ```bash
    # Install uv (if you haven't already)
    pip install uv

    # Create virtualenv and install dependencies
    uv venv
    source .venv/bin/activate
    uv pip install -e .
    ```


4.  **Configure Environment**
    Copy `.env.example` to `.env` and add your API keys:
    ```bash
    cp .env.example .env
    # Edit .env with your OPENAI_API_KEY
    ```

5.  **Run the App**
    ```bash
    streamlit run app/ui/main.py
    ```

## 📂 Project Structure

```text
DSPy-RAG-Intelligence/
├── app/
│   ├── infrastructure/   # Milvus & Embedding wrappers
│   ├── core/             # DSPy Modules (QueryUnderstanding, RAG, etc.)
│   ├── pipeline/         # Orchestrators
│   └── ui/               # Streamlit Dashboard
├── data/                 # Local data storage
├── scripts/              # Indexing & Optimization scripts
└── docker-compose.yml    # Infrastructure setup
```
