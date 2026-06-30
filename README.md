# Building Projects Roadmap — Plan 5

## 🧠 RAG, Agents & Tooling Apps

Esta organización reúne los proyectos del **Plan 5 — RAG, Agents & Tooling Apps** dentro de **Building Projects**.

Este plan acompaña directamente al:

```txt id="bp5-ai-relation"
AI Engineer Plan 5 — LLMs, RAG, Agents & Agentic Systems
```

La idea central es construir microproductos pequeños y visibles alrededor de búsqueda semántica, recuperación de documentos, evaluación de retrieval y visualización de workflows agentic.

Mientras AI Engineer profundiza en embeddings, semantic search, chunking, RAG, tool use, function calling, agentes, LangGraph, guardrails, MCP y evaluación, Building Projects convierte una parte de ese aprendizaje en herramientas prácticas, claras y publicables.

```txt id="bp5-core"
documentos
→ embeddings
→ búsqueda semántica
→ retrieval
→ evaluación
→ workflow agentic
→ trazas
→ reportes visuales
→ README claro
```

Building Projects no reemplaza los proyectos profundos de AI Engineer.

Los acompaña con herramientas pequeñas que demuestran comprensión aplicada.

---

# 🎯 Objetivo general

Construir herramientas aplicadas de RAG y agentes capaces de:

* Crear búsqueda semántica simple.
* Mostrar documentos recuperados.
* Explicar chunks y fuentes.
* Comparar estrategias de retrieval.
* Visualizar métricas como Recall@K y Precision@K.
* Mostrar trazas de workflows agentic.
* Representar pasos como planner, tool call, evaluator, retry y stop.
* Convertir sistemas LLM en evidencia visible.
* Documentar límites, errores y decisiones.
* Acompañar la ruta principal sin inflar el alcance.

---

# 🔗 Regla de match del Plan 5

Building Projects hará match solo con los proyectos impares de AI Engineer.

```txt id="bp5-match-rule"
Proyecto 25 IA → Proyecto 13 Building
Proyecto 26 IA → Nada
Proyecto 27 IA → Proyecto 14 Building
Proyecto 28 IA → Nada
Proyecto 29 IA → Proyecto 15 Building
Proyecto 30 IA → Nada
```

Esto significa que este plan tendrá **3 proyectos**, no 6.

Cada proyecto Building toma como referencia la duración del proyecto IA correspondiente.

---

# 🗺️ Cronograma Plan 5

| Semana Building |                        Proyecto Building | Match IA |  Duración | Objetivo                                                 |
| --------------- | ---------------------------------------: | -------: | --------: | -------------------------------------------------------- |
| 50-53           |           `13-semantic-search-demo-lite` |    IA 25 | 4 semanas | Crear búsqueda semántica visual con documentos y fuentes |
| 54-57           | `14-retrieval-evaluation-dashboard-lite` |    IA 27 | 4 semanas | Comparar estrategias de retrieval y métricas             |
| 58-62           |         `15-agent-workflow-trace-viewer` |    IA 29 | 5 semanas | Visualizar trazas de workflows agentic                   |

Duración total del Plan 5:

```txt id="bp5-duration"
13 semanas
```

---

# 🧭 Filosofía de trabajo

Los sistemas con LLMs pueden parecer mágicos si no se muestran sus pasos internos.

Este plan existe para que RAG y agentes no se queden como cajas negras.

Regla central:

```txt id="bp5-philosophy"
Un sistema LLM serio debe mostrar de dónde sacó información,
qué recuperó,
qué herramienta usó,
qué decisión tomó
y qué límites tiene.
```

Un Building Project de RAG y agentes debe ser:

```txt id="bp5-values"
pequeño
trazable
visual
explicable
documentado
terminable
```

No debe convertirse en una plataforma agentic pesada.

Debe mostrar una capacidad clara con evidencia.

---

# 🧩 Conceptos base

## Semantic Search

Semantic Search permite buscar por significado, no solo por palabras exactas.

Ejemplo:

```txt id="bp5-semantic-example"
Pregunta:
¿Cómo preparo datos para ML?

Resultado:
Fragmentos sobre limpieza, features, datasets y pipeline,
aunque no usen exactamente las mismas palabras.
```

---

## Chunk

Un chunk es una parte pequeña de un documento.

Sirve para que el sistema pueda recuperar fragmentos relevantes.

La calidad del chunk afecta directamente la calidad del retrieval.

---

## Retrieval Evaluation

Retrieval evaluation mide si el sistema recuperó los fragmentos correctos.

Puede incluir:

* Recall@K.
* Precision@K.
* ranking;
* relevancia manual;
* comparación entre estrategias de chunking;
* notas de error.

---

## Agent Workflow Trace

Una trace de agente muestra los pasos internos de un workflow agentic.

Ejemplo:

```txt id="bp5-agent-trace-example"
user request
→ planner
→ tool call
→ tool result
→ evaluator
→ retry
→ final answer
```

Sin trazas, el agente se vuelve difícil de depurar.

---

# 📁 Proyectos del Plan 5

---

## 13 — semantic-search-demo-lite

### Match

```txt id="bp13-match"
AI Engineer Proyecto 25 — semantic-search-embeddings-api
```

### Duración

```txt id="bp13-duration"
4 semanas
```

---

## 🧠 Descripción

Microproducto ligero de búsqueda semántica con documentos, chunks, embeddings y resultados recuperados.

Este proyecto acompaña al proyecto de AI Engineer donde se construye una API de semantic search con embeddings.

Mientras AI Engineer profundiza en ingestion, chunking, embeddings, vector index y API, este Building Project crea una demo visual y entendible para mostrar cómo funciona la búsqueda semántica.

La idea es mostrar:

```txt id="bp13-core"
documentos
→ chunks
→ embeddings
→ búsqueda
→ top results
→ source cards
→ demo
```

Este proyecto no busca crear un RAG completo.

Busca demostrar búsqueda semántica básica con evidencia visible.

---

## 🎯 Objetivo

Crear una demo donde el usuario escriba una consulta y vea resultados semánticamente relevantes con fuentes visibles.

El objetivo es explicar:

* qué documentos entran;
* cómo se dividen en chunks;
* qué busca el usuario;
* qué resultados se recuperan;
* por qué esos resultados parecen relevantes;
* qué limitaciones tiene la búsqueda.

---

## 👤 Usuario objetivo

* AI Engineer en formación.
* Persona que quiere entender embeddings.
* Usuario que necesita buscar dentro de documentos.
* Reclutador técnico viendo evidencia de semantic search.
* Yo mismo como constructor de portafolio aplicado.

---

## 🧱 Arquitectura esperada

```txt id="bp13-architecture"
Documents
   ↓
Ingestion
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Search
   ↓
Top-K Results
   ↓
Source Cards
   ↓
Demo Lite
```

---

## 🔁 Flujo técnico

```txt id="bp13-flow"
documents
→ load documents
→ split into chunks
→ create embeddings
→ store vectors
→ query
→ retrieve top k
→ show source cards
→ export demo
```

---

## 🧩 Módulos

### Módulo 1 — Document Ingestion

Cargar documentos pequeños.

Incluye:

* documentos `.txt` o `.md`;
* fuente;
* título;
* contenido;
* metadata simple;
* limitaciones.

Pregunta central:

```txt id="bp13-q1"
¿Qué documentos voy a hacer buscables?
```

---

### Módulo 2 — Chunking

Dividir documentos en fragmentos.

Incluye:

* tamaño de chunk;
* overlap si aplica;
* chunk id;
* fuente;
* texto recuperable;
* notas de limitación.

Pregunta central:

```txt id="bp13-q2"
¿Cómo divido documentos sin perder contexto?
```

---

### Módulo 3 — Embedding Notes

Crear o simular embeddings.

Incluye:

* representación vectorial;
* relación con significado;
* consulta;
* similitud;
* límites.

Pregunta central:

```txt id="bp13-q3"
¿Cómo convierte el sistema texto en algo comparable por significado?
```

---

### Módulo 4 — Semantic Search

Ejecutar búsqueda semántica.

Incluye:

* query del usuario;
* top-k resultados;
* score de similitud si aplica;
* ranking;
* fragmentos recuperados.

Pregunta central:

```txt id="bp13-q4"
¿Qué fragmentos se parecen más al significado de la consulta?
```

---

### Módulo 5 — Source Cards

Mostrar resultados como tarjetas.

Cada tarjeta debe incluir:

* título del documento;
* chunk recuperado;
* score si aplica;
* por qué parece relevante;
* limitación.

Pregunta central:

```txt id="bp13-q5"
¿Cómo muestro resultados de búsqueda de forma clara y confiable?
```

---

### Módulo 6 — Demo Lite

Crear vista final.

Puede ser:

* Streamlit simple;
* notebook visual;
* `dashboard/README.md`;
* HTML ligero.

Debe mostrar:

* caja de búsqueda;
* resultados;
* source cards;
* limitaciones.

Pregunta central:

```txt id="bp13-q6"
¿Puede alguien probar búsqueda semántica sin abrir el código?
```

---

## 🧪 Labs

### tec-labs

* `tec-document-ingestion-lab`
* `tec-basic-chunking-lab`
* `tec-embedding-concept-lab`
* `tec-semantic-search-lab`
* `tec-source-card-lab`

### docs-labs

* `docs-semantic-search-storytelling-lab`
* `docs-source-display-template-lab`

### cloud-labs

* `cloud-documents-to-gcp-storage-lab`
* `cloud-documents-to-aws-s3-lab`
* `cloud-documents-to-azure-blob-lab`

---

## 📊 Métricas / Evidencia

* Número de documentos.
* Número de chunks.
* Top-K results.
* Similarity score si aplica.
* Source cards.
* Query examples.
* Failure examples.
* Demo visual.
* Capturas.
* README profesional.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt id="bp13-cycle"
Semana 1 → Documentos, ingestion y chunking
Semana 2 → Embeddings, búsqueda semántica y top-k results
Semana 3 → Source cards, ejemplos de consulta y demo
Semana 4 → Labs, README, capturas y cierre
```

---

## 📌 Próximos pasos

* Elegir documentos pequeños.
* Crear ingestion.
* Crear chunking.
* Crear embeddings o simulación.
* Crear búsqueda semántica.
* Mostrar top-k results.
* Crear source cards.
* Crear demo ligera.
* Documentar limitaciones.
* Agregar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Demo de búsqueda semántica.
* Documentos de ejemplo.
* Chunks.
* Embeddings o representación conceptual.
* Top-K results.
* Source cards.
* Labs documentados.
* README profesional.
* Capturas u outputs visibles.
* Conexión clara con `semantic-search-embeddings-api`.

---

## 🧭 Regla final

```txt id="bp13-rule"
Semantic search no es solo devolver texto.
Debe mostrar fuentes, fragmentos, relevancia y límites.

La confianza empieza cuando el usuario puede ver de dónde salió el resultado.
```

---

# 14 — retrieval-evaluation-dashboard-lite

### Match

```txt id="bp14-match"
AI Engineer Proyecto 27 — chunking-retrieval-evaluation-lab
```

### Duración

```txt id="bp14-duration"
4 semanas
```

---

## 🧠 Descripción

Dashboard ligero para comparar estrategias de chunking y métricas de retrieval.

Este proyecto acompaña al proyecto de AI Engineer donde se evalúan estrategias de chunking, retrieval test sets, relevancia manual, Recall@K y Precision@K.

Mientras AI Engineer profundiza en evaluación formal de retrieval, este Building Project crea un dashboard visual para comparar resultados de forma clara.

La idea es mostrar:

```txt id="bp14-core"
documentos
→ estrategias de chunking
→ queries de prueba
→ resultados recuperados
→ etiquetas de relevancia
→ métricas
→ dashboard
```

Este proyecto no busca construir un evaluador enterprise de RAG.

Busca mostrar cómo comparar retrieval con evidencia visible.

---

## 🎯 Objetivo

Crear un dashboard que permita comparar estrategias de retrieval usando métricas simples y ejemplos de resultados.

El objetivo es explicar:

* qué estrategia de chunking se usó;
* qué queries se probaron;
* qué resultados se recuperaron;
* cuáles eran relevantes;
* qué métricas salieron;
* qué estrategia funcionó mejor y por qué.

---

## 👤 Usuario objetivo

* AI Engineer en formación.
* Persona construyendo RAG.
* Equipo que necesita evaluar retrieval.
* Reclutador técnico viendo criterio de evaluación.
* Yo mismo como constructor de evidencia aplicada.

---

## 🧱 Arquitectura esperada

```txt id="bp14-architecture"
Documents
   ↓
Chunking Strategy A / B
   ↓
Retrieval Test Queries
   ↓
Retrieved Results
   ↓
Manual Relevance Labels
   ↓
Recall@K / Precision@K
   ↓
Comparison Dashboard
```

---

## 🔁 Flujo técnico

```txt id="bp14-flow"
documents
→ build chunks
→ define test queries
→ retrieve top k
→ label relevance
→ calculate metrics
→ compare strategies
→ export dashboard
```

---

## 🧩 Módulos

### Módulo 1 — Chunking Strategy Setup

Definir estrategias de chunking.

Puede incluir:

* chunks pequeños;
* chunks medianos;
* overlap;
* sin overlap;
* comparación simple.

Pregunta central:

```txt id="bp14-q1"
¿Cómo afecta el tamaño del chunk al retrieval?
```

---

### Módulo 2 — Retrieval Test Set

Crear queries de prueba.

Incluye:

* query;
* intención;
* respuesta esperada conceptual;
* documentos relevantes;
* notas.

Pregunta central:

```txt id="bp14-q2"
¿Qué consultas usaré para probar si el retrieval funciona?
```

---

### Módulo 3 — Retrieved Results Table

Guardar resultados recuperados.

Incluye:

* query;
* estrategia;
* top-k resultados;
* chunk id;
* documento fuente;
* score.

Pregunta central:

```txt id="bp14-q3"
¿Qué recuperó cada estrategia?
```

---

### Módulo 4 — Relevance Labels

Asignar relevancia manual.

Incluye:

* relevante;
* parcialmente relevante;
* no relevante;
* razón;
* notas de error.

Pregunta central:

```txt id="bp14-q4"
¿Cuáles resultados realmente ayudan a responder la consulta?
```

---

### Módulo 5 — Metrics Calculator

Calcular métricas simples.

Incluye:

* Recall@K;
* Precision@K;
* hit rate;
* comparación por query;
* comparación por estrategia.

Pregunta central:

```txt id="bp14-q5"
¿Qué estrategia recupera mejor la información correcta?
```

---

### Módulo 6 — Comparison Dashboard

Crear vista final.

Puede ser:

* Streamlit simple;
* notebook visual;
* `dashboard/README.md`;
* HTML ligero.

Debe mostrar:

* estrategias;
* métricas;
* tablas;
* ejemplos;
* conclusiones.

Pregunta central:

```txt id="bp14-q6"
¿Puede alguien ver qué estrategia de retrieval conviene sin leer el código?
```

---

## 🧪 Labs

### tec-labs

* `tec-chunking-strategy-comparison-lab`
* `tec-retrieval-test-set-lab`
* `tec-relevance-labeling-lab`
* `tec-recall-at-k-lab`
* `tec-precision-at-k-lab`

### docs-labs

* `docs-retrieval-evaluation-storytelling-lab`
* `docs-rag-evaluation-report-template-lab`

### cloud-labs

* `cloud-retrieval-report-to-gcp-storage-lab`
* `cloud-retrieval-report-to-aws-s3-lab`
* `cloud-retrieval-report-to-azure-blob-lab`

---

## 📊 Métricas / Evidencia

* Número de documentos.
* Número de chunks por estrategia.
* Número de queries.
* Top-K results.
* Relevance labels.
* Recall@K.
* Precision@K.
* Hit rate.
* Comparison table.
* Dashboard visual.
* Capturas.
* README profesional.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt id="bp14-cycle"
Semana 1 → Estrategias de chunking y test queries
Semana 2 → Retrieval results y relevance labels
Semana 3 → Métricas, comparación y dashboard
Semana 4 → Labs, README, capturas y cierre
```

---

## 📌 Próximos pasos

* Elegir documentos pequeños.
* Definir estrategias de chunking.
* Crear test queries.
* Ejecutar retrieval.
* Guardar top-k results.
* Etiquetar relevancia.
* Calcular Recall@K.
* Calcular Precision@K.
* Crear dashboard.
* Documentar limitaciones.
* Agregar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Dashboard de evaluación retrieval.
* Documentos de ejemplo.
* Estrategias de chunking.
* Test queries.
* Retrieved results table.
* Relevance labels.
* Recall@K.
* Precision@K.
* Comparación de estrategias.
* Labs documentados.
* README profesional.
* Capturas u outputs visibles.
* Conexión clara con `chunking-retrieval-evaluation-lab`.

---

## 🧭 Regla final

```txt id="bp14-rule"
Un RAG no mejora solo porque responde bonito.
Primero debe recuperar bien.

Evaluar retrieval es medir si el sistema encontró la evidencia correcta.
```

---

# 15 — agent-workflow-trace-viewer

### Match

```txt id="bp15-match"
AI Engineer Proyecto 29 — agentic-workflow-langgraph-lab
```

### Duración

```txt id="bp15-duration"
5 semanas
```

---

## 🧠 Descripción

Visualizador ligero de trazas de workflows agentic.

Este proyecto acompaña al proyecto de AI Engineer donde se trabaja agentic workflow, estado, planner node, tool executor, evaluator, retry/stop conditions y workflow trace.

Mientras AI Engineer profundiza en arquitectura agentic con LangGraph o herramienta equivalente, este Building Project crea una herramienta visual para mostrar qué hizo el agente paso a paso.

La idea es mostrar:

```txt id="bp15-core"
solicitud del usuario
→ planner
→ tool call
→ resultado de herramienta
→ evaluación
→ retry / stop
→ respuesta final
→ trace viewer
```

Este proyecto no busca crear un agente avanzado.

Busca mostrar cómo se puede observar, explicar y depurar un workflow agentic.

---

## 🎯 Objetivo

Crear un viewer que muestre los pasos de un agente, sus decisiones, tools usadas, errores, retries y condición de cierre.

El objetivo es explicar:

* qué pidió el usuario;
* qué plan creó el agente;
* qué herramienta llamó;
* qué resultado recibió;
* cómo evaluó el resultado;
* cuándo hizo retry;
* cuándo se detuvo;
* qué limitaciones tuvo.

---

## 👤 Usuario objetivo

* AI Engineer en formación.
* Persona interesada en agentes.
* Equipo que necesita depurar workflows agentic.
* Reclutador técnico viendo evidencia de sistemas con trazas.
* Yo mismo como constructor de portafolio aplicado.

---

## 🧱 Arquitectura esperada

```txt id="bp15-architecture"
User Request
      ↓
Planner Node
      ↓
Tool Executor
      ↓
Tool Result
      ↓
Evaluator Node
      ↓
Retry / Stop Condition
      ↓
Final Answer
      ↓
Trace Viewer
```

---

## 🔁 Flujo técnico

```txt id="bp15-flow"
user request
→ generate plan
→ select tool
→ execute tool
→ store result
→ evaluate result
→ retry or stop
→ render trace
```

---

## 🧩 Módulos

### Módulo 1 — Trace Schema

Definir formato de una traza.

Incluye:

* step id;
* node name;
* input;
* action;
* output;
* status;
* error si aplica;
* timestamp conceptual.

Pregunta central:

```txt id="bp15-q1"
¿Qué información necesito guardar para entender lo que hizo un agente?
```

---

### Módulo 2 — Planner Step Viewer

Mostrar el paso de planificación.

Incluye:

* solicitud del usuario;
* plan creado;
* pasos propuestos;
* objetivo;
* limitación.

Pregunta central:

```txt id="bp15-q2"
¿Qué decidió hacer el agente antes de usar herramientas?
```

---

### Módulo 3 — Tool Call Viewer

Mostrar llamadas a herramientas.

Incluye:

* tool name;
* argumentos;
* resultado;
* error si aplica;
* validación.

Pregunta central:

```txt id="bp15-q3"
¿Qué herramienta usó el agente y con qué argumentos?
```

---

### Módulo 4 — Evaluation Step Viewer

Mostrar evaluación del resultado.

Incluye:

* resultado recibido;
* criterio de evaluación;
* aprobado / fallido;
* razón;
* siguiente acción.

Pregunta central:

```txt id="bp15-q4"
¿Cómo decide el agente si el resultado sirve?
```

---

### Módulo 5 — Retry / Stop Condition

Mostrar retries y cierre.

Incluye:

* motivo de retry;
* número de intento;
* condición de parada;
* respuesta final;
* advertencia.

Pregunta central:

```txt id="bp15-q5"
¿Cuándo debe intentar de nuevo y cuándo debe detenerse?
```

---

### Módulo 6 — Trace Viewer

Crear vista final.

Puede ser:

* Streamlit simple;
* notebook visual;
* `dashboard/README.md`;
* HTML ligero.

Debe mostrar:

* timeline;
* nodos;
* tools;
* errores;
* retries;
* respuesta final.

Pregunta central:

```txt id="bp15-q6"
¿Puede alguien entender el comportamiento del agente sin leer el código?
```

---

## 🧪 Labs

### tec-labs

* `tec-agent-trace-schema-lab`
* `tec-planner-node-viewer-lab`
* `tec-tool-call-viewer-lab`
* `tec-evaluator-node-viewer-lab`
* `tec-retry-stop-condition-lab`

### docs-labs

* `docs-agent-trace-storytelling-lab`
* `docs-agent-debug-report-template-lab`

### cloud-labs

* `cloud-agent-traces-to-gcp-storage-lab`
* `cloud-agent-traces-to-aws-s3-lab`
* `cloud-agent-traces-to-azure-blob-lab`

---

## 📊 Métricas / Evidencia

* Número de pasos.
* Tool calls.
* Tool success/failure.
* Número de retries.
* Stop condition.
* Trace timeline.
* Error notes.
* Final answer.
* Viewer visual.
* Capturas.
* README profesional.

---

## 🚀 Estado actual

Pendiente / por iniciar.

---

## 🧭 Ciclo de trabajo

```txt id="bp15-cycle"
Semana 1 → Trace schema, ejemplos y planner step
Semana 2 → Tool call viewer y tool result cards
Semana 3 → Evaluator, retry y stop condition
Semana 4 → Trace viewer, error notes y debug report
Semana 5 → Labs, README, capturas y cierre
```

---

## 📌 Próximos pasos

* Definir trace schema.
* Crear ejemplo de user request.
* Crear planner step.
* Crear tool call example.
* Crear tool result card.
* Crear evaluator step.
* Crear retry example.
* Crear stop condition.
* Crear trace viewer.
* Documentar limitaciones.
* Agregar capturas.
* Publicar repo.

---

## ✅ Entregable final

Al terminar este proyecto debe existir:

* Agent workflow trace viewer.
* Trace schema.
* Planner step viewer.
* Tool call viewer.
* Evaluation step viewer.
* Retry / stop condition.
* Error notes.
* Debug report.
* Labs documentados.
* README profesional.
* Capturas u outputs visibles.
* Conexión clara con `agentic-workflow-langgraph-lab`.

---

## 🧭 Regla final

```txt id="bp15-rule"
Un agente sin trazas es difícil de confiar y difícil de depurar.
No basta con que responda.

Debo poder ver qué pensó, qué herramienta usó, qué falló y por qué se detuvo.
```

---

# 🧱 Ciclo general de cada proyecto

Cada proyecto del Plan 5 sigue este ciclo:

```txt id="bp5-cycle-general"
1. Definir microproducto.
2. Definir usuario.
3. Definir qué debe entenderse.
4. Elegir ejemplos pequeños.
5. Crear README inicial.
6. Crear estructura mínima.
7. Crear primera demo.
8. Agregar tarjetas explicativas.
9. Crear labs pequeños.
10. Probar si aplica.
11. Documentar decisiones.
12. Agregar capturas.
13. Preparar demo o evidencia.
14. Escribir aprendizajes.
15. Definir limitaciones.
16. Definir siguiente paso.
17. Publicar en GitHub.
18. Conectar con el proyecto IA correspondiente.
```

---

# 🗂️ Estructura recomendada del repositorio

```txt id="bp5-repo-structure"
RAG-Agents-and-Tooling-Apps/
├── 13-semantic-search-demo-lite/
│   ├── data/
│   ├── src/
│   ├── reports/
│   ├── dashboard/
│   ├── docs/
│   ├── labs/
│   ├── scripts/
│   └── README.md
│
├── 14-retrieval-evaluation-dashboard-lite/
│   ├── data/
│   ├── src/
│   ├── reports/
│   ├── dashboard/
│   ├── docs/
│   ├── labs/
│   └── README.md
│
├── 15-agent-workflow-trace-viewer/
│   ├── data/
│   ├── src/
│   ├── reports/
│   ├── dashboard/
│   ├── docs/
│   ├── labs/
│   └── README.md
│
└── README.md
```

---

# 📊 Nivel esperado al terminar Plan 5

| Área                               | Nivel esperado |
| ---------------------------------- | -------------: |
| Semantic search aplicado           |           8/10 |
| Chunking básico                    |           8/10 |
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

# 🧠 Resultado esperado del Plan 5

Al completar este plan, podré decir:

```txt id="bp5-result"
Sé crear demos ligeras de búsqueda semántica.
Sé mostrar documentos, chunks y fuentes recuperadas.
Sé evaluar retrieval con métricas visibles.
Sé comparar estrategias de chunking.
Sé diseñar dashboards de evaluación RAG.
Sé visualizar workflows agentic.
Sé mostrar planner, tool calls, evaluator, retries y stop condition.
Sé convertir sistemas LLM en evidencia trazable.
```

---

# 🧭 Regla final de avance

```txt id="bp5-final-rule"
Un sistema LLM no debe ser una caja negra.
Debe mostrar fuentes, pasos, herramientas, evaluación y límites.

Lo que no se puede observar,
se vuelve difícil de confiar.
```

Frase guía:

```txt id="bp5-final-phrase"
AI Engineer me enseña a construir RAG y agentes.
Building Projects me obliga a hacerlos visibles, trazables y explicables.
```

---

# 👤 Autor

**Jean Franck Loa Rojas**

Building Projects Path Builder
RAG • Semantic Search • Retrieval Evaluation • Agents • Tool Use • Trace Viewer • Technical Storytelling
