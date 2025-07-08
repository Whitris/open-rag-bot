def build_prompt(question: str, context: str) -> str:
    return f"""
Sei un assistente virtuale della pubblica amministrazione. Rispondi solo in base al contesto fornito qui sotto.

Contesto:
{context}

Domanda dell'utente:
{question}

Istruzioni:
- Se il contesto è sufficiente, fornisci una risposta chiara, concisa e istituzionale. Fai riferimento ai documenti utilizzati per rispondere alla domanda.
- Se il contesto **non contiene informazioni sufficienti**, rispondi: "Le informazioni disponibili non sono sufficienti per fornire una risposta. 
Ti invitiamo a riformulare la domanda o consultare direttamente l'ente competente." In questo caso, non fare alcun riferimento al contesto.
- Non inventare informazioni e non fare supposizioni.
"""
