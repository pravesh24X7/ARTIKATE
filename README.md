## ARTIKATE
**Technical Assignment for the Post of AI/ML Engineer**

### Directory Structure

```

ARTIKATE/
├── Task 01 - Diagnose a Failing LLM Pipeline/
│   └── Answers.md
│
├── Task 02 - Build a Production-Grade RAG Pipeline/
│   ├── data/contracts/         # all the pdf files go here
│   ├── faiss_index/
│   ├── src/
│   │   ├── **pycache**/
│   │   ├── **init**.py
│   │   ├── chunking.py
│   │   ├── embedding.py
│   │   ├── evaluator.py
│   │   ├── generator.py
│   │   ├── ingest.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   ├── .env
│   ├── Design.md
│   └── main.py
|   └── requirements.txt
│
├── Task 03 - Fine-Tune or Prompt-Engineer a Classifier/
│   ├── src/
│   │   ├── **pycache**/
│   │   ├── data/               # all the .csv data records go here
│   │   ├── models/
│   │   │   ├── **pycache**/
│   │   │   ├── evaluate.py
│   │   │   └── train.py
│   │   └── **init**.py
│   ├── Answers.md
│   └── requirements.txt
│
└── Task 04 - Written Systems Design Review/
└── Answers.md
```

### Setup instructions

**For Task 02**

Install required libraries
```bash
pip install -r requirements.txt
```

Create a .env file and store the value of both the keys in below given format.
```
export GROQ_API_KEY=your_key
export HUGGINGFACEHUB_API_TOKEN=your_key
```

**Note**:
**Add some demo contact files (3 to 5) in *data/contracts/* folder**

**How to run**

```bash
python main.py
```

**For Task 03**

Install required libraries
```bash
pip install -r requirements.txt
```

**How to run**

```bash
python -m src.models.train          # to train the model, first run this command
python -m src.models.evaluate       # second run this command to get the results.
```

**Note**: No additional data we've to add for running the **TASK 03**, as we've created the synthetic data using python.