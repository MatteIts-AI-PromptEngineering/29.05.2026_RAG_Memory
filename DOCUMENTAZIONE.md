# Documentazione progetto "Rag con memeoria conversazionale"

## Descrizione del progetto
Questo progetto realizza un sistema RAG con memoria conversazionale per interrogare un documento PDF.
L’obiettivo è permettere all’utente di fare domande sul contenuto del manuale e ricevere risposte generate da un modello linguistico, ma fondate esclusivamente sul testo disponibile nel documento e sulla conversazione precedente.

Il sistema è composto da tre parti principali:
1. **Estrazione del testo dal PDF e creazione di un indice per la ricerca**
2. **Recupero semantico delle informazioni**
3. **Chatbot con memoria conversazionale**

## Obiettivi del progetto
### Sistema RAG
Creare un sistema in grado di:
- estrarre il testo da un PDF
- dividerlo in chunk coerenti
- creare embedding
- salvare i chunk in ChromaDB
- recuperare i chunk più rilevanti rispetto a una domanda
- generare una risposta con un LLM

Logica implementata in:
- src/rag/extractor.py
- src/rag/embedder.py
- src/rag/retriever.py
- src/rag/rag_system.py
### Memoria conversazionale
Implementare una memoria conversazionale che permetta al sistema di ricordare le interazioni precedenti con l’utente, in modo da fornire risposte più contestualizzate e coerenti nel tempo.

Questa parte è gestita in:
- src/rag/memory_system.py
### Chatbot con interfaccia web
Creare un’interfaccia web semplice con Gradio per interagire con il sistema.

Questa parte è avviata in:
- app.py

## Architettura generale
L’architettura del progetto è basata su questi moduli:

### **Estrazione del testo**
Il PDF viene letto e convertito in testo markdown tramite pymupdf4llm.

File coinvolto:
- src/rag/extractor.py

### **Chunking**
Il testo viene suddiviso in frammenti più piccoli con RecursiveCharacterTextSplitter, per facilitare la ricerca semantica.
File coinvolto:
- src/rag/extractor.py

### **Embedding e indicizzazione**
Ogni chunk viene trasformato in embedding con il modello nomic-embed-text e salvato in ChromaDB.

File coinvolto:
- src/rag/embedder.py

### **Retrieval**
Quando arriva una domanda, il sistema confronta la query con i chunk del documento e recupera i più simili.

File coinvolto:
- src/rag/retriever.py

### **Memoria conversazionale**
I turni della chat vengono salvati in una seconda collection ChromaDB, così il sistema può richiamare ciò che è stato detto in precedenza.

File coinvolto:
- src/rag/memory_system.py

### **Generazione della risposta**
Il prompt finale combina:
- contesto dal documento
- memoria conversazionale
- domanda dell’utente

e viene avviato Ollama.

File coinvolti:
- src/chat_client/prompt_builder.py
- src/chat_client/client.py
- src/chat_client/chat_engine.py

## Struttura dei file
### app.py

È il punto di ingresso dell’applicazione.

Qui vengono creati:
- RagSystem
- MemorySystem
- Client
- ChatEngine
- gr.ChatInterface
- 
Inoltre, la knowledge base viene inizializzata una sola volta all’avvio.

### src/config.py
Contiene tutte le configurazioni del progetto:

- URL di Ollama
- modello LLM
- modello embedding
- parametri di chunking
- percorso del PDF
- percorso del database
- parametri della memoria

Questa centralizzazione rende il progetto più facile da mantenere.

### src/rag/extractor.py
Si occupa di:
- leggere il PDF
- estrarre il testo
- dividerlo in chunk

### src/rag/embedder.py
Si occupa di:
- calcolare gli embedding
- creare o aprire la collection ChromaDB
- salvare i chunk del documento

### src/rag/retriever.py
Si occupa di:
- trasformare la domanda in embedding
- cercare i chunk più simili nel database vettoriale

### src/rag/rag_system.py
Coordina l’intera pipeline RAG:
- extraction
- chunking
- embedding
- indexing

### src/rag/memory_system.py
Gestisce la memoria della conversazione:
- salva ogni turno
- recupera i turni più pertinenti
- usa una sliding window per limitare il contesto

### src/chat_client/client.py
Fa la chiamata al modello Ollama e costruisce la lista dei messaggi da inviare al modello.

### src/chat_client/prompt_builder.py
Costruisce:
- il system prompt
- il prompt utente finale con documento + memoria + domanda

### src/chat_client/chat_engine.py
È il livello di orchestrazione:
- normalizza il messaggio
- recupera documenti e memoria
- costruisce il prompt
- invia la richiesta al modello
- salva il turno nella memoria

## Configurazione
Le principali impostazioni si trovano in src/config.py.

**Configurazioni del modello**
- API_URL = "http://localhost:11434"
- MODEL = "llama3.2:latest"
- TEMPERATURE = 0.1
- TOP_P = 0.1
- NUM_PREDICT = 200

**Configurazioni embedding**
- EMBEDDING_MODEL = "nomic-embed-text"
- TOP_K = 5

**Configurazioni chunking**
- CHUNK_SIZE = 500
- CHUNK_OVERLAP = 100
- SEPARATORS = ["\n## ", "\n### ", "\n\n", "\n", " "]

**Percorsi**
- FILE_PATH = "./data/Manuale_Gestione_SIARB.pdf"
- DATABASE_URL = "./data/chroma/chroma.db"

**Memoria**
- MEMORY_TOP_K = 3
- MEMORY_WINDOW_SIZE = 30

## Dipendenze
Le librerie principali usate dal progetto sono elencate in requirements.txt:
- ollama
- chromadb
- pymupdf4llm
- langchain-text-splitters
- tiktoken
- gradio

Ruolo delle dipendenze
- **ollama**: chat con il modello e creazione embedding
- **chromadb**: database vettoriale persistente
- **pymupdf4llm**: estrazione del testo dal PDF
- **langchain-text-splitters**: divisione in chunk
- **gradio**: interfaccia web
- **tiktoken**: supporto tecnico per il tokenizing/chunking

## Avvio del progetto
Il progetto si avvia dal file app.py.

**Requisiti**

Prima di eseguire l’applicazione è necessario:
- avere Ollama attivo in locale
- avere disponibile il modello llama3.2:latest
- avere disponibile il modello embedding nomic-embed-text
- posizionare il PDF in ./data/Manuale_Gestione_SIARB.pdf

**Avvio**

L’applicazione inizializza la knowledge base all’avvio e poi apre l’interfaccia chat Gradio.

## Gestione della memoria conversazionale
La memoria è uno degli aspetti più interessanti del progetto.

**Funzionamento**
- ogni domanda e risposta viene salvata come turno
- il turno viene trasformato in embedding
- il turno viene salvato nella collection conversation_memory
- nelle domande successive, il sistema recupera i turni più rilevanti

**Persistenza**

La memoria viene mantenuta nel database ChromaDB, quindi non si perde tra una sessione e l’altra.

**Sliding window**

Per evitare di inviare troppa storia al modello, viene usata una finestra limitata degli ultimi turni.

Implementazione principale:
- src/rag/memory_system.py
- src/chat_client/client.py

## Esempi di utilizzo
Puoi inserire una sezione con esempi pratici come:
- “Quali moduli compongono la sezione UMA?”
- “Come funziona la gestione dei bandi regionali?”
- “Cosa mi hai detto sulla sezione UMA?”
- “Ricapitoliamo: di cosa abbiamo parlato finora?”
- “Una domanda che non è presente né nel documento né nella chat.”
Questi esempi dimostrano:
- retrieval dal documento
- uso della memoria conversazionale
- comportamento corretto quando l’informazione non è disponibile

## Conclusione
Questo progetto dimostra come costruire un sistema completo di:
- analisi di documenti
- retrieval semantico
- memoria conversazionale
- interfaccia chat web

L’unione di RagSystem, MemorySystem e ChatEngine consente di creare un assistente in grado di rispondere in modo contestualizzato e persistente.

