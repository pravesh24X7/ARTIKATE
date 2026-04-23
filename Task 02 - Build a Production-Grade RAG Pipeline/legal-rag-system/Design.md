## 1. Chunking Strategy

I used a RecursiveCharacterTextSplitter with:

* chunk size: ~600–700 characters
* chunk overlap: ~100 characters

### Why this approach

Legal documents are structured in clauses and paragraphs. Important meaning is usually present within a clause, not a single sentence.

If chunk size is:

* too small → meaning gets broken
* too large → retrieval becomes noisy

Overlap is added to:

* preserve context across boundaries
* avoid losing important information at edges

This balance helps in retrieving complete and meaningful legal clauses.



## 2. Embedding Model Choice

I used:

* sentence-transformers/all-MiniLM-L6-v2

### Why this model

* Fast and lightweight
* Good semantic similarity performance
* Works well for short-to-medium text chunks
* Easy to run locally without GPU

### Limitation

* Not trained specifically on legal domain
* May miss some domain-specific language

But for this assignment scale, it gives a good trade-off between speed and accuracy.



## 3. Vector Store Choice (FAISS vs Pinecone vs Others)

I used **FAISS** as the vector store.

### Why FAISS

* Runs locally (no external dependency)
* Fast similarity search
* Simple to set up and integrate
* Works well for small to medium datasets (like 500 PDFs)



### Why NOT Pinecone

Pinecone is a managed vector database and is better for production systems, but I did not use it because:

* Requires API key and external service
* Adds network latency
* Not necessary for small dataset
* Overkill for this assignment

Since the dataset size is small and system runs locally, FAISS is more efficient and simpler.



### Why NOT Chroma

* Chroma is easier for metadata handling
* But FAISS is faster and more mature for similarity search

So FAISS was chosen as a better low-level and efficient option.



## 4. Retrieval Strategy

I used **top-k retrieval with k=3**.

### Why top-k

* Simple and effective
* Ensures most relevant chunks are retrieved
* Works well for precise legal queries



### Why k = 3

* Keeps only highly relevant chunks
* Reduces noise in context
* Improves answer quality



### Limitations

* Does not use keyword matching
* May miss exact phrase queries



### Possible Improvement

Hybrid retrieval:

* Combine dense embeddings + keyword search (BM25)

This is useful in legal cases where:

* exact terms matter
* numeric values (₹1 crore) are important



## 5. Full Pipeline Implementation

The system follows this flow:

1. Document ingestion

   * Load PDF files using PyPDFLoader

2. Chunking

   * Split into smaller overlapping chunks

3. Embedding

   * Convert chunks into vector representations

4. Vector Store

   * Store embeddings using FAISS

5. Retrieval

   * Retrieve top-3 relevant chunks

6. Generation

   * Pass retrieved chunks to LLM
   * Generate answer

7. Source Citation

   * Return:

     * document name
     * page number
     * chunk text



## 6. Evaluation Harness

I created:

* 10 manual question–answer pairs

For each question:

* retrieve top 3 chunks
* check if correct answer exists in those chunks

### Metric: Precision@3

Precision@3 =
(number of queries where correct chunk is in top 3) / total queries

### Result

Precision@3 ≈ 0.7

This means:

* in 70% cases, correct chunk is retrieved in top 3



## 7. Hallucination Mitigation Strategy

I implemented **answer refusal + source grounding**.

### Method

* If no relevant chunks are retrieved:
  → return "Not found"

* Answer is generated ONLY from retrieved context

* Confidence score is calculated based on:

  * number of retrieved chunks



### Why this works

* Prevents model from generating unsupported answers
* Ensures answers are grounded in documents
* Reduces hallucination risk



## 8. Scaling to 50,000 Documents

If dataset increases significantly, current system will face issues.

### Bottlenecks

1. FAISS (local storage)

   * memory limitations
   * slower search

2. Embedding generation

   * slow for large corpus

3. Retrieval latency

   * increases with dataset size



### Solutions

#### 1. Replace FAISS with Pinecone or Weaviate

* distributed storage
* scalable
* faster retrieval

#### 2. Use Hybrid Retrieval

* combine vector search + keyword search (Elasticsearch)

#### 3. Add Re-ranking

* use cross-encoder model to improve top-k results

#### 4. Batch Embedding

* process documents in parallel

#### 5. Caching

* cache frequent queries
* reduce repeated computation



## Final Conclusion

The system is designed to:

* retrieve relevant legal content
* generate grounded answers
* provide source citations
* avoid hallucination

FAISS is chosen because it is simple and efficient for current scale, while Pinecone is better suited for large-scale production systems.
