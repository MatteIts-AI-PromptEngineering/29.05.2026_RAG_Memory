def get_system_prompt() -> str:
    return (
        "Sei un assistente che risponde ESCLUSIVAMENTE in base al contesto fornito. "
        "Se la risposta non e' presente nel contesto documentale ne' nella storia conversazionale, "
        "dillo esplicitamente senza inventare informazioni. "
        "Rispondi sempre in ITALIANO"
    )


def get_user_prompt(doc_chunks: list, question: str, memory_chunks: list = None) -> str:
    doc_section = "\n\n".join(doc_chunks) if doc_chunks else "Nessun documento rilevante trovato."

    memory_section = ""
    if memory_chunks:
        memory_section = (
            "\n--- Storia conversazionale rilevante ---\n"
            + "\n\n".join(memory_chunks)
            + "\n---\n"
        )

    return (
        "--- Contesto dal documento ---\n"
        + doc_section
        + "\n---\n"
        + memory_section
        + "\nDomanda: " + question
    )
