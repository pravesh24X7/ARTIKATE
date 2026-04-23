from langchain_groq import ChatGroq


class Generator:
    def __init__(self):
        self.llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.2
        )

    def generate(self, question, docs):
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are a legal assistant.

Answer ONLY from the context.
If answer not found, say "Not found".

Context:
{context}

Question:
{question}
"""

        response = self.llm.invoke(prompt)

        return response.content