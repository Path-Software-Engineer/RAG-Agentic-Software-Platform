# 15-agent-workflow-trace-viewer

## 🧠 Descripción

Visualizador ligero de trazas de workflows agentic.

Este proyecto pertenece a la ruta:

```txt id="bp15-route"
Building Projects
```

y acompaña directamente al proyecto:

```txt id="bp15-match"
AI Engineer Proyecto 29 — agentic-workflow-langgraph-lab
```

Mientras AI Engineer profundiza en arquitectura agentic con estado, planner node, tool executor, evaluator, retry/stop conditions y workflow trace, este Building Project crea una herramienta visual para mostrar qué hizo el agente paso a paso.

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

* Qué pidió el usuario.
* Qué plan creó el agente.
* Qué herramienta llamó.
* Qué argumentos usó.
* Qué resultado recibió.
* Cómo evaluó el resultado.
* Cuándo hizo retry.
* Cuándo se detuvo.
* Qué limitaciones tuvo.

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

* Step ID.
* Node name.
* Input.
* Action.
* Output.
* Status.
* Error si aplica.
* Timestamp conceptual.

Pregunta central:

```txt id="bp15-q1"
¿Qué información necesito guardar para entender lo que hizo un agente?
```

---

### Módulo 2 — Planner Step Viewer

Mostrar el paso de planificación.

Incluye:

* Solicitud del usuario.
* Plan creado.
* Pasos propuestos.
* Objetivo.
* Limitación.

Pregunta central:

```txt id="bp15-q2"
¿Qué decidió hacer el agente antes de usar herramientas?
```

---

### Módulo 3 — Tool Call Viewer

Mostrar llamadas a herramientas.

Incluye:

* Tool name.
* Argumentos.
* Resultado.
* Error si aplica.
* Validación.

Pregunta central:

```txt id="bp15-q3"
¿Qué herramienta usó el agente y con qué argumentos?
```

---

### Módulo 4 — Tool Result Card

Convertir el resultado de la herramienta en tarjeta.

Incluye:

* Tool usada.
* Input enviado.
* Output recibido.
* Estado.
* Posible error.
* Interpretación.

Pregunta central:

```txt id="bp15-q4"
¿Qué devolvió la herramienta y cómo lo entiende el agente?
```

---

### Módulo 5 — Evaluation Step Viewer

Mostrar evaluación del resultado.

Incluye:

* Resultado recibido.
* Criterio de evaluación.
* Aprobado / fallido.
* Razón.
* Siguiente acción.

Pregunta central:

```txt id="bp15-q5"
¿Cómo decide el agente si el resultado sirve?
```

---

### Módulo 6 — Retry / Stop Condition

Mostrar retries y cierre.

Incluye:

* Motivo de retry.
* Número de intento.
* Condición de parada.
* Respuesta final.
* Advertencia.

Pregunta central:

```txt id="bp15-q6"
¿Cuándo debe intentar de nuevo y cuándo debe detenerse?
```

---

### Módulo 7 — Trace Viewer

Crear vista final.

Puede ser:

* Streamlit simple.
* Notebook visual.
* `dashboard/README.md`.
* HTML ligero.

Debe mostrar:

* Timeline.
* Nodos.
* Tools.
* Errores.
* Retries.
* Respuesta final.

Pregunta central:

```txt id="bp15-q7"
¿Puede alguien entender el comportamiento del agente sin leer el código?
```

---

## 🧪 Labs

### tec-labs

* `tec-agent-trace-schema-lab`
* `tec-planner-node-viewer-lab`
* `tec-tool-call-viewer-lab`
* `tec-tool-result-card-lab`
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

Este proyecto puede generar:

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
* Tool result cards.
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

Este proyecto debe demostrar que puedo convertir un workflow agentic en una herramienta observable y explicable.
