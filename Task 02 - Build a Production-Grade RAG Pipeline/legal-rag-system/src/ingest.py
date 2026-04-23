from langchain_community.document_loaders import PyPDFLoader


def load_pdfs(file_paths):
    documents = []

    for path in file_paths:
        loader = PyPDFLoader(path)

        for doc in loader.load():
            doc.metadata["document"] = path.split("/")[-1]
            doc.metadata["page"] = doc.metadata.get("page", -1)
            documents.append(doc)

    return documents