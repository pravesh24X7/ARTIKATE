def precision_at_k(retriever, queries, ground_truth, k=3):
    correct = 0

    for q, gt in zip(queries, ground_truth):
        docs = retriever.invoke(q)

        top_k = docs[:k]
        retrieved_texts = [doc.page_content for doc in top_k]

        if any(gt in text for text in retrieved_texts):
            correct += 1

    return correct / len(queries)