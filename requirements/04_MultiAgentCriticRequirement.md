# Multi-Agent Critic Loop Requirement Specification

## 1. Introduction

### Purpose
This document specifies the functional and non-functional requirements for the Multi-Agent Critic Loop component of the DSPy Self-Optimizing RAG System. The Multi-Agent Critic Loop implements an iterative refinement mechanism where a Critic Agent analyzes generated answers and a Revision Agent improves them based on critiques.

### Scope
**In-Scope:**
- CriticAgent module for answer analysis and issue identification
- RevisionAgent module for answer improvement
- Iterative refinement loop with convergence criteria
- Scoring and improvement tracking
- Integration with RAG Pipeline and BAML Validator

**Out-of-Scope:**
- Initial answer generation (covered in RAG Pipeline Requirements)
- Output validation and schema enforcement (covered in BAML Validator Requirements)
- UI display of critic loop (covered in UI Component Requirements)
- Evaluation metrics collection (covered in Evaluation Dashboard Requirements)

### Assumptions
- Initial answer is provided by AnswerGenerator module
- LLM providers are configured and available
- DSPy framework supports multi-agent patterns
- Small-scale deployment: <100 queries/day
- Maximum iteration limit is configurable (default: 3)

### Glossary
- **Critic Agent**: An AI agent that analyzes answers and identifies issues (logical, factual, safety, ambiguity)
- **Revision Agent**: An AI agent that improves answers based on critiques
- **Critique**: A structured analysis identifying issues in an answer
- **Convergence**: The state where no significant improvements are made between iterations
- **Improvement Delta**: The difference in quality scores between iterations

## 2. Functional Requirements

### 2.1 CriticAgent Module

**REQ-CRITIC-001**: The system SHALL provide a CriticAgent DSPy module that analyzes generated answers and identifies issues.

**REQ-CRITIC-002**: The CriticAgent module SHALL accept as input:
- Generated answer text
- Original query
- Evidence chunks used
- Reasoning steps (if available)

**REQ-CRITIC-003**: The CriticAgent module SHALL identify the following types of issues:
- Logical inconsistencies
- Factual inaccuracies
- Safety concerns (harmful content, bias)
- Ambiguity or unclear statements
- Missing information
- Incomplete reasoning

**REQ-CRITIC-004**: The CriticAgent module SHALL output a structured critique including:
- List of identified issues (with types and severity)
- Issue descriptions
- Suggested improvements
- Overall quality score (0.0 to 1.0)
- Confidence in critique (0.0 to 1.0)

**REQ-CRITIC-005**: The CriticAgent module SHALL provide reasoning for each identified issue.

**REQ-CRITIC-006**: The CriticAgent module SHALL support multiple LLM providers (OpenAI, Anthropic, local models).

**REQ-CRITIC-007**: The CriticAgent module SHALL be optimizable using DSPy optimizers.

### 2.2 RevisionAgent Module

**REQ-CRITIC-008**: The system SHALL provide a RevisionAgent DSPy module that improves answers based on critiques.

**REQ-CRITIC-009**: The RevisionAgent module SHALL accept as input:
- Original answer
- Critique from CriticAgent
- Original query
- Evidence chunks used

**REQ-CRITIC-010**: The RevisionAgent module SHALL generate an improved answer that addresses identified issues.

**REQ-CRITIC-011**: The RevisionAgent module SHALL output:
- Revised answer text
- Explanation of changes made
- Updated confidence score
- List of issues addressed

**REQ-CRITIC-012**: The RevisionAgent module SHALL preserve correct information from the original answer.

**REQ-CRITIC-013**: The RevisionAgent module SHALL support multiple LLM providers (OpenAI, Anthropic, local models).

**REQ-CRITIC-014**: The RevisionAgent module SHALL be optimizable using DSPy optimizers.

### 2.3 Iterative Refinement Loop

**REQ-CRITIC-015**: The system SHALL implement an iterative refinement loop that:
1. Generates initial answer (from AnswerGenerator)
2. CriticAgent analyzes the answer
3. RevisionAgent improves the answer
4. Repeats steps 2-3 until convergence or max iterations

**REQ-CRITIC-016**: The refinement loop SHALL support configurable maximum iterations (default: 3, range: 1-5).

**REQ-CRITIC-017**: The refinement loop SHALL terminate early if:
- Quality score improves by less than a threshold (default: 0.05) between iterations
- No major issues are identified by CriticAgent
- Maximum iterations reached

**REQ-CRITIC-018**: The refinement loop SHALL track improvement delta (change in quality score) between iterations.

**REQ-CRITIC-019**: The refinement loop SHALL return the best answer across all iterations (highest quality score).

**REQ-CRITIC-020**: The refinement loop SHALL provide a summary of all iterations including:
- Iteration number
- Quality score per iteration
- Issues identified per iteration
- Changes made per iteration

### 2.4 Scoring and Quality Metrics

**REQ-CRITIC-021**: The system SHALL calculate quality scores for answers using the CriticAgent.

**REQ-CRITIC-022**: Quality scores SHALL be normalized to a range of 0.0 to 1.0.

**REQ-CRITIC-023**: The system SHALL track improvement delta (difference in quality scores between iterations).

**REQ-CRITIC-024**: The system SHALL calculate improvement percentage: ((final_score - initial_score) / initial_score) * 100.

**REQ-CRITIC-025**: The system SHALL log quality scores and improvement metrics for evaluation.

### 2.5 Integration with RAG Pipeline

**REQ-CRITIC-026**: The Multi-Agent Critic Loop SHALL integrate with the AnswerGenerator module from the RAG Pipeline.

**REQ-CRITIC-027**: The Multi-Agent Critic Loop SHALL receive evidence chunks and reasoning from the RAG Pipeline.

**REQ-CRITIC-028**: The Multi-Agent Critic Loop SHALL pass improved answers to the BAML Validator.

**REQ-CRITIC-029**: The Multi-Agent Critic Loop SHALL be wrapped in a DSPy Module for optimization.

### 2.6 Error Handling

**REQ-CRITIC-030**: The system SHALL handle CriticAgent failures gracefully:
- If critique generation fails, return original answer with warning
- Log error and continue with next iteration or terminate

**REQ-CRITIC-031**: The system SHALL handle RevisionAgent failures gracefully:
- If revision fails, return previous iteration's answer
- Log error and terminate loop

**REQ-CRITIC-032**: The system SHALL handle LLM API failures with retry logic (max 2 retries per agent call).

## 3. Non-Functional Requirements

### 3.1 Performance

**REQ-CRITIC-NFR-001**: The CriticAgent module SHALL complete analysis within 15 seconds for 95% of queries (p95 latency).

**REQ-CRITIC-NFR-002**: The RevisionAgent module SHALL complete revision within 15 seconds for 95% of queries (p95 latency).

**REQ-CRITIC-NFR-003**: A single iteration (critic + revision) SHALL complete within 35 seconds for 95% of queries (p95 latency).

**REQ-CRITIC-NFR-004**: The full refinement loop (3 iterations max) SHALL complete within 90 seconds for 95% of queries (p95 latency).

**REQ-CRITIC-NFR-005**: The system SHALL support early termination to reduce latency when no improvements are detected.

### 3.2 Quality

**REQ-CRITIC-NFR-006**: The CriticAgent SHALL identify at least 80% of actual issues in answers (precision).

**REQ-CRITIC-NFR-007**: The RevisionAgent SHALL improve answer quality by at least 10% (quality score improvement) for 70% of cases.

**REQ-CRITIC-NFR-008**: The refinement loop SHALL converge (no significant improvement) within 3 iterations for 80% of queries.

### 3.3 Reliability

**REQ-CRITIC-NFR-009**: The system SHALL handle LLM API rate limits gracefully with exponential backoff.

**REQ-CRITIC-NFR-010**: The system SHALL not degrade answer quality if critic loop fails (fallback to original answer).

**REQ-CRITIC-NFR-011**: The system SHALL prevent infinite loops by enforcing maximum iteration limit.

### 3.4 Resource Usage

**REQ-CRITIC-NFR-012**: The system SHALL track token usage for both CriticAgent and RevisionAgent calls.

**REQ-CRITIC-NFR-013**: The system SHALL optimize token usage by reusing context where possible.

## 4. Interfaces & Contracts

### 4.1 CriticAgent Module Interface

**Input Schema:**
```python
class CriticAgentInput:
    answer: str  # Generated answer to critique
    original_query: str  # Original user query
    evidence_chunks: List[EvidenceChunk]  # Evidence used
    reasoning_steps: Optional[List[str]]  # CoT reasoning steps
    iteration_number: int  # Current iteration (1-based)
```

**Output Schema:**
```python
class Issue:
    issue_type: str  # "logical", "factual", "safety", "ambiguity", "missing_info", "incomplete_reasoning"
    severity: str  # "critical", "high", "medium", "low"
    description: str  # Description of the issue
    location: Optional[str]  # Part of answer where issue occurs
    suggestion: str  # Suggested improvement

class CriticAgentOutput:
    issues: List[Issue]  # List of identified issues
    overall_quality_score: float  # 0.0 to 1.0
    critique_confidence: float  # 0.0 to 1.0
    critique_reasoning: str  # Explanation of critique
    has_major_issues: bool  # True if critical or high severity issues found
```

**DSPy Signature:**
```python
class CriticAgent(dspy.Module):
    def __init__(self, llm_provider="openai", model_name="gpt-4"):
        self.llm = dspy.LM(model=f"{llm_provider}:{model_name}")
        self.critic = dspy.ChainOfThought(
            "answer, original_query, evidence_chunks -> issues, overall_quality_score, critique_reasoning"
        )
```

### 4.2 RevisionAgent Module Interface

**Input Schema:**
```python
class RevisionAgentInput:
    original_answer: str  # Answer to improve
    critique: CriticAgentOutput  # Critique from CriticAgent
    original_query: str  # Original user query
    evidence_chunks: List[EvidenceChunk]  # Evidence used
    iteration_number: int  # Current iteration
```

**Output Schema:**
```python
class RevisionAgentOutput:
    revised_answer: str  # Improved answer
    changes_explanation: str  # Explanation of changes made
    updated_confidence: float  # Updated confidence score (0.0 to 1.0)
    issues_addressed: List[str]  # List of issue IDs or descriptions addressed
    preserved_content: List[str]  # Parts of original answer preserved
```

**DSPy Signature:**
```python
class RevisionAgent(dspy.Module):
    def __init__(self, llm_provider="openai", model_name="gpt-4"):
        self.llm = dspy.LM(model=f"{llm_provider}:{model_name}")
        self.revision = dspy.ChainOfThought(
            "original_answer, critique, original_query -> revised_answer, changes_explanation, updated_confidence"
        )
```

### 4.3 Multi-Agent Critic Loop Interface

**Input Schema:**
```python
class CriticLoopInput:
    initial_answer: str  # Answer from AnswerGenerator
    original_query: str  # Original user query
    evidence_chunks: List[EvidenceChunk]  # Evidence used
    reasoning_steps: Optional[List[str]]  # CoT reasoning
    max_iterations: int = 3  # Maximum iterations
    improvement_threshold: float = 0.05  # Minimum improvement to continue
```

**Output Schema:**
```python
class IterationResult:
    iteration_number: int
    answer: str
    quality_score: float
    issues_identified: List[Issue]
    changes_made: str
    improvement_delta: float  # Change from previous iteration

class CriticLoopOutput:
    final_answer: str  # Best answer across all iterations
    final_quality_score: float
    iterations: List[IterationResult]  # All iteration results
    total_iterations: int
    improvement_percentage: float  # Overall improvement from initial
    converged: bool  # True if loop terminated due to convergence
    termination_reason: str  # "max_iterations", "convergence", "no_issues", "error"
```

**DSPy Module Wrapper:**
```python
class MultiAgentCriticLoop(dspy.Module):
    def __init__(self, critic_agent, revision_agent, max_iterations=3):
        self.critic_agent = critic_agent
        self.revision_agent = revision_agent
        self.max_iterations = max_iterations
```

### 4.4 Error Codes

| Error Code | Description | HTTP Equivalent |
|------------|-------------|-----------------|
| CRITIC-ERR-001 | CriticAgent execution failure | 500 Internal Server Error |
| CRITIC-ERR-002 | RevisionAgent execution failure | 500 Internal Server Error |
| CRITIC-ERR-003 | LLM API failure in critic loop | 502 Bad Gateway |
| CRITIC-ERR-004 | Maximum iterations reached without convergence | 200 OK (with warning) |
| CRITIC-ERR-005 | Invalid critique format | 500 Internal Server Error |
| CRITIC-ERR-006 | Invalid revision format | 500 Internal Server Error |

## 5. Tenant & Security Considerations

### 5.1 Multi-Tenancy
**REQ-CRITIC-SEC-001**: The system SHALL support single-tenant operation for local deployment (no multi-tenancy required).

### 5.2 Authentication & Authorization
**REQ-CRITIC-SEC-002**: The system SHALL use the same LLM provider credentials as the RAG Pipeline.

### 5.3 Data Privacy
**REQ-CRITIC-SEC-003**: The system SHALL not log sensitive answer content in production logs (configurable).

**REQ-CRITIC-SEC-004**: The system SHALL allow configuration of data retention for critique and revision logs.

## 6. Observability & Telemetry

### 6.1 Metrics

**REQ-CRITIC-OBS-001**: The system SHALL track the following metrics:
- CriticAgent execution time (histogram)
- RevisionAgent execution time (histogram)
- Total refinement loop duration (histogram)
- Number of iterations per query (histogram)
- Quality score improvement delta (histogram)
- Improvement percentage (histogram)
- Convergence rate (percentage of queries that converge)
- Issue identification rate (issues per answer, histogram)
- LLM token usage for critic loop (counter)

### 6.2 Logging

**REQ-CRITIC-OBS-002**: The system SHALL log at INFO level:
- Critic loop start/end with iteration count
- Quality scores per iteration
- Improvement delta per iteration
- Convergence status

**REQ-CRITIC-OBS-003**: The system SHALL log at ERROR level:
- CriticAgent failures
- RevisionAgent failures
- LLM API failures
- Loop termination due to errors

**REQ-CRITIC-OBS-004**: The system SHALL log at DEBUG level:
- Full critique output
- Full revision output
- Issue details
- Change explanations

### 6.3 Health Checks

**REQ-CRITIC-OBS-005**: The system SHALL verify CriticAgent and RevisionAgent module initialization in health checks.

## 7. Compliance & Governance

### 7.1 Audit Logging

**REQ-CRITIC-COMP-001**: The system SHALL log all critic loop executions with:
- Timestamp
- Query identifier
- Number of iterations
- Final quality score
- Improvement percentage
- Termination reason

### 7.2 Data Retention

**REQ-CRITIC-COMP-002**: The system SHALL support configurable retention for critique and revision data (default: 30 days).

## 8. Open Questions & Assumptions

### Open Questions

1. **Q1**: Should the CriticAgent and RevisionAgent use the same LLM model or different models? (Assumed: Same model, configurable)
2. **Q2**: Should the system support different critique strategies (strict vs. lenient)? (Assumed: Single strategy, configurable severity thresholds)
3. **Q3**: What is the optimal maximum iteration limit? (Assumed: 3, configurable)
4. **Q4**: Should the system support parallel critique of multiple answer candidates? (Assumed: Sequential processing for initial version)
5. **Q5**: Should quality scores be calibrated against human evaluation? (Assumed: Internal scoring, calibration in future)

### Assumptions

1. CriticAgent and RevisionAgent can use the same LLM provider
2. Quality scores are relative and may not be directly comparable across different queries
3. Improvement threshold of 0.05 is reasonable for detecting meaningful improvements
4. Maximum 3 iterations is sufficient for most cases
5. Early termination improves user experience without significant quality loss
6. DSPy optimization can improve both CriticAgent and RevisionAgent performance

