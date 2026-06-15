# RAG con Memoria — Progetto Guidato

## Documento di riferimento

**SIA-RB — Manuale di Gestione (Sistema Informativo Agricolo Regione Basilicata)**

- **File**: `Manuale_Gestione_SIARB.pdf` (nella stessa cartella)
- **Contenuto**: manuale tecnico del sistema informativo gestionale della Regione Basilicata
- **Argomenti**: anagrafe regionale, gestione accessi, procedure operative, moduli del sistema
- **Dimensione**: 18 pagine

---

## Step 1 — Sistema RAG

Costruire un sistema RAG che permetta di interrogare il manuale in linguaggio naturale.

Il sistema deve:

- Estrarre il testo dal PDF e suddividerlo in chunk semanticamente coerenti
- Convertire ogni chunk in embedding e salvarlo in ChromaDB
- Data una domanda, recuperare i chunk più rilevanti e generare una risposta con un LLM
- Rispondere solo in base al contenuto del documento; se la risposta non c'è, dirlo esplicitamente

**Verifica**: le domande seguenti devono ricevere risposte pertinenti e fondate sul testo del manuale.

1. Quali moduli compongono la sezione UMA del sistema?
2. Come funziona la gestione dei bandi regionali?
3. Quali procedure amministrative gestisce il comparto fitosanitario?
4. Come si richiedono gli indennizzi per danni da calamità naturali?

---

## Step 2 — Memoria Conversazionale con RAG

Estendere il sistema dello Step 1 con una memoria basata su ChromaDB: ogni scambio della conversazione viene salvato in una seconda collection e recuperato semanticamente nelle domande successive.

Il sistema deve:

- Mantenere due collection ChromaDB separate: una per la knowledge base del documento, una per la storia della conversazione
- Ad ogni turno, interrogare entrambe le collection e combinare i risultati nel prompt
- Limitare il contesto live con una sliding window (non trasmettere l'intera storia)
- Persistere la memoria tra sessioni diverse senza perdere i turni precedenti

**Verifica**: dopo una serie di domande sul documento, il sistema deve rispondere correttamente anche a:

1. "Cosa mi hai detto sulla sezione UMA?" — deve attingere dalla memoria conversazionale
2. "Ricapitoliamo: di cosa abbiamo parlato finora?" — deve saper sintetizzare dalla memoria
3. Una domanda assente sia dal documento che dalla conversazione — deve ammetterlo

---

## Step 3 — Chatbot con Gradio

Costruire un'interfaccia web funzionante che esponga il sistema degli Step 1 e 2 come chatbot reale.

L'interfaccia deve:

- Mostrare la conversazione in un'area chat con messaggi user/assistant distinti
- Accettare input testuali e restituire risposte del sistema RAG+memoria
- Inizializzare la knowledge base al lancio dell'applicazione (non ad ogni messaggio)
- Mantenere la memoria conversazionale per tutta la durata della sessione

**Verifica**:

1. L'applicazione si avvia senza errori e la knowledge base viene caricata una sola volta
2. È possibile fare più domande in sequenza senza ricaricare la pagina
3. Le domande che fanno riferimento a scambi precedenti ricevono risposte coerenti
