

enum SourceType {
    Documentation
    Code
    Other
}

class Reference {
    name string
    type SourceType
}

class FinalAnswer {
    answer string
    confidence float
    sources Reference[]
}

function GenerateAnswer(question: string, context: string) -> FinalAnswer {
    client GPT4
    prompt #"
        Given the context below, answer the user's question.
        
        Context:
        {{ context }}

        Question:
        {{ question }}

        {{ ctx.output_format }}
    "#
}
