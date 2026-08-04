# Project 05 master plan

> Preserved planning baseline. Implementation status and executable instructions live in the project `README.md`; only Sprint 1 is implemented in the current working tree.

# 05-rag-agent-workflow-platform

## 🧠 Descripción

**RAG Agent Workflow Platform** es una aplicación de software aplicada a sistemas de lenguaje, búsqueda semántica, evaluación de retrieval y visualización de workflows agentic.

Este proyecto pertenece a:

```txt
Path Software Engineer
Plan 5 — RAG & Agentic Software Platform
```

y acompaña directamente al:

```txt
Path AI Engineer
Plan 5 — LLMs, RAG, Agents & Agentic Systems
```

Este proyecto nace como evolución de los antiguos proyectos de Building Projects:

```txt
13-semantic-search-demo-lite
14-retrieval-evaluation-dashboard-lite
15-agent-workflow-trace-viewer
```

Ahora esos proyectos ya no vivirán como repositorios separados.

Se convierten en **3 sprints principales** dentro de una sola aplicación de software más robusta, trazable, documentada y orientada a producto.

---

# 🎯 Objetivo general

Construir una plataforma aplicada que permita:

```txt
cargar documentos
→ dividirlos en chunks
→ buscar por significado
→ mostrar fuentes recuperadas
→ evaluar retrieval
→ comparar estrategias
→ visualizar workflows agentic
→ mostrar tools, retries y stop conditions
→ exponer resultados en dashboard
→ documentar decisiones y evidencia
```

El objetivo no es construir un sistema enterprise de RAG desde el inicio.

El objetivo es crear una aplicación sólida y progresiva que conecte:

```txt
documentos
→ embeddings
→ retrieval
→ evaluación
→ agentes
→ trazas
→ software
→ evidencia profesional
```

---

# 🧭 Relación con Path AI Engineer

Este proyecto acompaña los proyectos impares del Plan 5 de Path AI Engineer:

```txt
Path AI Engineer Proyecto 25
→ semantic-search-embeddings-api

Path AI Engineer Proyecto 27
→ chunking-retrieval-evaluation-lab

Path AI Engineer Proyecto 29
→ agentic-workflow-langgraph-lab
```

Cada uno se convierte en un sprint dentro de esta plataforma.

```txt
Sprint 1 → Semantic Search Module
Sprint 2 → Retrieval Evaluation Dashboard
Sprint 3 → Agent Workflow Trace Viewer
```

---

# 👤 Usuario objetivo

Esta plataforma está pensada para:

```txt
AI Engineer en formación
persona construyendo RAG
equipo que necesita evaluar retrieval
equipo que necesita depurar agentes
reclutador técnico
constructor de portafolio aplicado
```

El usuario debe poder abrir la aplicación o el README y entender:

```txt
qué documentos entraron
qué chunks se generaron
qué resultados fueron recuperados
qué fuentes respaldan una respuesta
qué estrategia de retrieval funcionó mejor
qué pasos siguió un agente
qué tool usó
dónde falló
qué limitaciones tiene el sistema
```

---

# 🏗️ Arquitectura general esperada

```txt
RAG Agent Workflow Platform
│
├── Frontend
│   └── Search, retrieval evaluation and trace dashboard
│
├── Backend
│   └── API for queries, results, metrics and traces
│
├── AI Services
│   └── ingestion, chunking, embeddings, retrieval, evaluation and traces
│
├── Data Layer
│   └── documents, chunks, test queries and metadata
│
├── Reports
│   └── source cards, metrics, trace reports and outputs
│
└── Docs
    └── user stories, technical stories, decisions and sprint docs
```

---

# 🔁 Flujo general de la plataforma

```txt
data/documents
→ document ingestion
→ chunking
→ embedding representation
→ vector search
→ top-k retrieval
→ source cards
→ retrieval evaluation
→ agent workflow traces
→ API
→ frontend dashboard
→ reports
→ documentation
```

---

# 🧩 Sprints del proyecto

## Sprint 1 — Semantic Search Module

### Match

```txt
Path AI Engineer Proyecto 25 — semantic-search-embeddings-api
```

### Base anterior

```txt
13-semantic-search-demo-lite
```

### Objetivo

Crear el primer módulo de la plataforma para cargar documentos, dividirlos en chunks, buscar por significado y mostrar resultados con fuentes visibles.

### Flujo

```txt
documentos
→ ingestion
→ chunking
→ embeddings
→ query
→ top-k results
→ source cards
→ semantic search demo
```

### Módulos principales

#### Módulo 1 — Document Ingestion

Cargar documentos pequeños con metadata simple.

Pregunta central:

```txt
¿Qué documentos voy a hacer buscables?
```

#### Módulo 2 — Chunking

Dividir documentos en fragmentos recuperables.

Pregunta central:

```txt
¿Cómo divido documentos sin perder contexto?
```

#### Módulo 3 — Embedding Notes

Crear o simular representación semántica.

Pregunta central:

```txt
¿Cómo convierte el sistema texto en algo comparable por significado?
```

#### Módulo 4 — Semantic Search

Ejecutar búsqueda semántica y recuperar top-k resultados.

Pregunta central:

```txt
¿Qué fragmentos se parecen más al significado de la consulta?
```

#### Módulo 5 — Source Cards

Mostrar resultados con fuente, chunk, score y limitación.

Pregunta central:

```txt
¿Cómo muestro resultados de búsqueda de forma clara y confiable?
```

#### Módulo 6 — Demo Lite

Crear vista final de búsqueda.

Pregunta central:

```txt
¿Puede alguien probar búsqueda semántica sin abrir el código?
```

### Resultado esperado

Al finalizar este sprint, la plataforma debe permitir ver:

```txt
documentos cargados
chunks generados
query del usuario
top-k results
source cards
scores si aplican
limitaciones de la búsqueda
demo visual de semantic search
```

---

## Sprint 2 — Retrieval Evaluation Dashboard

### Match

```txt
Path AI Engineer Proyecto 27 — chunking-retrieval-evaluation-lab
```

### Base anterior

```txt
14-retrieval-evaluation-dashboard-lite
```

### Objetivo

Agregar un módulo para comparar estrategias de chunking y retrieval con métricas simples y evidencia visual.

### Flujo

```txt
documentos
→ estrategias de chunking
→ test queries
→ top-k retrieved results
→ relevance labels
→ Recall@K / Precision@K
→ comparison dashboard
```

### Módulos principales

#### Módulo 1 — Chunking Strategy Setup

Definir estrategias de chunking.

Pregunta central:

```txt
¿Cómo afecta el tamaño del chunk al retrieval?
```

#### Módulo 2 — Retrieval Test Set

Crear queries de prueba y documentos relevantes esperados.

Pregunta central:

```txt
¿Qué consultas usaré para probar si el retrieval funciona?
```

#### Módulo 3 — Retrieved Results Table

Guardar resultados recuperados por estrategia.

Pregunta central:

```txt
¿Qué recuperó cada estrategia?
```

#### Módulo 4 — Relevance Labels

Asignar relevancia manual a los resultados.

Pregunta central:

```txt
¿Cuáles resultados realmente ayudan a responder la consulta?
```

#### Módulo 5 — Metrics Calculator

Calcular Recall@K, Precision@K y hit rate si aplica.

Pregunta central:

```txt
¿Qué estrategia recupera mejor la información correcta?
```

#### Módulo 6 — Comparison Dashboard

Crear vista de comparación.

Pregunta central:

```txt
¿Puede alguien ver qué estrategia de retrieval conviene sin leer el código?
```

### Resultado esperado

Al finalizar este sprint, la plataforma debe permitir ver:

```txt
estrategias de chunking
queries de prueba
resultados recuperados
etiquetas de relevancia
Recall@K
Precision@K
tabla comparativa
errores de retrieval
dashboard de evaluación
```

---

## Sprint 3 — Agent Workflow Trace Viewer

### Match

```txt
Path AI Engineer Proyecto 29 — agentic-workflow-langgraph-lab
```

### Base anterior

```txt
15-agent-workflow-trace-viewer
```

### Objetivo

Agregar un módulo para visualizar workflows agentic y entender qué hizo un agente paso a paso.

### Flujo

```txt
user request
→ planner
→ tool call
→ tool result
→ evaluator
→ retry / stop
→ final answer
→ trace viewer
```

### Módulos principales

#### Módulo 1 — Trace Schema

Definir formato de una traza.

Pregunta central:

```txt
¿Qué información necesito guardar para entender lo que hizo un agente?
```

#### Módulo 2 — Planner Step Viewer

Mostrar el paso de planificación.

Pregunta central:

```txt
¿Qué decidió hacer el agente antes de usar herramientas?
```

#### Módulo 3 — Tool Call Viewer

Mostrar llamadas a herramientas y argumentos.

Pregunta central:

```txt
¿Qué herramienta usó el agente y con qué argumentos?
```

#### Módulo 4 — Evaluation Step Viewer

Mostrar evaluación del resultado.

Pregunta central:

```txt
¿Cómo decide el agente si el resultado sirve?
```

#### Módulo 5 — Retry / Stop Condition

Mostrar retries, intentos y condición de parada.

Pregunta central:

```txt
¿Cuándo debe intentar de nuevo y cuándo debe detenerse?
```

#### Módulo 6 — Trace Viewer

Crear vista final del workflow.

Pregunta central:

```txt
¿Puede alguien entender el comportamiento del agente sin leer el código?
```

### Resultado esperado

Al finalizar este sprint, la plataforma debe permitir ver:

```txt
user request
planner step
tool calls
tool results
evaluation step
retry / stop condition
final answer
trace timeline
error notes
debug report
```

---

# 🧱 Módulos principales de la plataforma

## 1. Document Ingestion

Responsabilidad:

```txt
Cargar documentos y metadata para hacerlos buscables.
```

Incluye:

```txt
documentos .txt / .md
título
fuente
metadata
validación básica
```

---

## 2. Chunking Engine

Responsabilidad:

```txt
Dividir documentos en fragmentos recuperables.
```

Incluye:

```txt
chunk size
overlap
chunk id
source id
texto recuperable
```

---

## 3. Semantic Search Engine

Responsabilidad:

```txt
Recuperar fragmentos relevantes para una consulta.
```

Incluye:

```txt
query
embedding o representación semántica
similarity score
top-k results
ranking
```

---

## 4. Source Card Generator

Responsabilidad:

```txt
Convertir resultados recuperados en tarjetas claras y confiables.
```

Incluye:

```txt
document title
chunk text
score
por qué parece relevante
limitación
```

---

## 5. Retrieval Evaluation Engine

Responsabilidad:

```txt
Evaluar si el sistema recuperó la evidencia correcta.
```

Incluye:

```txt
test queries
relevance labels
Recall@K
Precision@K
hit rate
error examples
```

---

## 6. Agent Trace Engine

Responsabilidad:

```txt
Guardar y representar los pasos de un workflow agentic.
```

Incluye:

```txt
planner
tool call
tool result
evaluator
retry
stop condition
final answer
```

---

## 7. Visual Dashboard

Responsabilidad:

```txt
Mostrar búsqueda, evaluación y trazas de forma clara.
```

Debe incluir:

```txt
semantic search
source cards
retrieval metrics
comparison tables
agent traces
error notes
limitations
```

---

# 🧪 Labs del proyecto

## Sprint 1 — Semantic Search Labs

```txt
tec-document-ingestion-lab
tec-basic-chunking-lab
tec-embedding-concept-lab
tec-semantic-search-lab
tec-source-card-lab
tec-query-examples-lab
docs-semantic-search-storytelling-lab
docs-source-display-template-lab
cloud-documents-to-gcp-storage-lab
cloud-documents-to-aws-s3-lab
cloud-documents-to-azure-blob-lab
```

## Sprint 2 — Retrieval Evaluation Labs

```txt
tec-chunking-strategy-comparison-lab
tec-retrieval-test-set-lab
tec-relevance-labeling-lab
tec-recall-at-k-lab
tec-precision-at-k-lab
tec-retrieval-error-examples-lab
docs-retrieval-evaluation-storytelling-lab
docs-rag-evaluation-report-template-lab
cloud-retrieval-report-to-gcp-storage-lab
cloud-retrieval-report-to-aws-s3-lab
cloud-retrieval-report-to-azure-blob-lab
```

## Sprint 3 — Agent Trace Labs

```txt
tec-agent-trace-schema-lab
tec-planner-node-viewer-lab
tec-tool-call-viewer-lab
tec-tool-result-card-lab
tec-evaluator-node-viewer-lab
tec-retry-stop-condition-lab
docs-agent-trace-storytelling-lab
docs-agent-debug-report-template-lab
cloud-agent-traces-to-gcp-storage-lab
cloud-agent-traces-to-aws-s3-lab
cloud-agent-traces-to-azure-blob-lab
```

---

# 📊 Métricas / Evidencia esperada

## Semantic Search

```txt
número de documentos
número de chunks
top-k results
similarity scores
source cards
query examples
failure examples
demo visual
```

## Retrieval Evaluation

```txt
número de documentos
número de chunks por estrategia
número de queries
retrieved results
relevance labels
Recall@K
Precision@K
hit rate
comparison table
error examples
```

## Agent Workflow Trace

```txt
número de pasos
tool calls
tool success / failure
número de retries
stop condition
trace timeline
error notes
final answer
debug report
```

---

# 🖥️ Dashboard esperado

La plataforma debe incluir una vista visual con secciones como:

```txt
Overview
Semantic Search
Retrieval Evaluation
Agent Traces
Reports
Limitations
```

Cada sección debe mostrar resultados claros sin obligar al usuario a leer el código.

---

# 🚀 Estado actual

Pendiente / por iniciar.

---

# 🧭 Ciclo de trabajo

```txt
Sprint 1 → Semantic Search Module
Sprint 2 → Retrieval Evaluation Dashboard
Sprint 3 → Agent Workflow Trace Viewer
```

Cada sprint debe cerrar con:

```txt
módulo funcional
historias documentadas
resultados visibles
reports actualizados
README actualizado
sprint review
sprint retrospective
conexión con Path AI Engineer
```

---

# 📌 Próximos pasos

## Sprint 1

```txt
Definir documentos de ejemplo
Crear ingestion
Crear chunking
Crear embeddings o simulación
Crear semantic search
Crear source cards
Crear demo inicial
Documentar labs
Actualizar README
```

## Sprint 2

```txt
Definir estrategias de chunking
Crear test queries
Ejecutar retrieval
Etiquetar relevancia
Calcular Recall@K
Calcular Precision@K
Crear dashboard comparativo
Documentar errores
```

## Sprint 3

```txt
Definir trace schema
Crear planner step
Crear tool call example
Crear evaluator step
Crear retry / stop condition
Crear trace viewer
Crear debug report
Documentar limitaciones
```

---

# ✅ Entregable final

Al terminar este proyecto debe existir:

```txt
Aplicación RAG y agentic aplicada
Semantic Search Module
Retrieval Evaluation Dashboard
Agent Workflow Trace Viewer
Frontend
Backend/API si aplica
Servicio de IA
Documentos de ejemplo
Chunks
Source cards
Retrieval metrics
Agent traces
Reports
User stories
Technical stories
Acceptance criteria
Sprint docs
Labs documentados
README profesional
Evidencia visual
Deploy o guía de deploy
```

---

# 🧠 Resultado esperado

Al terminar este proyecto podré decir:

```txt
Construí una aplicación de software aplicada a RAG y agentes.

No solo hice búsqueda semántica.
No solo calculé métricas de retrieval.
No solo hice un agente que responde.

Integré documentos, chunks, embeddings, retrieval, evaluación, source cards, tool calls, trazas, API, dashboard, documentación, sprints e historias dentro de una sola plataforma.
```

---

# 🧭 Regla final

```txt
Un sistema LLM no debe ser una caja negra.

Debe mostrar fuentes, fragmentos, métricas, herramientas usadas, pasos internos, errores y límites.

Path AI Engineer me da la profundidad.
Path Software Engineer convierte esa profundidad en producto.
```

---

# 👤 Autor

**Jean Franck Loa Rojas**

Path Software Engineer Builder
RAG • Semantic Search • Retrieval Evaluation • Agents • Tool Use • Trace Viewer • Applied AI Software Systems
