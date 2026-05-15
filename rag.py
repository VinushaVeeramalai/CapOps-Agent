import os
from typing import List, Tuple
KB_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")

def init_rag():
    docs: List[Tuple[str, str]] = []
    files = ["hr_policies.txt", "it_sop.txt", "finance_faq.txt", "onboarding.txt"]
    
    for f in files:
        path = os.path.join(KB_DIR, f)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    docs.append((f, content))
            except Exception as e:
                print(f"Error loading {f}: {e}")
            
    if not docs:
        print("No documents loaded!")
        return None
        
    return docs

kb_docs = None


def _tokenize(text: str) -> set:
    return {token for token in text.lower().split() if token}


def _best_doc_for_query(query: str, docs: List[Tuple[str, str]]) -> Tuple[str, str, float]:
    query_tokens = _tokenize(query)
    if not query_tokens:
        return "Unknown", "", 0.0

    best_name = "Unknown"
    best_text = ""
    best_score = 0.0
    for name, content in docs:
        content_tokens = _tokenize(content)
        overlap = len(query_tokens & content_tokens)
        score = overlap / max(len(query_tokens), 1)
        if score > best_score:
            best_name = name
            best_text = content
            best_score = score
    return best_name, best_text, best_score

def query_kb(query: str) -> dict:
    global kb_docs
    if kb_docs is None:
        try:
            kb_docs = init_rag()
        except Exception as e:
            print(f"Failed to init RAG: {e}")
            return {"answer": "Knowledge base unavailable.", "source_doc": "None", "confidence_score": 0.0}
            
    if not kb_docs:
        return {"answer": "Knowledge base not loaded.", "source_doc": "None", "confidence_score": 0.0}
        
    try:
        source_doc_name, source_text, score = _best_doc_for_query(query, kb_docs)
        if source_text:
            snippet = source_text[:700].strip()
            answer = f"Based on {source_doc_name}: {snippet}"
        else:
            answer = "I could not find a strong match in the local knowledge base."
            
        return {
            "answer": answer,
            "source_doc": source_doc_name,
            "confidence_score": round(score, 2)
        }
    except Exception as e:
        print(f"Query error: {e}")
        return {"answer": "An error occurred while finding the answer.", "source_doc": "None", "confidence_score": 0.0}
