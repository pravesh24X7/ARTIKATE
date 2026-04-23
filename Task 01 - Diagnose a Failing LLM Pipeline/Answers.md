## Question 1: (Hallucinated Pricing)

**Problem:**  
Chatbot gives wrong product prices confidently.

**Answer:**  
This indicates the chatbot is experiencing hallucination.

### Possible Reasons:

1. **High Temperature Value**
   - Default value is usually `0.7`.
   - Higher temperature (> 0.7) increases creativity and leads to guessing.
   - Lower values preserve factual accuracy.

   **Solution:**
   - Reduce `temperature` to around `0.5` (or any value ≤ 0.7).

2. **RAG Pipeline Issues**
   - Possible wrong vector store configuration.
   - Inefficient similarity search algorithm.
   - Redundant or low-quality retrieved documents.

   **Testing Retrieval:**
   - Query: `"What is the price of Product X?"`
   - Evaluate:
     - Is correct data fetched? → If not, vector store misconfigured.
     - Are retrieved documents accurate? → If not, similarity search is weak.

   **Solutions:**
   - Reconfigure vector store if incorrect data is fetched.
   - Use better retrieval strategies:
     - `MMR` (Max Marginal Relevance)
     - `MultiQuery`
   - Tune similarity search parameters for stricter context matching.

3. **Prompt Issues**
   - Prompt may lack clear constraints.
   - Model may be allowed to guess.

   **Testing Prompt:**
   - Check if prompt enforces:
     - “Use only provided data”
     - Avoid guessing

   **Solution:**
   - Add strict instructions:
     ```
     Only answer using the provided product data.
     If price is missing, say "I don’t know".
     Do not guess.
     ```

4. **Knowledge Cutoff / Outdated Model**
   - Model may not have updated pricing knowledge.
   - RAG pipeline may not be working properly.

   **Testing:**
   - Query: `"What is the price of Product X in 2024?"`
   - If older data is correct but current is wrong → model is outdated.

   **Solutions:**
   - Use a fine-tuned model with updated data.
   - Strengthen RAG pipeline for accurate retrieval.

### Diagnosis Log 1: Hallucinated Pricing
* **What I investigated first:** I checked if the AI was receiving the correct price in its prompt. I also checked if the model was getting too "creative."
* **What I ruled out:** I ruled out a "model temperature" issue. Even if the temperature (creativity) is 0, the AI will still guess the wrong price if it doesn't know the real one. 
* **What I identified as the root cause:** Knowledge Cutoff. The model was trained months ago and memorized old prices. 
* **How to distinguish:** To test this, check the text being sent to the AI. If the correct price is in the text but the AI ignores it, it is a Prompt or Temperature issue. If the correct price is *missing* from the text, it is a Retrieval or Knowledge Cutoff issue. 
* **The Fix:** Build a RAG pipeline. Before asking the AI, we search our database for the exact price, insert it into the prompt, and tell the AI: *"Only use the prices listed below. Do not guess."*


---

## Question 2: (Language Switching)

**Problem:**  
Chatbot occasionally responds in English even when the user writes in Hindi or Arabic.

**Answer:**  
This usually happens due to weak system-level instructions (e.g., `SystemMessage`) that fail to enforce language consistency.

### Cause:
- The model defaults to English (its dominant training language).
- System prompt does not enforce consistent language behavior.

### Solution:
- Add strict instructions in the system prompt:
  - Always respond in the same language as the user.
  - Detect and match user language dynamically.

Example:

Respond strictly in the same language as the user's input.
Do not switch languages unless explicitly asked.

### Diagnosis Log 2: Language Switching
* **What I investigated first:** I looked at the System Prompt (the hidden instructions given to the AI).
* **What I ruled out:** I ruled out the model's inability to speak Hindi or Arabic. GPT-4o is very good at both.
* **What I identified as the root cause:** The mechanism causing this is that the System Prompt is written in English. When the user writes a very short message in Arabic, the AI pays more attention to the long English system prompt and replies in English.
* **The Fix:** Add a specific, language-agnostic rule to the system prompt: *"CRITICAL: You must always reply in the exact same language the user used in their last message. If the user writes in Hindi, you must reply in Hindi. If Arabic, reply in Arabic."*

## Question 3: (Latency Degradation)

**Problem:**  
Response time increased from ~1.2s to 8–12s as user base grew.

**Answer:**  
Since no code changes were made, the issue is likely related to scalability, infrastructure, or system design.

### Possible Causes:
- Sequential request processing → queue buildup
- Increased context/token size → slower processing
- Slower retrieval (e.g., MultiQuery, Context Compression)
- External API/vendor latency under load

### Solutions:

1. **Optimize Context Size**
   - Large prompts increase latency.

   **Apply:**
   - Context trimming (remove irrelevant history)
   - Summarization of past interactions
   - Token limits per request

2. **Parallelization & Batching**
   - Avoid sequential processing.

   **Apply:**
   - Asynchronous request handling
   - Parallel execution
   - Worker queues with multiple consumers

3. **Improve Scalability**
   - Scale infrastructure based on load.

   **Apply:**
   - Horizontal and vertical scaling
   - Load balancing
   - Auto-scaling

4. **Optimize Retrieval Pipeline**
   - Reduce overhead from complex retrieval.

   **Apply:**
   - Cache frequent queries/results
   - Reduce retrieval calls per request
   - Use faster embedding indexes
   - Fallback to simpler retrieval under heavy load

5. **Streaming Responses**
   - Improve perceived latency.

   **Apply:**
   - Stream partial responses instead of waiting for full completion

### Diagnosis Log 3: Latency Degradation
* **Three distinct causes for slowness over time:**
    1.  **Context Bloat:** Users are having longer conversations. Sending a history of 50 messages to the AI takes much longer to process than sending 2 messages.
    2.  **API Rate Limits / Queueing:** As the user base grows, we might be hitting OpenAI's limits (Requests Per Minute), causing the system to wait in a queue or retry before succeeding.
    3.  **Database Slowdown:** If we use a database to search for answers (RAG), the database might be getting too big and slow because it lacks proper indexing.
* **What I would investigate first:** I would check **Context Bloat (Chat History)** first. This is the most common reason a chatbot slows down slowly over a few weeks without any code changes, because individual user chat sessions just keep getting longer and longer.


## Post-Mortem Summary (150–200 words)

The chatbot issues were caused by a mix of data, prompt, and scaling problems. The incorrect pricing responses were mainly due to missing or faulty retrieval from the product database, causing the model to guess answers instead of using real data. This was fixed by enforcing strict grounding in retrieved data and reducing model creativity.

The language switching issue occurred because the system prompt did not clearly instruct the model to maintain the user’s language. As a result, the model defaulted to English in some cases. This was resolved by adding a strong instruction to always respond in the same language as the user.

The increase in response time was caused by system scaling issues rather than code changes. As usage grew, longer conversation histories and higher traffic increased processing time. Limiting context size, optimizing retrieval, and adding caching helped restore performance.

Overall, these issues highlight the importance of strong prompt design, reliable data retrieval, and scalability planning in production AI systems.