# BAML Validator Requirement Specification

## 1. Introduction

### Purpose
This document specifies the functional and non-functional requirements for the BAML (Binary Application Markup Language) Validator component of the DSPy Self-Optimizing RAG System. The BAML Validator enforces strict output structure, validates types, and ensures deterministic output formatting for the RAG system.

### Scope
**In-Scope:**
- BAML schema definition and enforcement
- Output validation and type checking
- Retry mechanism on invalid output
- Structured output generation (FinalAnswer schema)
- Integration with AnswerGenerator and RevisionAgent
- Error handling and recovery

**Out-of-Scope:**
- Answer generation logic (covered in RAG Pipeline Requirements)
- Answer improvement logic (covered in Multi-Agent Critic Requirements)
- UI display of validation results (covered in UI Component Requirements)
- Caching of validated outputs (covered in Caching Layer Requirements)

### Assumptions
- BAML framework is installed and configured
- LLM providers support structured output generation
- Answers are generated in text format before validation
- Small-scale deployment: <100 queries/day
- Validation failures are retryable

### Glossary
- **BAML**: Binary Application Markup Language, a schema definition language for structured LLM outputs
- **Schema**: A BAML definition that specifies the expected structure and types of output
- **Validation**: The process of checking if output conforms to the defined schema
- **Retry**: Attempting to regenerate output when validation fails
- **FinalAnswer**: The structured output schema for validated answers

## 2. Functional Requirements

### 2.1 Schema Definition

**REQ-BAML-001**: The system SHALL define a BAML schema for the FinalAnswer structure.

**REQ-BAML-002**: The FinalAnswer schema SHALL include the following fields:
- `answer`: string (required) - The final answer text
- `confidence`: float (required) - Confidence score between 0.0 and 1.0
- `sources`: array of strings (required) - List of source document identifiers
- `reasoning`: string (optional) - Explanation or reasoning for the answer
- `metadata`: object (optional) - Additional metadata (timestamp, model used, etc.)

**REQ-BAML-003**: The system SHALL support custom BAML schema definitions for different answer types.

**REQ-BAML-004**: The system SHALL validate schema definitions at initialization time.

**REQ-BAML-005**: The system SHALL provide schema versioning support (v1, v2, etc.).

### 2.2 Output Validation

**REQ-BAML-006**: The system SHALL validate all answers from AnswerGenerator before returning to users.

**REQ-BAML-007**: The system SHALL validate all revised answers from RevisionAgent before accepting them.

**REQ-BAML-008**: The validator SHALL check:
- Required fields are present
- Field types match schema definition (string, float, array, object)
- Value constraints are met (e.g., confidence in 0.0-1.0 range)
- Array elements conform to expected types
- Object structure matches schema

**REQ-BAML-009**: The validator SHALL provide detailed error messages for validation failures including:
- Field name that failed validation
- Expected type vs. actual type
- Constraint violations
- Missing required fields

**REQ-BAML-010**: The validator SHALL handle partial validation failures gracefully (identify all issues, not just first).

### 2.3 Retry Mechanism

**REQ-BAML-011**: The system SHALL implement a retry mechanism when validation fails.

**REQ-BAML-012**: The retry mechanism SHALL support configurable maximum retry attempts (default: 3, range: 1-5).

**REQ-BAML-013**: The retry mechanism SHALL pass validation errors back to the AnswerGenerator or RevisionAgent for correction.

**REQ-BAML-014**: The retry mechanism SHALL use exponential backoff between retries (1s, 2s, 4s).

**REQ-BAML-015**: The system SHALL track retry attempts and include them in logs and metrics.

**REQ-BAML-016**: The system SHALL return the last attempt's output (even if invalid) if max retries are exceeded, with a validation error flag.

### 2.4 Structured Output Generation

**REQ-BAML-017**: The system SHALL enforce structured output generation using BAML schemas.

**REQ-BAML-018**: The system SHALL convert validated outputs to the FinalAnswer schema format.

**REQ-BAML-019**: The system SHALL ensure deterministic output formatting (consistent structure across calls).

**REQ-BAML-020**: The system SHALL preserve all required information from the original answer in the structured format.

**REQ-BAML-021**: The system SHALL handle optional fields gracefully (include if present, omit if not).

### 2.5 Integration with Answer Generation

**REQ-BAML-022**: The validator SHALL integrate with AnswerGenerator module from RAG Pipeline.

**REQ-BAML-023**: The validator SHALL integrate with RevisionAgent module from Multi-Agent Critic Loop.

**REQ-BAML-024**: The validator SHALL be called after each answer generation or revision attempt.

**REQ-BAML-025**: The validator SHALL provide feedback to generation modules to improve structured output quality.

### 2.6 Error Handling

**REQ-BAML-026**: The system SHALL handle BAML framework errors gracefully:
- Schema parsing errors
- Validation runtime errors
- Type conversion errors

**REQ-BAML-027**: The system SHALL log all validation errors with context (query, answer attempt, error details).

**REQ-BAML-028**: The system SHALL provide fallback behavior when validation consistently fails (return unstructured answer with warning).

## 3. Non-Functional Requirements

### 3.1 Performance

**REQ-BAML-NFR-001**: The validator SHALL complete validation within 1 second for 95% of validations (p95 latency).

**REQ-BAML-NFR-002**: The validator SHALL complete validation within 2 seconds for 99% of validations (p99 latency).

**REQ-BAML-NFR-003**: The retry mechanism SHALL not add more than 30 seconds to total processing time (3 retries with backoff).

**REQ-BAML-NFR-004**: Schema parsing and initialization SHALL complete within 5 seconds at startup.

### 3.2 Accuracy

**REQ-BAML-NFR-005**: The validator SHALL correctly identify 99% of invalid outputs (high precision).

**REQ-BAML-NFR-006**: The validator SHALL correctly accept 95% of valid outputs (high recall, minimize false rejections).

**REQ-BAML-NFR-007**: The validator SHALL correctly validate all required schema constraints.

### 3.3 Reliability

**REQ-BAML-NFR-008**: The validator SHALL handle malformed input gracefully without crashing.

**REQ-BAML-NFR-009**: The validator SHALL recover from BAML framework errors and continue operation.

**REQ-BAML-NFR-010**: The validator SHALL provide meaningful error messages for debugging.

### 3.4 Resource Usage

**REQ-BAML-NFR-011**: The validator SHALL have minimal memory footprint (<50MB for schema definitions and validation state).

**REQ-BAML-NFR-012**: The validator SHALL not significantly impact overall system performance.

## 4. Interfaces & Contracts

### 4.1 BAML Schema Definition

**FinalAnswer Schema (BAML):**
```baml
model FinalAnswer {
    answer: string
    confidence: float
    sources: string[]
    reasoning?: string
    metadata?: {
        timestamp?: string
        model_used?: string
        token_usage?: {
            input_tokens?: int
            output_tokens?: int
        }
        program_version?: string
    }
}
```

**Validation Constraints:**
- `answer`: Non-empty string, max length 10000 characters
- `confidence`: Float between 0.0 and 1.0 (inclusive)
- `sources`: Array of non-empty strings, min length 1, max length 50
- `reasoning`: Optional string, max length 5000 characters
- `metadata`: Optional object with specified structure

### 4.2 Validator Interface

**Input Schema:**
```python
class ValidatorInput:
    raw_answer: str  # Unstructured answer from generator
    query: str  # Original query (for context)
    evidence_chunks: Optional[List[EvidenceChunk]]  # Evidence used
    schema_version: str = "v1"  # Schema version to use
    max_retries: int = 3  # Maximum retry attempts
```

**Output Schema:**
```python
class ValidationError:
    field_name: str  # Field that failed validation
    error_type: str  # "missing_field", "type_mismatch", "constraint_violation"
    expected: str  # Expected value/type
    actual: str  # Actual value/type
    message: str  # Human-readable error message

class ValidatorOutput:
    is_valid: bool  # True if validation passed
    validated_answer: Optional[FinalAnswer]  # Structured answer if valid
    errors: List[ValidationError]  # List of validation errors if invalid
    retry_count: int  # Number of retries attempted
    validation_time: float  # Validation duration in seconds
```

**Function Signature:**
```python
def validate_answer(
    raw_answer: str,
    query: str,
    evidence_chunks: Optional[List[EvidenceChunk]] = None,
    schema_version: str = "v1",
    max_retries: int = 3
) -> ValidatorOutput:
    """
    Validate and structure an answer according to BAML schema.
    
    Args:
        raw_answer: Unstructured answer text
        query: Original user query
        evidence_chunks: Evidence used (optional)
        schema_version: Schema version to use
        max_retries: Maximum retry attempts on failure
        
    Returns:
        ValidatorOutput with validation results
    """
```

### 4.3 Retry Interface

**Retry Request Schema:**
```python
class RetryRequest:
    original_answer: str  # Original answer that failed validation
    validation_errors: List[ValidationError]  # Errors from validation
    query: str  # Original query
    attempt_number: int  # Current retry attempt (1-based)
    max_attempts: int  # Maximum retry attempts
```

**Retry Response Schema:**
```python
class RetryResponse:
    regenerated_answer: str  # New answer from generator
    attempt_number: int  # Retry attempt number
    should_retry: bool  # Whether to attempt validation again
```

### 4.4 FinalAnswer Structure

**FinalAnswer Python Class:**
```python
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class TokenUsage:
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

@dataclass
class AnswerMetadata:
    timestamp: Optional[str] = None
    model_used: Optional[str] = None
    token_usage: Optional[TokenUsage] = None
    program_version: Optional[str] = None

@dataclass
class FinalAnswer:
    answer: str
    confidence: float
    sources: List[str]
    reasoning: Optional[str] = None
    metadata: Optional[AnswerMetadata] = None
```

### 4.5 Error Codes

| Error Code | Description | HTTP Equivalent |
|------------|-------------|-----------------|
| BAML-ERR-001 | Schema parsing error | 500 Internal Server Error |
| BAML-ERR-002 | Validation failure - missing required field | 422 Unprocessable Entity |
| BAML-ERR-003 | Validation failure - type mismatch | 422 Unprocessable Entity |
| BAML-ERR-004 | Validation failure - constraint violation | 422 Unprocessable Entity |
| BAML-ERR-005 | Maximum retries exceeded | 500 Internal Server Error |
| BAML-ERR-006 | BAML framework error | 500 Internal Server Error |
| BAML-ERR-007 | Schema version not found | 400 Bad Request |
| BAML-ERR-008 | Invalid schema definition | 500 Internal Server Error |

## 5. Tenant & Security Considerations

### 5.1 Multi-Tenancy
**REQ-BAML-SEC-001**: The system SHALL support single-tenant operation for local deployment (no multi-tenancy required).

### 5.2 Data Validation
**REQ-BAML-SEC-002**: The validator SHALL sanitize input to prevent injection attacks in structured output.

**REQ-BAML-SEC-003**: The validator SHALL enforce maximum length constraints on all string fields to prevent DoS.

### 5.3 Schema Security
**REQ-BAML-SEC-004**: The system SHALL validate schema definitions to prevent malicious schema injection.

**REQ-BAML-SEC-005**: The system SHALL restrict schema modifications to authorized processes only.

## 6. Observability & Telemetry

### 6.1 Metrics

**REQ-BAML-OBS-001**: The system SHALL track the following metrics:
- Validation success rate (percentage)
- Validation failure rate by error type (counter)
- Validation latency (histogram)
- Retry count distribution (histogram)
- Average retries per query (gauge)
- Schema version usage (counter)
- Validation errors by field (counter)

### 6.2 Logging

**REQ-BAML-OBS-002**: The system SHALL log at INFO level:
- Validation success/failure
- Retry attempts
- Schema version used

**REQ-BAML-OBS-003**: The system SHALL log at ERROR level:
- Validation failures with error details
- Maximum retries exceeded
- BAML framework errors
- Schema parsing errors

**REQ-BAML-OBS-004**: The system SHALL log at DEBUG level:
- Full validation error details
- Retry request/response details
- Schema validation steps

### 6.3 Health Checks

**REQ-BAML-OBS-005**: The system SHALL verify BAML schema loading and validation framework initialization in health checks.

## 7. Compliance & Governance

### 7.1 Audit Logging

**REQ-BAML-COMP-001**: The system SHALL log all validation attempts with:
- Timestamp
- Query identifier
- Validation result (success/failure)
- Retry count
- Schema version used
- Error details (if failed)

### 7.2 Data Retention

**REQ-BAML-COMP-002**: The system SHALL support configurable retention for validation logs (default: 30 days).

### 7.3 Schema Versioning

**REQ-BAML-COMP-003**: The system SHALL maintain schema version history for audit purposes.

**REQ-BAML-COMP-004**: The system SHALL support backward compatibility checks for schema changes.

## 8. Open Questions & Assumptions

### Open Questions

1. **Q1**: Should the validator support multiple schema versions simultaneously? (Assumed: Yes, with version selection)
2. **Q2**: Should validation errors trigger automatic prompt engineering improvements? (Assumed: Manual optimization for initial version)
3. **Q3**: What is the optimal retry strategy - immediate or with backoff? (Assumed: Exponential backoff)
4. **Q4**: Should the validator support custom validation rules beyond BAML schema? (Assumed: BAML schema only for initial version)
5. **Q5**: Should invalid outputs be stored for analysis? (Assumed: Logged only, not stored)

### Assumptions

1. BAML framework supports Python integration
2. LLM providers can generate structured outputs that can be validated
3. Validation failures are typically due to formatting, not fundamental answer quality
4. Maximum 3 retries is sufficient for most cases
5. Schema changes will be infrequent and require code updates
6. Validation adds minimal overhead to answer generation pipeline
7. BAML schemas can be defined in separate files for maintainability

