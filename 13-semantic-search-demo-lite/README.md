# 13-semantic-search-demo-lite

## 🧠 Descripción

Microproducto ligero de búsqueda semántica con documentos, chunks, embeddings y resultados recuperados.

Este proyecto pertenece a la ruta:

```txt id="bp13-route"
Building Projects
```

y acompaña directamente al proyecto:

```txt id="bp13-match"
AI Engineer Proyecto 25 — semantic-search-embeddings-api
```

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

* Qué documentos entran.
* Cómo se dividen en chunks.
* Qué busca el usuario.
* Qué resultados se recuperan.
* Por qué esos resultados parecen relevantes.
* Qué limitaciones tiene la búsqueda.

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

* Documentos `.txt` o `.md`.
* Fuente.
* Título.
* Contenido.
* Metadata simple.
* Limitaciones.

Pregunta central:

```txt id="bp13-q1"
¿Qué documentos voy a hacer buscables?
```

---

### Módulo 2 — Chunking

Dividir documentos en fragmentos.

Incluye:

* Tamaño de chunk.
* Overlap si aplica.
* Chunk ID.
* Fuente.
* Texto recuperable.
* Notas de limitación.

Pregunta central:

```txt id="bp13-q2"
¿Cómo divido documentos sin perder contexto?
```

---

### Módulo 3 — Embedding Notes

Crear o simular embeddings.

Incluye:

* Representación vectorial.
* Relación con significado.
* Consulta.
* Similitud.
* Límites.

Pregunta central:

```txt id="bp13-q3"
¿Cómo convierte el sistema texto en algo comparable por significado?
```

---

### Módulo 4 — Semantic Search

Ejecutar búsqueda semántica.

Incluye:

* Query del usuario.
* Top-K resultados.
* Score de similitud si aplica.
* Ranking.
* Fragmentos recuperados.

Pregunta central:

```txt id="bp13-q4"
¿Qué fragmentos se parecen más al significado de la consulta?
```

---

### Módulo 5 — Source Cards

Mostrar resultados como tarjetas.

Cada tarjeta debe incluir:

* Título del documento.
* Chunk recuperado.
* Score si aplica.
* Por qué parece relevante.
* Limitación.

Pregunta central:

```txt id="bp13-q5"
¿Cómo muestro resultados de búsqueda de forma clara y confiable?
```

---

### Módulo 6 — Query Examples

Crear ejemplos de búsqueda.

Incluye:

* Consulta fácil.
* Consulta ambigua.
* Consulta fuera del alcance.
* Resultado esperado.
* Resultado recuperado.

Pregunta central:

```txt id="bp13-q6"
¿Qué tipo de consultas prueban si la búsqueda funciona de verdad?
```

---

### Módulo 7 — Demo Lite

Crear vista final.

Puede ser:

* Streamlit simple.
* Notebook visual.
* `dashboard/README.md`.
* HTML ligero.

Debe mostrar:

* Caja de búsqueda.
* Resultados.
* Source cards.
* Limitaciones.

Pregunta central:

```txt id="bp13-q7"
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
* `tec-query-examples-lab`

### docs-labs

* `docs-semantic-search-storytelling-lab`
* `docs-source-display-template-lab`

### cloud-labs

* `cloud-documents-to-gcp-storage-lab`
* `cloud-documents-to-aws-s3-lab`
* `cloud-documents-to-azure-blob-lab`

---

## 📊 Métricas / Evidencia

Este proyecto puede generar:

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
* Crear ejemplos de query.
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
* Query examples.
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

Este proyecto debe demostrar que puedo convertir búsqueda semántica en una demo clara, útil y confiable.
