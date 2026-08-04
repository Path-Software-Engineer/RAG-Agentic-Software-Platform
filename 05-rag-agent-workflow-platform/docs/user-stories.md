# User Stories — Sprint 1

## US-501 — Register and index controlled documents

**Story:** As a knowledge user, I want to upload an allowed document so that its content becomes searchable without exposing infrastructure details.

**Acceptance criteria:**

- Given a UTF-8 `.txt` or `.md` file within the size limit, when it is uploaded, then the API returns a stable document ID, version ID, ingestion job ID, status, and correlation ID.
- Given identical bytes, when the file is uploaded again, then the existing document is returned and no duplicate version or chunks are created.
- Given an unsupported, empty, oversized, or non-UTF-8 file, when it is uploaded, then the API returns a stable validation error and stores no document.
- Given an accepted version, when ingestion completes, then its chunks retain document, version, order, offsets, and chunking version.

**Status:** Implemented in the Sprint 1 working tree.

**Evidence:** `backend/nestjs-api/src/documents`, `ai-services/rag-agent-service/app/ingestion`, `database/migrations/001_sprint_01_initial.sql`, `/documents`.

## US-502 — Search with resolvable sources

**Story:** As a knowledge user, I want ranked fragments with visible sources so that I can inspect where every result came from.

**Acceptance criteria:**

- Given indexed documents and a valid query, when search runs, then results are ordered and every result includes score, document ID, version ID, chunk ID, and citation ID.
- Given an allowed document filter, when search runs, then results are limited to those documents.
- Given a citation ID, when it is opened, then the API resolves its snippet and locator to an existing chunk and document resource.
- Given no matching indexed content, when search runs, then the UI shows an explicit empty state and does not invent an answer.
- The UI explains that similarity is a ranking signal rather than confidence or truth.

**Status:** Implemented in the Sprint 1 working tree.

**Evidence:** `ai-services/rag-agent-service/app/retrieval`, `backend/nestjs-api/src/search`, `frontend/sveltekit-app/src/routes/search`, `frontend/sveltekit-app/src/routes/citations`.
