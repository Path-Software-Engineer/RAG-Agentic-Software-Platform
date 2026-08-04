# Retrieval safety

Retrieved text is untrusted data. A search result can provide evidence, but it cannot replace system policy or authorize a tool. Every visible result must retain its document, version, chunk, and locator so an operator can inspect the source.

The first release uses exact cosine search as a reference. Similarity is a ranking signal, not a probability, confidence score, or guarantee that the passage answers the question.
