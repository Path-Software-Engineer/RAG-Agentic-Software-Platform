# 14-retrieval-evaluation-dashboard-lite

## 🧠 Descripción

Dashboard ligero para comparar estrategias de chunking y métricas de retrieval.

Este proyecto pertenece a la ruta:

```txt id="bp14-route"
Building Projects
```

y acompaña directamente al proyecto:

```txt id="bp14-match"
AI Engineer Proyecto 27 — chunking-retrieval-evaluation-lab
```

Mientras AI Engineer profundiza en evaluación formal de retrieval, estrategias de chunking, test sets, relevancia manual, Recall@K y Precision@K, este Building Project crea un dashboard visual para comparar resultados de forma clara.

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

* Qué estrategia de chunking se usó.
* Qué queries se probaron.
* Qué resultados se recuperaron.
* Cuáles resultados eran relevantes.
* Qué métricas salieron.
* Qué estrategia funcionó mejor y por qué.
* Qué limitaciones tiene la evaluación.

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

* Chunks pequeños.
* Chunks medianos.
* Overlap.
* Sin overlap.
* Comparación simple.
* Notas de impacto.

Pregunta central:

```txt id="bp14-q1"
¿Cómo afecta el tamaño del chunk al retrieval?
```

---

### Módulo 2 — Retrieval Test Set

Crear queries de prueba.

Incluye:

* Query.
* Intención.
* Respuesta esperada conceptual.
* Documentos relevantes.
* Notas.

Pregunta central:

```txt id="bp14-q2"
¿Qué consultas usaré para probar si el retrieval funciona?
```

---

### Módulo 3 — Retrieved Results Table

Guardar resultados recuperados.

Incluye:

* Query.
* Estrategia.
* Top-K resultados.
* Chunk ID.
* Documento fuente.
* Score.

Pregunta central:

```txt id="bp14-q3"
¿Qué recuperó cada estrategia?
```

---

### Módulo 4 — Relevance Labels

Asignar relevancia manual.

Incluye:

* Relevante.
* Parcialmente relevante.
* No relevante.
* Razón.
* Notas de error.

Pregunta central:

```txt id="bp14-q4"
¿Cuáles resultados realmente ayudan a responder la consulta?
```

---

### Módulo 5 — Metrics Calculator

Calcular métricas simples.

Incluye:

* Recall@K.
* Precision@K.
* Hit rate.
* Comparación por query.
* Comparación por estrategia.

Pregunta central:

```txt id="bp14-q5"
¿Qué estrategia recupera mejor la información correcta?
```

---

### Módulo 6 — Error Examples

Documentar fallos del retrieval.

Incluye:

* No recuperó evidencia importante.
* Recuperó fragmento irrelevante.
* Ranking incorrecto.
* Chunk demasiado corto.
* Chunk demasiado largo.
* Problemas de overlap.

Pregunta central:

```txt id="bp14-q6"
¿Qué errores muestran que el retrieval todavía debe mejorar?
```

---

### Módulo 7 — Comparison Dashboard

Crear vista final.

Puede ser:

* Streamlit simple.
* Notebook visual.
* `dashboard/README.md`.
* HTML ligero.

Debe mostrar:

* Estrategias.
* Métricas.
* Tablas.
* Ejemplos.
* Conclusiones.

Pregunta central:

```txt id="bp14-q7"
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
* `tec-retrieval-error-examples-lab`

### docs-labs

* `docs-retrieval-evaluation-storytelling-lab`
* `docs-rag-evaluation-report-template-lab`

### cloud-labs

* `cloud-retrieval-report-to-gcp-storage-lab`
* `cloud-retrieval-report-to-aws-s3-lab`
* `cloud-retrieval-report-to-azure-blob-lab`

---

## 📊 Métricas / Evidencia

Este proyecto puede generar:

* Número de documentos.
* Número de chunks por estrategia.
* Número de queries.
* Top-K results.
* Relevance labels.
* Recall@K.
* Precision@K.
* Hit rate.
* Comparison table.
* Error examples.
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
Semana 3 → Métricas, comparación, errores y dashboard
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
* Documentar errores.
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
* Error examples.
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

Este proyecto debe demostrar que puedo evaluar recuperación de información con métricas, ejemplos y criterio visual.
