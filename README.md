# 🧩 Path Software Engineer Roadmap — Plan 5

## 🧠 RAG & Agentic Software Platform

Esta organización reúne el **Plan 5 — RAG & Agentic Software Platform** dentro de **Path Software Engineer**.

Este plan convierte la profundidad técnica de **Path AI Engineer — Plan 5: LLMs, RAG, Agents & Agentic Systems** en una aplicación de software robusta, trazable, visual y orientada a producto.

El objetivo no es construir demos sueltas de LLMs.

El objetivo es construir una plataforma aplicada que permita trabajar con documentos, búsqueda semántica, evaluación de retrieval y trazas de workflows agentic.

La idea central del plan es transformar sistemas LLM en software observable:

```txt
documentos
→ chunks
→ embeddings
→ búsqueda semántica
→ retrieval
→ evaluación
→ agentes
→ herramientas
→ trazas
→ dashboard
→ API
→ documentación
→ evidencia profesional
```

---

# 🎯 Objetivo del plan

Construir una aplicación de software aplicada a RAG y agentes que permita:

- cargar documentos;
- dividir documentos en chunks;
- ejecutar búsqueda semántica;
- mostrar fuentes recuperadas;
- comparar estrategias de retrieval;
- calcular métricas como Recall@K y Precision@K;
- visualizar workflows agentic;
- mostrar planner, tool calls, evaluator, retries y stop condition;
- documentar límites, errores y decisiones;
- exponer resultados mediante API o dashboard;
- convertir sistemas LLM en evidencia visible y profesional.

Este plan une fundamentos de software con sistemas de lenguaje, retrieval y agentes.

---

# 🔗 Relación con Path AI Engineer

Este plan acompaña el **Plan 5 de Path AI Engineer**:

**LLMs, RAG, Agents & Agentic Systems**

Path AI Engineer construye la profundidad técnica:

```txt
documentos
→ chunking
→ embeddings
→ retrieval
→ RAG
→ tools
→ agents
→ evaluation
→ security
→ multi-agent systems
```

Path Software Engineer convierte esa profundidad en producto:

```txt
aplicación robusta
→ frontend
→ backend
→ servicios de IA
→ source cards
→ retrieval dashboard
→ agent trace viewer
→ documentación funcional
→ user stories
→ technical stories
→ evidencia profesional
```

---

# 📦 Proyecto del plan

Este plan contiene un proyecto principal:

```txt
05-rag-agent-workflow-platform
```

## 🧠 Proyecto 05 — RAG Agent Workflow Platform

**RAG Agent Workflow Platform** es una aplicación de software aplicada a sistemas de lenguaje para buscar documentos, evaluar retrieval y visualizar workflows agentic.

El proyecto integra tres módulos principales:

```txt
Sprint 1 — Semantic Search Module
Sprint 2 — Retrieval Evaluation Dashboard
Sprint 3 — Agent Workflow Trace Viewer
```

Cada sprint corresponde a un antiguo Building Project, ahora convertido en parte de una sola plataforma robusta.

---

# 🏗️ Estructura esperada del proyecto

```txt
05-rag-agent-workflow-platform/
│
├── frontend/
├── backend/
├── ai-services/
├── data/
├── vector-store/
├── reports/
├── docs/
├── labs/
├── tests/
├── scripts/
└── deployment/
```

## 📁 Responsabilidades generales

### frontend/

Presenta la interfaz visual para búsqueda, evaluación de retrieval y trazas de agentes.

### backend/

Expone endpoints para consultas, resultados, métricas, source cards y traces.

### ai-services/

Contiene ingestion, chunking, embeddings, retrieval, métricas, evaluación y trazas agentic.

### data/

Guarda documentos, chunks, datasets de prueba y metadata.

### vector-store/

Guarda índices vectoriales locales, embeddings o representaciones persistentes si aplica.

### reports/

Guarda métricas, outputs, source cards, evaluation reports, trace reports y capturas.

### docs/

Guarda arquitectura, decisiones, historias, contratos API y documentación de sprints.

### labs/

Guarda laboratorios técnicos, cloud, producto y documentación.

### tests/

Guarda pruebas mínimas de frontend, backend y ai-services.

### scripts/

Guarda comandos repetibles para ingestion, search, evaluation y demo.

### deployment/

Guarda notas y archivos de despliegue.

---

# 🏃 Sprints del proyecto

## 🔎 Sprint 1 — Semantic Search Module

### Match

```txt
Path AI Engineer Proyecto 25 — semantic-search-embeddings-api
```

### Base anterior

```txt
13-semantic-search-demo-lite
```

### Objetivo

Construir el primer módulo de la plataforma para cargar documentos, dividirlos en chunks, crear embeddings o una representación semántica y mostrar resultados recuperados con fuentes visibles.

### Flujo

```txt
documentos
→ ingestion
→ chunking
→ embeddings
→ query
→ top-k results
→ source cards
→ demo de búsqueda
```

### Resultado esperado

- documentos de ejemplo;
- chunks generados;
- representación semántica;
- consulta del usuario;
- top-k results;
- source cards;
- ejemplos de búsqueda;
- limitaciones visibles;
- primer dashboard de búsqueda semántica.

---

## 📊 Sprint 2 — Retrieval Evaluation Dashboard

### Match

```txt
Path AI Engineer Proyecto 27 — chunking-retrieval-evaluation-lab
```

### Base anterior

```txt
14-retrieval-evaluation-dashboard-lite
```

### Objetivo

Agregar un módulo para comparar estrategias de chunking y retrieval usando métricas simples, ejemplos recuperados y etiquetas de relevancia.

### Flujo

```txt
documentos
→ estrategias de chunking
→ queries de prueba
→ retrieval top-k
→ relevance labels
→ Recall@K / Precision@K
→ comparison dashboard
```

### Resultado esperado

- estrategias de chunking comparadas;
- test queries;
- retrieved results table;
- relevance labels;
- Recall@K;
- Precision@K;
- hit rate si aplica;
- tabla comparativa;
- error examples;
- dashboard de evaluación retrieval.

---

## 🧠 Sprint 3 — Agent Workflow Trace Viewer

### Match

```txt
Path AI Engineer Proyecto 29 — agentic-workflow-langgraph-lab
```

### Base anterior

```txt
15-agent-workflow-trace-viewer
```

### Objetivo

Agregar un módulo para visualizar workflows agentic, mostrando qué hizo el agente paso a paso: planner, tool calls, resultados, evaluación, retries, stop condition y respuesta final.

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

### Resultado esperado

- trace schema;
- planner step viewer;
- tool call viewer;
- tool result cards;
- evaluation step viewer;
- retry / stop condition;
- trace timeline;
- error notes;
- debug report;
- viewer de trazas agentic.

---

# 📚 Documentación esperada

Cada sprint debe dejar documentación clara:

- Sprint Goal;
- User Stories;
- Technical Stories;
- Acceptance Criteria;
- Definition of Done;
- Sprint Review;
- Sprint Retrospective;
- decisiones técnicas;
- evidencia generada;
- limitaciones;
- conexión con Path AI Engineer.

## 📄 Documentos principales

```txt
docs/architecture.md
docs/decisions.md
docs/user-stories.md
docs/technical-stories.md
docs/api-contract.md
docs/sprint-01-semantic-search.md
docs/sprint-02-retrieval-evaluation.md
docs/sprint-03-agent-trace-viewer.md
```

---

# ✅ Definition of Done del plan

Una tarea no termina solo cuando el código funciona.

Termina cuando deja evidencia.

Definition of Done:

- código implementado;
- prueba mínima realizada;
- resultado visible;
- fuente o traza documentada;
- decisión registrada;
- historia actualizada si aplica;
- README actualizado si aplica;
- output o captura generada si aplica;
- sin archivos basura;
- sin responsabilidades mezcladas.

---

# 🧪 Labs esperados

El proyecto incluirá labs técnicos, cloud, producto y documentación.

## Sprint 1 — Semantic Search Labs

- `tec-document-ingestion-lab`;
- `tec-basic-chunking-lab`;
- `tec-embedding-concept-lab`;
- `tec-semantic-search-lab`;
- `tec-source-card-lab`;
- `tec-query-examples-lab`;
- `docs-semantic-search-storytelling-lab`;
- `docs-source-display-template-lab`;
- `cloud-documents-to-gcp-storage-lab`;
- `cloud-documents-to-aws-s3-lab`;
- `cloud-documents-to-azure-blob-lab`.

## Sprint 2 — Retrieval Evaluation Labs

- `tec-chunking-strategy-comparison-lab`;
- `tec-retrieval-test-set-lab`;
- `tec-relevance-labeling-lab`;
- `tec-recall-at-k-lab`;
- `tec-precision-at-k-lab`;
- `tec-retrieval-error-examples-lab`;
- `docs-retrieval-evaluation-storytelling-lab`;
- `docs-rag-evaluation-report-template-lab`;
- `cloud-retrieval-report-to-gcp-storage-lab`;
- `cloud-retrieval-report-to-aws-s3-lab`;
- `cloud-retrieval-report-to-azure-blob-lab`.

## Sprint 3 — Agent Trace Labs

- `tec-agent-trace-schema-lab`;
- `tec-planner-node-viewer-lab`;
- `tec-tool-call-viewer-lab`;
- `tec-tool-result-card-lab`;
- `tec-evaluator-node-viewer-lab`;
- `tec-retry-stop-condition-lab`;
- `docs-agent-trace-storytelling-lab`;
- `docs-agent-debug-report-template-lab`;
- `cloud-agent-traces-to-gcp-storage-lab`;
- `cloud-agent-traces-to-aws-s3-lab`;
- `cloud-agent-traces-to-azure-blob-lab`.

Los labs no son relleno.

Sirven para comparar, reforzar decisiones y dejar evidencia técnica.

---

# 📊 Métricas y evidencia esperada

## Semantic Search

- número de documentos;
- número de chunks;
- top-k results;
- similarity score si aplica;
- source cards;
- query examples;
- failure examples;
- demo visual.

## Retrieval Evaluation

- número de documentos;
- número de chunks por estrategia;
- número de queries;
- top-k results;
- relevance labels;
- Recall@K;
- Precision@K;
- hit rate;
- comparison table;
- error examples;
- dashboard visual.

## Agent Workflow Trace

- número de pasos;
- tool calls;
- tool success / failure;
- número de retries;
- stop condition;
- trace timeline;
- error notes;
- final answer;
- debug report;
- viewer visual.

---

# 🖥️ Resultado final esperado

Al terminar este plan, debe existir una plataforma RAG y agentic aplicada con:

- Semantic Search Module;
- Retrieval Evaluation Dashboard;
- Agent Workflow Trace Viewer;
- frontend;
- backend;
- AI services;
- source cards;
- retrieval metrics;
- trace viewer;
- API documentada;
- reports;
- labs documentados;
- user stories;
- technical stories;
- sprint docs;
- README profesional;
- guía de ejecución local;
- evidencia visual;
- notas de deploy.

---

# 📊 Nivel esperado al terminar Plan 5

| Área                               | Nivel esperado |
| ---------------------------------- | -------------: |
| Semantic search aplicado           |           8/10 |
| Document ingestion                 |           8/10 |
| Chunking básico                    |           8/10 |
| Embedding concepts                 |           8/10 |
| Source cards                       |         8.5/10 |
| Retrieval evaluation               |         8.5/10 |
| Recall@K / Precision@K             |           8/10 |
| Relevance labeling                 |           8/10 |
| RAG evaluation storytelling        |         8.5/10 |
| Agent trace design                 |         8.5/10 |
| Tool call visualization            |           8/10 |
| Retry / stop condition explanation |           8/10 |
| Debug report de agentes            |         8.5/10 |
| README profesional                 |         8.5/10 |
| Evidencia visual de aprendizaje    |           9/10 |

---

# 🧠 Resultado de aprendizaje

Al cerrar este plan podré decir:

Construí una aplicación de software aplicada a RAG y agentes.

No solo hice búsquedas con embeddings.  
No solo calculé métricas de retrieval.  
No solo hice un agente que responde.

Integré documentos, chunks, embeddings, retrieval, evaluación, source cards, tool calls, trazas, API, dashboard, documentación, sprints e historias dentro de una plataforma.

---

# 🧭 Regla final del plan

Un sistema LLM no debe ser una caja negra.

Debe mostrar:

- fuentes;
- fragmentos;
- métricas;
- herramientas usadas;
- pasos internos;
- errores;
- límites.

Lo que no se puede observar, se vuelve difícil de confiar.

Path AI Engineer me da profundidad técnica.

Path Software Engineer convierte esa profundidad en producto.

---

# 👤 Autor

**Jean Franck Loa Rojas**

Path Software Engineer Builder  
RAG • Semantic Search • Retrieval Evaluation • Agents • Tool Use • Trace Viewer • Applied AI Software Systems
